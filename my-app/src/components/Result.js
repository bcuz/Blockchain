import React, { Component } from 'react';

class Result extends Component {

  render() {

    var total = 0

    for (var block of this.props.chain.chain) {
      for (var trans of block.transactions) {

        // way this is written will reject anything sent to yourself
        if (trans.recipient === this.props.id && trans.sender !== this.props.id) {
          total += parseInt(trans.amount)
        } else if (trans.recipient !== this.props.id && trans.sender === this.props.id) {
          total -= parseInt(trans.amount)
        }
      }
    }

    return (
      <div>
        <p>balance: {total}</p>
        <p>transactions including {this.props.id}:</p>
        {this.props.chain.chain.map(block => {
          
          return block.transactions.map(trans => {

            if (trans.recipient === this.props.id || trans.sender === this.props.id) {
              return (
                <div className="trans">
                  <p>amount: {trans.amount}</p>
                  <p>recipient: {trans.recipient}</p>
                  <p>sender: {trans.sender}</p>
                </div>)
              
            }


          })
        })}
      </div>
    );    
  }  

}

export default Result;
