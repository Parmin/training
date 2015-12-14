var config = {
    SESSION_LIMIT: 50,
    DBPATH: '/data/db',
    MONGOD_PATH: '/home/vagrant/mongodb-linux-x86_64-3.0.6/bin/mongod',
    MONGO_PATH: '/home/vagrant/mongodb-linux-x86_64-3.0.6/bin/mongo',
    MONGOD_ARGS: ['--port', '5001', '--auth', '--storageEngine', 'wiredTiger', '--dbpath', '/home/vagrant/mws-dbpath'],
    CORS_DOMAINS: [
        // Any service that embeds MWS must have its origin whitelisted here.
        // Since this is the dev_config file, it should contain any address that devs use.
        "http://192.168.33.10:8000", // the default address for mitx when using Vagrant
        "http://192.168.33.11:3000", // the example app in the edu-mws repo
        "http://jasonz.pagekite.me:3000"
    ],
    RSA_PUB: './lib/server_rsa.pub',
    RSA_PEM: './lib/server_rsa.pem',
    DATA_PATH: '../../education/edu-mws-data',
    MONGOD_PORT: 5001, // Don't forget to change MONGOD_ARGS as well.
    SERVER_PORT: 8080
}

module.exports = config;
