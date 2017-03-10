function randomString(len, charSet) {
    charSet = charSet || 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var randomString = '';
    for (var i = 0; i < len; i++) {
    	var randomPoz = Math.floor(Math.random() * charSet.length);
    	randomString += charSet.substring(randomPoz,randomPoz+1);
    }
    return randomString;
}

function insertUserData(coll, count) {
    for (var x=0;x<count; x++) {
        var randomValue = randomString(15);
        var email = randomString(7);
        email = email + "@test.com"
        db.users.insert({userId:x,password:randomValue, emailAddress:email})
    }
}

