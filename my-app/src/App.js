import React, { Component } from 'react';
import './App.css';
import axios from 'axios';
import Result from './components/Result';

class App extends Component {
  state = {
    chain: [],
    id: ''
  }

  getData() {
    axios
    .get('http://localhost:5000/chain')
    .then(response => this.setState({chain: response.data}))
    .catch(err => console.log(err));
  }

  handleSubmit = event => {
    event.preventDefault();
    this.getData()
  }

  handleInputChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  };

  render() {
    return (
      <div className="App">
        <form onSubmit={this.handleSubmit}>
          <input
            onChange={this.handleInputChange}
            placeholder="id"
            value={this.state.id}
            name="id"
          />
          <button type="submit">Submit</button>
          </form>
          {this.state.chain.length > 0 ? <Result chain={this.state.chain} /> : null}          
      </div>
    );    
  }
}

export default App;
