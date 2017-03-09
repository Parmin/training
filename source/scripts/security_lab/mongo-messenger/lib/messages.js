const MongoClient = require('mongodb').MongoClient
const assert = require('assert')

const url = 'mongodb://localhost:27017/security-lab'
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
