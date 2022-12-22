import binascii
import hashlib
import json
import requests
from time import time
from urllib.parse import urlparse
from ecc import*
from level1db import Level1db


class BlockChain(object):
    """ Main BlockChain class """
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        # create the genesis block
        self.new_block(previous_hash=1, proof=100)

    @staticmethod
    def hash(block):
        # hashes a block
        # also make sure that the transactions are ordered otherwise we will have insonsistent hashes!
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def new_block(self, proof, rxRoot, tranRoot, stateRoot, previous_hash=None):
        # creates a new block in the blockchain
        block = {
            'index': len(self.chain)+1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'receiptsRoot': rxRoot,
            'transactionRoot': tranRoot,
            'stateRoot': stateRoot
        }

        # reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    @property
    def last_block(self):
        # returns last block in the chain
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount, data, nonce, sk=None):
        # get hash value of transaction
        baseTran = {
            'sender': sender,
            'recipient': recipient,
            'value': amount,
            'data': data,
            'nonce': nonce
        }
        hash = self.hash(baseTran)
        # adds a new transaction into the list of transactions
        # these transactions go into the next mined block
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'value': amount,
            'data': data,
            'hash': hash,
            'sign': sk.sign_msg(hash.encode())
        })
        return int(self.last_block['index'])+1

    def proof_of_work(self, last_proof):
        # simple proof of work algorithm
        # find a number p' such as hash(pp') containing leading 4 zeros where p is the previous p'
        # p is the previous proof and p' is the new proof
        proof = 0
        while self.validate_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def validate_proof(last_proof, proof):
        # validates the proof: does hash(last_proof, proof) contain 4 leading zeroes?
        operation = f'{last_proof}{proof}'.encode()
        hash_operation = hashlib.sha256(operation).hexdigest()
        return hash_operation[:4] == "0000"

    def register_node(self, address):
        # add a new node to the list of nodes
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def full_chain(self):
        # xxx returns the full chain and a number of blocks
        pass

    def register_miner_node(self, address):
        # add on the new miner node onto the list of nodes
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        return

    def valid_chain(self, chain):

        # determine if a given blockchain is valid
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False
            # check that the proof of work is correct
            if not self.validate_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        # this is our Consensus Algorithm, it resolves conflicts by replacing
        # our chain with the longest one in the network.

        neighbours = self.nodes
        new_chain = None

        # we are only looking for the chains longer than ours
        max_length = len(self.chain)
        print('length of this chain', max_length)

        # grab and verify chains from all the nodes in our network
        for node in neighbours:
            print('in loop')
            print(f'http://{node}/chain_request')
            # we utilize our own api to construct the list of chains :)
            response = requests.get(f'http://{node}/chain_request')

            if response.status_code == 200:

                length = response.json()['length']
                chain = response.json()['chain']

                # check if the chain is longer and whether the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # replace our chain if we discover a new longer valid chain
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def valid_transaction(self):
        for tran in self.current_transactions:
            if tran['sender'] == 0:
                # reward for miner
                pass
            elif tran['sender'] == getAddress(tran['sign'].recover_public_key_from_msg(tran['hash'].encode()).to_hex()):
                # verify the signature
                pass
            else:
                # delete the invalid transaction
                self.current_transactions.remove(tran)
        return True

    def get_root_hash(self):
        '''
        change the world state by transactions
        get state root
        get transaction root
        :return:
        state root: str
        transaction root: str
        flag: bool
        '''
        # find the last world state
        last_block = self.last_block()
        last_stateRoot = last_block['stateRoot']
        root = binascii.unhexlify(last_stateRoot)
        # get the world state MPT
        trie = Level1db(root=root)
        # update world state by transactions
        for tran in self.current_transactions:
            sender = tran['sender']
            recipient = tran['recipient']
            value = tran['value']
            tran_hash = tran['hash']
            # check sender
            if sender != 0:
                # not the reward for miner
                try:
                    balance_sender = int(trie.get(sender.encode()).decode())
                except:
                    # sender not exist
                    return '', '', False
                if value <= balance_sender:
                    balance_sender = balance_sender - value
                else:
                    # no enough balance
                    return '', '', False
            # update the balance of sender
            trie.update(sender.encode(), str(balance_sender).encode())
            try:
                balance_recipient = int(trie.get(recipient.encode()).decode())
                balance_recipient = balance_recipient + value
            except:
                balance_recipient = value
            # update the balance of recipient
            trie.update(recipient.encode(), str(balance_recipient).encode())

            # put transactions in level2db

        # get the present state root
        stateRoot = trie.root().hex()


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)