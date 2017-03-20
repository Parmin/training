const MongoClient = require('mongodb').MongoClient
const assert = require('assert')

const url = 'mongodb://node1:27001/security-lab?replicaSet=APPDB'
let messages = null;

MongoClient.connect(url, (err, db) => {
  assert.equal(null, err)
  messages = db.collection('messages')
})

exports.insert = message => {
  messages.insert(message)
}

exports.all = callback => {
  messages.find({}).toArray((err, data) => {
    assert.equal(null, err)
    callback(data)
  })
}
