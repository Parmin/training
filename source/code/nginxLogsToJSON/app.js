var NginxParser = require('nginxparser'),
    commandLineArgs = require('command-line-args'),
    ip = require("ip"),
    assert = require('assert');

var month = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}

var options = commandLineOptions();

console.log(options);

var parser = new NginxParser('$load_balancer $remote_addr  - - [$day/$month/$year:$hour:$minute:$second +$timezone] '
		+ '"$method $resource $version" $status $body_bytes_sent "$http_referrer" "$http_user_agent"');

parser.read(options.path, function (row) {
    var datestr = row.year+"-"
    +month[row.month]
    +"-"+row.day
    +"T"
    +row.hour
    +":"
    +row.minute
    +":"
    +row.second
    +"Z";

    var doc = {};
    doc.ipStr = row.ip_str;
    doc.ip = row.ip;
    if (row.http_referrer !== null) {
        doc.referrer = row.http_referrer;
    }
    doc.method = row.method;
    doc.resource = row.resource;
    doc.httpVersion = row.version;
    doc.status = row.status;
    doc.bodyBytesSent = parseInt(row.body_bytes_sent);
    doc.timestamp = new Date(datestr);
    doc.httpUserAgent = row.http_user_agent;
    console.log(doc);
}, function (err) {
    if (err) throw err;
    console.log('Done!')
});


function commandLineOptions() {

    var cli = commandLineArgs([
        { name: "path", alias: "p", type: String }
    ]);

    var options = cli.parse()

    return options;

}
