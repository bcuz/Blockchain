import React, { Component } from 'react';
// import './App.css';
import axios from 'axios';

class App extends Component {
  state = {
    chain: []
  }

  componentDidMount() {
    axios
    .get('http://localhost:5000/chain')
    .then(response => this.setState({chain: response.data}))
    .catch(err => console.log(err));
  }

  render() {
    return (
      <div className="App">
        <p>Current length of chain: {this.state.chain.length}</p>
      </div>
    );    
  }
}

export default App;
