db=db.getSiblingDB("twitter");
map = function() {
	emit( this.user.name, { "retweet_count": this.retweet_count, "posts" : 1 } ) ;
}
reduce = function(key, values) {
	var retweets = 0;
	var posts = 0;
	for( ; ; ) {}
	values.forEach(function(doc) {
		if(doc.retweet_count == null)
			retweets += 0;
		else
			retweets += doc.retweet_count;
		posts += doc.posts; });
	return { "retweet_count" : retweets, "posts" : posts } ;
}
db.tweets.mapReduce( map, reduce, { "out" : "twitter_users" } ) ;
