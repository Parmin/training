import React from 'react'
import ReactDOM from 'react-dom'
import SweetAlert from 'sweetalert-react'
import io from 'socket.io-client'
import 'sweetalert/dist/sweetalert.css'

class App extends React.Component {
  constructor (props) {
    super(props)
    this.state = { 
      messages: [],
      show: false,
      userName: localStorage.getItem('username'),
    }
  }

  componentDidMount () {
    this.socket = io('/')

    this.socket.on('initalMessages', messages => {
      this.setState({ messages: messages })
    })

    this.socket.on('message', message => {
      this.setState({ messages: [...this.state.messages, message] })
    })
  }

  componentWillMount () {
    if (!this.state.userName) {
      this.setState({ show: true })
    }
  }

  componentDidUpdate () {
    this._scrollMessagesToBottom()
  }

  saveUser = userName => {
    localStorage.setItem('username', userName)
    this.setState({
      show: false,
      userName,
    })
  }

  sendMessage = event => {
    const body = event.target.value
    if (event.keyCode === 13 && body) {
      const message = {
        from: this.state.userName,
        body,
      }
      this.setState({ messages: [...this.state.messages, message] })
      this.socket.emit('message', message)
      event.target.value = '' // clear the input
    }
  }

  _scrollMessagesToBottom () {
    this.messages.scrollTop = 10000000000000
  }

  render () {
    const messages = this.state.messages.map((message, index) => {
      return <li key={index}><strong>{message.from}:</strong> {message.body}</li>
    })

    return (
      <div>
        <SweetAlert
          show={this.state.show}
          title="Welcome to Mongo Messenger!"
          text="Enter your desired username"
          type="input"
          inputPlaceholder="username"
          confirmButtonText="Submit"
          onConfirm={this.saveUser}
        />

        <div className="container">
          <h1 className="header">Mongo Messenger</h1>
          <div className="client">
            <div className="messages" ref={(messages) => { this.messages = messages }}>{messages}</div>
            <input type='text' placeholder='Enter a message...' onKeyUp={this.sendMessage} />
          </div>
        </div>
      </div>
    )
  }
}

ReactDOM.render(<App />, document.getElementById('root'))
