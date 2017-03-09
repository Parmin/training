const fs = require('fs')
const markov = require('markov')

const m = markov(2) // 2nd order markov chain generator
const consultingChat = fs.readFileSync(__dirname + '/consulting-chat.txt')

m.seed(consultingChat)

exports.send = callback => {
  (function generateRandomMessage () {
    _randomly(() => {
      const msg = _generateRandomMessage()
      callback({
        from: 'consulting engineer',
        body: msg,
      })
      generateRandomMessage()
    })
  })()
}

const _generateRandomMessage = () => {
  return m.fill(m.pick(), 11).join(' ')
}

const _randomly = callback => {
  // randomly under one minute do something
  setTimeout(() => callback, Math.random() * 60 * 1000)
}
