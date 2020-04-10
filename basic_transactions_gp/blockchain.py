# Paste your version of blockchain.py from the client_mining_p
# folder here
import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_cors import CORS


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    # * New transactions - for Wallet
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append(
            {"sender": sender, "recipient": recipient, "amount": amount}
        )

        return self.last_block["index"] + 1

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

        if len(self.chain) > 0:
            block_string = json.dumps(self.last_block, sort_keys=True)
            guess = f"{block_string}{proof}".encode()
            current_hash = hashlib.sha256(guess).hexdigest()
        else:
            current_hash = ""
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
            "hash": current_hash,
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

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
        guess = f"{block_string}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:6] == "000000"


# Instantiate our Node
app = Flask(__name__)
CORS(app)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace("-", "")

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route("/", methods=["GET"])
def home():
    return "<a href='/chain'>chain</a> || <a href='/last_block'>last block</a>"


@app.route("/mine", methods=["POST"])
def mine():
    try:
        req = request.get_json()
    except ValueError:
        res = {"that isn't json"}
        print(res)
        return jsonify(res), 400

    validate = ["proof", "id"]

    if not all(i in req for i in validate):
        res = {"something is missing..."}
        print(res)
        return jsonify(res), 400

    valid = req["proof"]
    last_block = json.dumps(blockchain.last_block, sort_keys=True)

    if blockchain.valid_proof(last_block, valid):
        previous = blockchain.hash(blockchain.last_block)
        new = blockchain.new_block(valid, previous)
        res = {"new_block": new}
        print(f"new block --> {res}")
        return jsonify(res), 200
    else:
        res = {"something went wrong"}
        print(res)
        return jsonify(res), 400


@app.route("/chain", methods=["GET"])
def full_chain():
    response = {"length": len(blockchain.chain), "chain": blockchain.chain}
    return jsonify(response), 200


@app.route("/last_block", methods=["GET"])
def get_last_block():
    response = {"last_block": blockchain.last_block}
    return jsonify(response), 200


# TODO for Wallet
# * request.get_json gets data out of POST
# * check if all values are present (sender, recipient, and amount)
# * if error, return 400 with jsonify(res)
# * if success, return index of the block with the transaction


@app.route("/transactions/new", methods=["POST"])
def get_transaction():
    req = request.get_json()
    validate = ["sender", "recipient", "amount"]

    if not all(k in req for k in validate):
        res = {"message": "Something is missing..."}
        return jsonify(res), 400

    index = blockchain.new_transaction(req["sender"], req["recipient"], req["amount"])
    res = {"message": f"Transaction added to block {index}"}

    return jsonify(res), 201


# Run the program on port 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
