import React, { Component } from 'react';

class Result extends Component {

  render() {

    var total = 0

    for (var block of this.props.chain.chain) {
      for (var trans of block.transactions) {

        // way this is written will reject anything sent to yourself
        if (trans.recipient === this.props.id && trans.sender !== this.props.id) {
          total += trans.amount             
        } else if (trans.recipient !== this.props.id && trans.sender === this.props.id) {
          total -= trans.amount
        }
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
