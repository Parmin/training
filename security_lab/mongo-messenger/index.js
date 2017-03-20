const express = require('express')
const http = require('http')
const bodyParser = require('body-parser')
const socketIo = require('socket.io')
const webpack = require('webpack')
const webpackDevMiddleware = require('webpack-dev-middleware')
const webpackConfig = require('./webpack.config.js')

const Messages = require('./lib/messages.js')
const Bot = require('./lib/bot.js')

const app = express()
const server = http.createServer(app)
const io = socketIo(server)

app.use(express.static(__dirname + '/public'))
app.use(webpackDevMiddleware(webpack(webpackConfig)))
app.use(bodyParser.urlencoded({ extended: false }))

// health check for AWS
app.get('/user/login', (req, res) => {
  res.sendStatus(200)
})

io.on('connection', socket => {
  // whenever a client connects send them all the messages in the db
  Messages.all(messages => {
    socket.emit('initalMessages', messages)
  })

  // whenever a new message is received store it and send it out
  socket.on('message', message => {
    Messages.insert(message)
    socket.broadcast.emit('message', message)
  })

  // have a bot simulate conversation
  Bot.send(message => {
    Messages.insert(message)
    socket.broadcast.emit('message', message)
  })
})

server.listen(8080)
