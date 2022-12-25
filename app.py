from uuid import uuid4
from flask import Flask, jsonify, request
from blockchain import*
from ecc import*

# initiate the node
app = Flask(__name__)
# generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
# initiate the Blockchain
blockchain = BlockChain()
# set the basecoin
eth_k = generate_eth_key()
pk = eth_k.public_key
baseCoin = getAddress(pk.to_hex())
# number of transactions
nonce_tran = 0

@app.route('/mine', methods=['GET'])
def mine():
    # Ensure nodes are synchronized
    blockchain.resolve_conflicts()

    '''
        Apply consensus algorithm to choose the miner
        Pow algorithm is used
    
    '''
    # first we need to run the proof of work algorithm to calculate the new proof..
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # we must recieve reward for finding the proof in form of receiving 100 Coin
    blockchain.new_transaction(
        sender=0,
        recipient=baseCoin,
        amount=100,
        data='Mining',
        nonce=nonce_tran + 1,
    )

    '''
        forge the new block by adding it to the chain
    '''
    # get previous hash
    previous_hash = blockchain.hash(last_block)

    # verify the validity of transactions
    if not blockchain.valid_transaction():
        return jsonify('There is invalid transaction', 500)

    # finish the work before mining
    stateRoot, transactionRoot, flag = blockchain.work_before_mine()
    if not flag:
        return jsonify('No enough balance', 500)

    # generate new block
    block = blockchain.new_block(
        proof=proof,
        tranRoot=transactionRoot,
        stateRoot=stateRoot,
        previous_hash=previous_hash)

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

@app.route('/transaction/new', methods=['GET'])
def new_transaction():

    values = request.get_json()
    required = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required):
        return 'Missing values.', 400

    # create a new transaction
    index = blockchain.new_transaction(
        sender = values['sender'],
        recipient = values['recipient'],
        amount = values['amount']
    )

    response = {
        'message': f'Transaction will be added to the Block {index}',
    }
    return jsonify(response, 200)

@app.route('/chain', methods=['GET'])
def full_chain():
    blockchain.resolve_conflicts()
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
    print('begin to solve conflict')
    conflicts = blockchain.resolve_conflicts()

    if (conflicts):
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


@app.route('/changeBasecoin', methods=['GET'])
def changeBasecoin():
    values = request.get_json()

    print('values', values)
    global baseCoin
    baseCoin = values.get('baseCoin')

    response = {
        'Basecoin': baseCoin
    }
    return jsonify(response, 200)