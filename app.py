from uuid import uuid4

import flask
from flask import Flask, jsonify, request, Response
from blockchain import*
from ecc import*
from utils import*

# initiate the node
app = Flask(__name__)
# generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
# initiate the Blockchain
blockchain = BlockChain()
# set the basecoin
eth_k = generate_sk()
pk = eth_k.public_key
baseCoin = getAddress(pk.to_hex())
# number of transactions
nonce_tran = 0

@app.route('/init', methods=['GET'])
def init():
    blockchain.init_genesis(baseCoin)
    response = 'Succeed to init the blockchain'
    return jsonify(response, 200)

@app.route('/mine', methods=['GET'])
def mine():

    '''
        Apply consensus algorithm to choose the miner
        Pow algorithm is used
    
    '''
    # first we need to run the proof of work algorithm to calculate the new proof..
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    global nonce_tran
    # we must recieve reward for finding the proof in form of receiving 100 Coin
    blockchain.new_transaction(
        sender=0,
        recipient=baseCoin,
        amount=100,
        data='Mining',
        nonce=nonce_tran,
    )

    nonce_tran = nonce_tran + 1
    '''
        forge the new block by adding it to the chain
    '''
    # get previous hash
    previous_hash = blockchain.hash(last_block)

    # verify the validity of transactions
    if not blockchain.valid_transaction():
        return jsonify('There is invalid transaction', 500)

    # finish the work before mining
    stateRoot,  flag = blockchain.work_before_mine()
    if not flag:
        return jsonify('No enough balance', 500)

    # generate new block
    block = blockchain.new_block(
        proof=proof,
        stateRoot=stateRoot,
        previous_hash=previous_hash)

    # broadcast the new block
    blockchain.broadcast_block(block)

    response = {
        'message': "Forged new block.",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'receiptsRoot': block['receiptsRoot'],
        'transactionRoot': block['transactionRoot'],
        'stateRoot': block['stateRoot']
    }
    return jsonify(response, 200)

@app.route('/transaction/new', methods=['POST'])
def new_transaction():

    values = request.get_json()
    required = ['sender', 'recipient', 'amount', 'data', 'sk']

    if not all(k in values for k in required):
        return 'Missing values.', 400

    global nonce_tran
    # create a new transaction
    index = blockchain.new_transaction(
        sender = values['sender'],
        recipient = values['recipient'],
        amount = values['amount'],
        data = values['data'],
        nonce = nonce_tran,
        sk = values['sk']
    )

    nonce_tran = nonce_tran + 1

    response = {
        'message': f'Transaction will be added to the Block {index}',
    }
    return jsonify(response, 200)

@app.route('/transaction/find', methods=['POST'])
def find_transaction():
    values = request.get_json()
    res, flag = blockchain.get_transaction(values['hash'])
    if flag:
        return jsonify(res, 200)
    else:
        return jsonify(res, 500)

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/chain_request', methods=['GET'])
def chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/add', methods=['POST'])
def register_nodes():
    values = request.get_json()

    print('values', values)
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    # register each newly added node
    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': "New nodes have been added",
        'all_nodes': list(blockchain.nodes),
    }

    return jsonify(response), 200


@app.route('/nodes/resolve', methods=['POST'])
def consensus():
    # an attempt to resolve conflicts to reach the consensus
    conflicts = blockchain.resolve_conflicts()

    if conflicts:
        response = {
            'message': 'Our chain was replaced.',
            'new_chain': blockchain.chain,
        }
        return jsonify(response), 200

    response = {
        'message': 'Our chain is authoritative.',
        'chain': blockchain.chain,
    }
    return jsonify(response), 200

@app.route('/nodes/receiveBlock', methods=['POST'])
def come_block():
    block = request.get_json()

    # check the block
    msg, flag = blockchain.valid_come_block(block)
    if flag:
        # add block to local
        blockchain.new_block(
            proof=block['proof'],
            stateRoot=block['stateRoot'],
            previous_hash=block['previous_hash'],
            timestamp=block['timestamp'],
            tran=block['transactions']
        )
        return jsonify(msg + ': Succeed to add'), 200
    else:
        return jsonify('Invalid Block: ' + msg), 500

@app.route('/account/changeBasecoin', methods=['POST'])
def changeBasecoin():
    values = request.get_json()
    global baseCoin

    newbase = values.get('baseCoin')
    if validate_account(newbase):
        baseCoin = newbase
    else:
        return jsonify('Wrong Account', 200)

    response = {
        'Basecoin': baseCoin
    }
    return jsonify(response, 200)


@app.route('/account/getBalance', methods=['POST'])
def getBalance():
    values = request.get_json()
    res, flag = blockchain.get_balance(values['account'])
    if flag:
        return jsonify(res, 200)
    else:
        return jsonify(res, 500)


@app.route('/account/create', methods=['GET'])
def createAccount():
    eth_k = generate_sk()
    pk = eth_k.public_key
    account = getAddress(pk.to_hex())
    pk_hex = sk2hex(pk)
    response = {
        'Account': account,
        'PrivateKey': pk_hex
    }

    # for test only, send 100 to the account
    global nonce_tran
    # we must receive reward for finding the proof in form of receiving 100 Coin
    blockchain.new_transaction(
        sender=0,
        recipient=account,
        amount=100,
        data='Creating',
        nonce=nonce_tran,
    )

    nonce_tran = nonce_tran + 1

    return jsonify(response, 200)

