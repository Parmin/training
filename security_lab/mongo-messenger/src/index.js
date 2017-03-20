import React from 'react'
import ReactDOM from 'react-dom'
import SweetAlert from 'sweetalert-react'
import 'sweetalert/dist/sweetalert.css'

import Client from './client.js'

class App extends React.Component {
  constructor (props) {
    super(props)
    this.state = { 
      show: false,
      userName: localStorage.getItem('username'),
    }
  }

  componentWillMount () {
    if (!this.state.userName) {
      this.setState({ show: true })
    }
  }

  saveUser = userName => {
    localStorage.setItem('username', userName)
    this.setState({
      show: false,
      userName,
    })
  }

  render () {
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
        <Client userName={this.state.userName} />
      </div>
    )
  }
}

ReactDOM.render(<App />, document.getElementById('root'))
