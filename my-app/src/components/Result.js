import React, { Component } from 'react';

class Result extends Component {

  render() {
    return (
      <div>
        chain length is {this.props.chain.length}
      </div>
    );    
  }  

}

export default Result;
