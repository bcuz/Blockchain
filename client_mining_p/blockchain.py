import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

class Blockchain(object):
  def __init__(self):
    self.chain = []
    self.current_transactions = []

    # Create the genesis block
    self.new_block(previous_hash=1, proof=100)

  def new_block(self, proof, previous_hash=None):
    """
    Create a new Block in the Blockchain

    A block should have:
    * Index
    * Timestamp
    * List of current transactions
    * The proof used to mine this block
    * The hash of the previous block

    :param proof: <int> The proof given by the Proof of Work algorithm
    :param previous_hash: (Optional) <str> Hash of previous Block
    :return: <dict> New Block
    """

    block = {
      'index': len(self.chain) + 1,
      'timestamp': time(),
      'transactions': self.current_transactions,
      'proof': proof,
      # if not none or the previous block hashed
      'previous_hash': previous_hash or self.hash(self.chain[-1]),
    }

    # Reset the current list of transactions
    self.current_transactions = []

    # Append the block to the chain
    self.chain.append(block)
    # Return the new block
    return block

  def hash(self, block):
    """
    Creates a SHA-256 hash of a Block

    :param block": <dict> Block
    "return": <str>
    """
    # Step 1: convert block / dictionary / object into usable string
    # Step 2: hash that string and return it
    # Step 3: profit $$

    # Use json.dumps to convert json into a string
    # Use hashlib.sha256 to create a hash
    # It requires a `bytes-like` object, which is what
    # .encode() does.
    # It converts the Python string into a byte string.
    # We must make sure that the Dictionary is Ordered,
    # or we'll have inconsistent hashes

    # Step 1
    # Create the string_object: convert block to a string
    string_object = json.dumps(block, sort_keys=True)
    # Create the block_string
    block_string = string_object.encode()

    # Step 2
    # Hash this string using sha256
    hash_object = hashlib.sha256(block_string)
    hash_string = hash_object.hexdigest()

    # By itself, the sha256 function returns the hash in a raw string
    # that will likely include escaped characters.
    # This can be hard to read, but .hexdigest() converts the
    # hash to a string of hexadecimal characters, which is
    # easier to work with and understand

    # Return the hashed block string in hexadecimal format
    # Gonna look like this:
    # '2c931fa172ec39bc333089e0dc03e904a61a0384b994e418249d1e3320f199c1'
    return hash_string

  @property
  def last_block(self):
    return self.chain[-1]

  # def proof_of_work(self):
  #   """
  #   Simple Proof of Work Algorithm
  #   Stringify the block and look for a proof.
  #   Loop through possibilities, checking each one against `valid_proof`
  #   in an effort to find a number that is a valid proof
  #   :return: A valid proof for the provided block
  #   """
  #   # Stringify the last block
  #   string_object = json.dumps(self.last_block, sort_keys=True)

  #   proof = 0

  #   while self.valid_proof(string_object, proof) is False:
  #     proof += 1

  #   return proof

  @staticmethod
  def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 3
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    # add the current proof from loop to the block and hash it
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # valid proof has to have three 0s in the beginning
    if guess_hash[:6] == '000000':
      print(guess_hash)
      return True
    return False

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['POST'])
def mine():
  # Run the proof of work algorithm to get the next proof

  # changing the transaction in a block, causes the prev_hash value in the next block to be wrong. and because it's wrong, the attacker has to regenerate any remaining blocks after it in the arr. and this is hard to do cuz we brute force the proof
  # proof = blockchain.proof_of_work()

  # # Forge the new Block by adding it to the chain with the proof

  # # easy to check whether a previous hash is correct
  data = request.get_json()
  # print(data)

  # if specific proof already in the chain, reject it

  # proof not validated server side, which is necessary, otherwise 
  # we will accept any non-duplicate proof client gives us.
  for blk in blockchain.chain:
    if data['proof'] == blk['proof']:
      return jsonify({'message': 'proof already used, bruh'}), 400      

  previous_hash = blockchain.hash(blockchain.last_block)
  block = blockchain.new_block(data['proof'], previous_hash)

  response = {
    'message': 'We mined a new block!',
    'index': block['index'],
    'transactions': block['transactions'],
    'proof': block['proof'],
    'previous_hash': block['previous_hash']
  }

  return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
  response = {
    # TODO: Return the chain and its current length
    'chain': blockchain.chain,
    'length': len(blockchain.chain)
  }
  return jsonify(response), 200

@app.route('/last_block', methods=['GET'])
def last_block():
  response = blockchain.chain[-1]
  return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)