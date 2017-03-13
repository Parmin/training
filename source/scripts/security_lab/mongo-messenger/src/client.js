import React from 'react'
import ReactDOM from 'react-dom'
import io from 'socket.io-client'

export default class Client extends React.Component {
  constructor (props) {
    super(props)

    this.state = { 
      messages: [],
      height: 700,
    }

    window.onresize = event => { this._updateMessagesHeight() }
  }

  componentDidMount () {
    this.socket = io('/')

    this.socket.on('initalMessages', messages => {
      this.setState({ messages: messages })
    })

    this.socket.on('message', message => {
      this.setState({ messages: [...this.state.messages, message] })
    })

    this._updateMessagesHeight()
  }

  componentDidUpdate () {
    this._scrollMessagesToBottom()
  }

  sendMessage = event => {
    const body = event.target.value
    if (event.keyCode === 13 && body) {
      const message = {
        from: this.props.userName,
        body,
      }
      this.setState({ messages: [...this.state.messages, message] })
      this.socket.emit('message', message)
      event.target.value = '' // clear the input
    }
  }

  _updateMessagesHeight () {
    this.setState({ height: this._calcMessagesHeight() })
  }

  _calcMessagesHeight () {
    const windowHeight = window.innerHeight
    const headerHeight = document.querySelector('.header').clientHeight
    const inputHeight = document.querySelector('input').clientHeight
    const padding = 95

    return windowHeight - headerHeight - inputHeight - padding
  }

  _scrollMessagesToBottom () {
    this.messages.scrollTop = 10000000000000
  }

  render () {
    const messages = this.state.messages.map((message, index) => {
      return <li key={index}><strong>{message.from}:</strong> {message.body}</li>
    })

    const messagesStyle = {
      height: this.state.height
    }

    return (
      <div className="container">
        <h1 className="header" ref={(header) => { this.header = header }}>Mongo Messenger</h1>
        <div className="client">
          <div className="messages" style={messagesStyle} ref={(messages) => { this.messages = messages }}>{messages}</div>
          <input type='text' ref={(input) => { this.input = input }} placeholder='Enter a message...' onKeyUp={this.sendMessage} />
        </div>
      </div>
    )
  }
}
