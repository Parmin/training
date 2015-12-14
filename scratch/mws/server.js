var util = require('./lib/util.js'),
    session = require('./lib/session.js'),
    child = require('child_process'),
    cors = require('cors'),
    parser = require('body-parser'),
    cookie = require('cookie'),
    ursa = require('ursa'),
    fs = require('fs'),
    MongoDB = require('mongodb');


// Load configuration appropriately. We want to crash quickly if there's no environment specified.
// Note: Possible update is just setting an environment variable to the file that we want to load from.
var config;
if (require.main === module) {
    console.log("ENV: " + process.env.NODE_ENV)
    if (process.env.NODE_ENV === 'development') {
        config = require('./lib/dev_config.js');
    } else if (process.env.NODE_ENV === 'production') {
        config = require('./lib/prod_config.js');
    } else if (process.env.NODE_ENV === 'staging') {
        config = require('./lib/staging_config.js');
    } else {
        console.error('No NODE_ENV specified.');
        process.exit(1);
    }
} else {
    // If this module is run via a require, as opposed to directly using node, use the testing config info.
    config = require('./lib/testing_config.js');
}

// Load in global variables. We want to crash if we can't find either of these files.
var crt = ursa.createPublicKey(fs.readFileSync(config.RSA_PUB)),
    key = ursa.createPrivateKey(fs.readFileSync(config.RSA_PEM)),
    PASSWORD = null;

/*
Get a database URI.
*/
function getUri(db) {
    return 'mongodb://localhost:' + config.MONGOD_PORT.toString() + '/' + db;
}

/*
Get the path to a file inside the data directory.
*/
function getPath(folder, file) {
    return config.DATA_PATH + '/' + folder + '/' + file;
}

/*
Get the path to a file inside the data directory.
*/
function getGithubScriptPath(file) {
    return '../../university-exercises/' + file;
}

/*
Write to a given input stream.
*/
function write(ps, message) {
    ps.stdin.write(message + '\n');
}

/*
Spawn a new mongod.
*/
function spawnDatabase(create_admin, callback) {
    console.log('spawning mongod...');
    mongod = child.spawn(config.MONGOD_PATH, config.MONGOD_ARGS).on('error', function(err) {
	if (err.errno === 'ENOENT') {
	    throw new Error("File doesn't exist: " + err.path);
	} else {
	    throw err;
	}
    });
    if (create_admin) {
        setTimeout(function() {
            MongoDB.connect(getUri('admin'), function(err, db) {
                db.addUser('su', PASSWORD, {roles: ['root', '__system']}, function(result) {
                    db.close(function (res) {
                        if (res) { console.log(res); }
                    });

                    if (callback) {
                        callback();
                    }
                });
            });
        }, 1000);
    }

    // In production, these statements are piped into a log file.
    mongod.stdout.on('data', function(data) {
        console.log(data.toString());
    });

    // If it crashes, respawn it. Users may get an error, but they should be able to pick back up.
    mongod.on('exit', function(code) {
        console.log('mongod exited with code ' + code);
        spawnDatabase(false);
    });
}

/*
All the code to run a server.
*/
function runServer() {

    // Warning: If you're doing this in development, don't use the same DBPATH as your other MongoDB instances!
    // We wipe the data directory to ensure there's no residual state from the last time the server was run.
    child.exec("rm -rf " + config.DBPATH + "/*", function(err, stdout, stderr) {
        if (err || stderr) {
            console.log("database clear error: " + err + stderr);
            process.exit(1);
        }

        // Generate a random password, and put it into a logfile on the server.
        PASSWORD = util.hash(Math.random()); // see admin.log for password
        fs.mkdir('logs', function(err) {
            if (err && err.code !== 'EEXIST') { throw err; }
            fs.writeFile('logs/admin.log', PASSWORD, function(err) {
                if (err) { throw err; }
            });
        });

        // Spawn the server, and then connect to it with the new administrative user.
        spawnDatabase(true, function() {
            MongoDB.connect(getUri('admin'), function(err, db) {

                if (err) { throw new Error(err); }

                // Authenticate. Note: We can perform all db operations as an admin user, since the users interact
                // with the database through a mongo shell, which isn't authenticated as admin.
                db.admin().authenticate('su', PASSWORD, function(err, result) {
                    if (err) {
                        // Usually the cause is a non-empty dbpath. Since the auth credentials
                        // are regenerated every time the server starts, they're not going to work
                        // with an existing dbpath. 
                        // TODO automatically delete the dbpath on startup?
                        throw err;
                    }
                    var app = require('express')();
                    var http = require('http').Server(app);
                    var conn = require('socket.io').listen(http);

                    app.use(parser.json());

                    var corsOptions = {
                        origin: function(origin, callback){
                            var originIsWhitelisted = config.CORS_DOMAINS.indexOf(origin) !== -1;
                            callback(null, originIsWhitelisted);
                        },
                        credentials: true
                    };

                    // This endpoint is for correctly setting session cookies.
                    app.get('/', cors(corsOptions), function(req, res) {
                        var ip_addr = req.ip;
                        var session = checkCookie(req.headers.cookie, ip_addr);

                        if (!session) {
                            var msg = ip_addr + '|' + Math.random().toString();
                            msg = crt.encrypt(msg, 'utf8', 'base64');
                            res.set('Set-Cookie', 'mws=' + msg + ';');
                        }
                        res.end();
                    });

                    // This endpoint is for the education server to verify the state
                    // of user databases.
                    app.options('/verify', cors(corsOptions));
                    app.post('/verify', cors(corsOptions), function(req, res) {

                        // Useful for testing verification from the client.
                        // If the session identifier is missing, set it based on cookies.
                        if (!req.body.ses) {
                            try {
                                var session_id = checkCookie(req.headers.cookie, req.ip);

                                if (session_id) {
                                    req.body.ses = session_id;
                                } else {
                                    res.status(401).send("Unauthorized");
                                    res.end();
                                    return;
                                }
                            } catch (c) {
                                res.status(401).send("Unauthorized");
                                res.end();
                                return;
                            }
                        }
                        else {
                            // If the session identifier is there, decrypt it.
                            try {
                                req.body.ses = key.decrypt(req.body.ses, 'base64', 'utf8');
                            } catch (e) {
                                console.log("Bad session.")
                                res.status(401).send("Unauthorized");
                                res.end();
                            }
                        }

                        // See if the session is available. If it isn't, return a 401.
                        // We don't return a 404 because we don't want to tell users why the request failed.
                        if (session.get(req.body.ses, req.body.sock, req.body.db) !== undefined &&
                            typeof req.body.db === 'string') {

                            _db = db.db(req.body.db);

                            // Read in the verification script, and execute it through the driver.
                            var script = "";
                            var path = getPath('verification', req.body.script);
                            try {
                                script = fs.readFileSync(path, {encoding: 'utf8'});
                            } catch (e) {
                                console.log('Error reading in verification script: ' + e);
                                res.end();
                                return;
                            }

                            // Evaluate the script, and check the result. Script must return true if the state is correct.
                            evaluate(_db, script, function(result) {
                                if (result === true) {
                                    res.send(JSON.stringify({ 'status' : true }));
                                    res.end();
                                } else {
                                    res.send(JSON.stringify({ 'status' : false }));
                                    res.end();
                                }
                            });

                        } else {
                            console.log("Bad session.")
                            res.status(401).send("Unauthorized");
                            res.end();
                        }

                    });

                    // Set up socket listeners, and fire up the server.
                    configureSocket(conn, db);

                    http.listen(config.SERVER_PORT, function() {
                        console.log('listening on port ' + config.SERVER_PORT + '...');
                    });
                });
            });
        });
    });
}

/*
Configure a new socket.
*/
function configureSocket(io, db) {
    io.on('connection', function(socket) {

        // Verify the session. If it isn't acceptable, send back unauthorized and disconnect.
        var session_identifier = checkCookie(socket.request.headers.cookie, socket.request.connection.remoteAddress);

        if (!session_identifier) {
            socket.emit('unauthorized', 'We were unable to authenticate you.');
            socket.disconnect();
            return;
        }

        // Create a new shell instance for the client.
        socket.on('create shell', function(initialization, callback) {

            initialization = JSON.parse(initialization);
            // Create a "unique" database identifier. On the rare case of a hash collision, not sure what will happen.
            var database = util.hash(session, Math.random());

            _db = db.db(database);
            // Configure database, if it's successful, open up the shell.
            configureDatabase(_db, initialization, database, session_identifier, function(success) {

                if (!success) {
                    callback(false, 'Unable to create a shell.');
                    dropDatabase(_db);
                    return;
                }

                var connected = session.insert(session_identifier, socket.id, database, function() {
                    var mongo_args = ['--port', config.MONGOD_PORT.toString(), '--shell', '--norc', '--quiet', '-u', database, '-p', session_identifier, database, "lib/init.js"];
                    var mongo_process = child.spawn(config.MONGO_PATH, mongo_args);

                    mongo_process.stdout.on('data', function(data) {
                        socket.emit('message', database, data.toString());
                    });

                    return mongo_process;
                });

                if (connected) {
                    var shell = session.get(session_identifier, socket.id, database);

                    if (shell) {
                        //**
                        // Write description to start exercise
                        //**
                        var path = getGithubScriptPath(initialization.script);

                        try {
                            script = fs.readFileSync(path, {encoding: 'utf8'});
                        } catch (e) {
                            console.log('Error reading in initialization script: ' + e);
                        }

                        _db.eval(script, "getDescription()", function(err, result) {
                            socket.emit('message', database, result);
                        });
                    }

                    callback(true, database);
                } else {
                    callback(false, 'Unable to create a shell.');
                    dropDatabase(_db);
                }

            });

        });

        // On message, write it into the shell. We don't need to perform any verification here.
        // All verification happens either when the shell is initialized, or via MongoDB's auth.
        socket.on('message', function(database, message, initialization) {
            var shell = session.get(session_identifier, socket.id, database);

            if (shell) {
                write(shell, message);


                //**
                // Check if exercise has been solved
                //**
                
                var path = '../../university-exercises/3.0/crud/find_student_grades.js';

                try {
                    script = fs.readFileSync(path, {encoding: 'utf8'});
                } catch (e) {
                    console.log('Error reading in initialization script: ' + e);
                }

                try {
                    _db = db.db(database);
                    _db.eval(script, ["submit()", message], function(err, result) {
                        if (result === true) {
                            write(shell, "printjson('CORRECT')");
                        } 
                    });
                } catch (e) { console.log(e)}

                console.log(message);
            }
        });

        // Gimmick for implementing autocompletion. If the shell changes significantly, this method
        // will need to change.
        socket.on('autocomplete', function(database, prefix) {
            var shell = session.get(session_identifier, socket.id, database);

            if (shell) {
                var input = "shellAutocomplete(" + JSON.stringify(prefix) + "); __autocomplete__";
                write(shell, input);
            }
        });

        // Verification via socket. Only used for tutorials, which aren't "serious" -- quizzes,
        // homeworks, and finals are all verified via POSTing to the /verify endpoint.
        socket.on('verify', function(database, filename, callback) {

            var script;
            var path = getPath('verification', filename);
            try {
                script = fs.readFileSync(path, {encoding: 'utf8'});
            } catch (e) {
                console.log('Error reading in verification script: ' + e);
                return;
            }

            _db = db.db(database);
            evaluate(_db, script, function(result) {
                if (result === true) {
                    callback(true);
                } else {
                    callback(false);
                }
            });
        })

        // Clean up the database and shell. After this completes, there should be no trace of the user.
        socket.on('close', function(database, callback) {

            if (typeof database !== 'string') {
                callback(false);
                return;
            }

            _db = db.db(database);

            var shell = session.get(session_identifier, socket.id, database);

            if (shell) {
                dropDatabase(_db);
                shell.kill('SIGKILL');
                session.remove(session_identifier, socket.id, database);
                callback(true);
                console.log('dropped database ' + database);
            } else {
                dropDatabase(_db);
                callback(false);
                console.log('failed to drop database ' + database);
            }
        });

        // Clean up all of the shells within a particular socket. This is why each shell must also be identified by
        // socket identifier.
        socket.on('disconnect', function() {
            var mongos = session.getAll(session_identifier, socket.id);

            console.log('socket ' + socket.id + ' disconnected. dropping all databases...');

            var db_ids = Object.getOwnPropertyNames(mongos);
            for (var i = 0; i < db_ids.length; i++) {

                var database = db_ids[i];
                var shell = mongos[database];

                if (typeof database === 'string') {
                    _db = db.db(database);

                    if (shell) {
                        dropDatabase(_db);
                        shell.kill('SIGKILL');
                        session.remove(session_identifier, socket.id, database);
                    }
                }
            }
        });
    });
}

/*
Configure a new database with a user and any initial state.
*/
function configureDatabase(_db, initialization, identifier, password, callback) {

    var script, json;
    // Add the limited user all user commands will be executed under.
    _db.addUser(identifier, password, {roles : [{role: "readWrite", db: identifier}]}, function(result) {
        console.log("Initialization script: " + initialization.script);

        // If there's a script, read it in.
        if (initialization.script) {
            var path = getGithubScriptPath(initialization.script);

            console.log("Initialization script path: " + path);

            try {
                script = fs.readFileSync(path, {encoding: 'utf8'});
            } catch (e) {
                console.log('Error reading in initialization script: ' + e);
            }

            _db.eval(script, "setup()", function(err, result) {
                if (result === true) {
                    callback(true);
                } else {
                    callback(false);
                }
            });
        }
        
    });
}

/*
Drop a database by identifier.
*/
function dropDatabase(_db) {
    _db.dropDatabase( function(res) {
        if (res) { console.log(res); }
    });
}

/*
Evaluate a script in a databate.
*/
function evaluate(_db, script, callback) {
    _db.eval(script, function(err, result) {
        callback(result);
    });
}

/*
Validate a session cookie.
*/
function checkCookie(cookie_header, ip_address) {
    if (!cookie_header) {
        console.log("Bad cookie: no cookies.");
        return false;
    }

    var cookies = cookie.parse(cookie_header);

    if (!cookies.mws) {
        console.log("Bad cookie: no MWS cookie.");
        return false;
    }

    var ses_id;
    try {
        ses_id = key.decrypt(cookies.mws, 'base64', 'utf8');
    } catch (e) {
        console.log("Bad cookie: unable to decrypt.");
        return false;
    }

    // Cookie is valid if it has the form <ip address>|<random number>
    var pieces = ses_id.split("|");
    if (pieces.length !== 2 || pieces[0] !== ip_address) {
        console.log("Bad cookie: IP addresses don't match.");
        return false;
    }

    return ses_id;
}

if (require.main === module) {
    runServer();
} else {
    module.exports = {
        checkCookie: checkCookie,
        evaluateDatabase: evaluate,
        dropDatabase: dropDatabase,
        configureDatabase: configureDatabase,
        spawnDatabase: spawnDatabase,
        getPath: getPath,
        getUri: getUri
    }
}
