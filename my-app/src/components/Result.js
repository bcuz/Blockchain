import React, { Component } from 'react';

class Result extends Component {

  render() {

    var total = 0

    for (var block of this.props.chain.chain) {
      for (var transaction of block.transactions) {

        // if getter, increment
        // if sender, decrement
        console.log(transaction.recipient);


      }
    }

    return (
      <div>
        balance: {total}
      </div>
    );    
  }  

}

export default Result;
