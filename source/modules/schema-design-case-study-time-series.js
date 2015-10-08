function populateSeconds(metric, min, max) {
    var now = ISODate();
    now.setMilliseconds(0);
    now.setSeconds(0);
    var nowInt = now.getTime();
    for (hour=0; hour<96; hour++) {
	for (minute=0; minute<60; minute++) {
	    var minuteDocument = {};
	    minuteDocument.minute = new Date(nowInt);
	    minuteDocument.metric = metric;
	    minuteDocument.values = [];
	    for (second=0; second<60; second++) {
		var rVal = Math.floor(Math.random() * (max - min)) + min;
		minuteDocument.values.push(rVal);
	    }
	    db.metrics.insert(minuteDocument);
	    nowInt -= 60000;
	}
	
    }

}


function getOneMinuteGranularity() {
    var cur = db.oneMinuteMetrics.aggregate(
	[ { "$unwind": "$values" },
	  { "$group": { "_id": { "metric": "$metric", "minute": "$minute"},
			"value" : { "$avg" : "$values" } } },
	  { "$project": { "_id" : 0,
	                  "metric": "$_id.metric",
			  "minute": "$_id.minute",
			  "value": "$value" } },
	  { "$sort": { "minute": 1 } }
	]
    )

    while (cur.hasNext()) {
	var minute = cur.next();
	printjson(minute);
    }
}


// db.metrics.createIndex( { "minute": 1 }, { expireAfterSeconds: 345600 } )
