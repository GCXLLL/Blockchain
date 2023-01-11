import binascii
import hashlib
import json
import os
import shutil

import requests
from time import time
from urllib.parse import urlparse
from ecc import*
from level1db import Level1db
from level2db import Level2db
from utils import get_basecoin


class BlockChain(object):
    """ Main BlockChain class """
    def __init__(self):
        level2 = Level2db()
        self.chain = level2.get_all_blocks()
        self.current_transactions = []
        self.nodes = set()
        # read the storage
        try:
            with open("data/nodes.txt", "r") as f:
                for line in f.readlines():
                    self.nodes.add(line.strip('\n'))
        except:
            # if not exist, pass
            pass
        level2.close()

    def init_genesis(self, account):
        # find init world state
        trie = Level1db()
        # create the transaction
        trie.update(account.encode(), b'100')
        stateRoot = trie.root().hex()
        trie.close()
        trans = {
            'sender': 0,
            'recipient': account,
            'value': 100,
            'data': 0,
            'hash': 0,
            'sign': 0
        }
        # create the genesis block
        self.new_block(previous_hash=1, stateRoot=stateRoot, proof=100, trans=[trans])


    @staticmethod
    def hash(block):
        # hashes a block
        # also make sure that the transactions are ordered otherwise we will have insonsistent hashes!
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def new_block(self, proof, stateRoot, previous_hash=None, timestamp=None, trans=None):
        if trans is None:
            transaction = self.current_transactions
        else:
            transaction = trans

        # put transactions in level2db
        level2 = Level2db()
        for tran in transaction:
            tran_hash = tran['hash']
            if tran_hash != 0:  # avoid transaction in genesis block
                level2.putTx2trie(tran_hash, tran)
                level2.putTransaction(tran_hash, tran)

        # get transaction root
        tranRoot = level2.get_tran_hash()

        rxRoot = tranRoot  # not consider tranRoot currently

        # creates a new block in the blockchain
        block = {
            'index': len(self.chain)+1,
            'timestamp': timestamp or time(),
            'transactions': transaction,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'receiptsRoot': rxRoot,
            'transactionRoot': tranRoot,
            'stateRoot': stateRoot
        }

        # check if received block
        if trans is None:
            # local generate block
            # reset the current list of transactions
            self.current_transactions = []

        # add to memory
        self.chain.append(block)

        # store in leveldb
        level2.putBlock(str(len(self.chain)), block)
        level2.close()

        return block

    @property
    def last_block(self):
        # returns last block in the chain
        return self.chain[-1]

    def store_nodes(self):
        # listen the change of the nodes
        with open("data/nodes.txt", "a") as f:
            for node in self.nodes:
                f.write(node + '\n')
                print('succeed to write: ', node)

    def new_transaction(self, sender, recipient, amount, data, nonce, sk=None):
        # get hash value of transaction
        baseTran = {
            'sender': sender,
            'recipient': recipient,
            'value': amount,
            'data': data,
            'nonce': nonce  # avoid hash conflict
        }
        hash = self.hash(baseTran)
        # identify the sender
        if sender == 0:
            sign = None
        else:
            sign = sign2hex(hex2sk(sk).sign_msg(hash.encode()))
        # adds a new transaction into the list of transactions
        # these transactions go into the next mined block
        self.current_transactions.append({
            'data': data,
            'hash': hash,
            'recipient': recipient,
            'sender': sender,
            'sign': sign,
            'value': amount
        })
        return int(self.last_block['index'])+1, hash

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
        self.store_nodes()

    def full_chain(self):
        # xxx returns the full chain and a number of blocks
        pass

    def register_miner_node(self, address):
        # add on the new miner node onto the list of nodes
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        self.store_nodes()
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

    def check_chain(self, chain):
        '''
        This function is to check whether all blocks of new chain are valid
        :param
        chain: list
        :return:
        flag: bool
        '''
        # deal with genesis block
        account = chain[0]['transactions'][0]['recipient']
        # init world state
        trie = Level1db(path='./data/pre1')
        trie.update(account.encode(), b'100')
        trie.close()
        for n in range(1, len(chain)):
            msg, flag = self.valid_come_block(
                block=chain[n],
                last_block=chain[n-1],
                path1='./data/pre1',
                path2='./data/pre2')
            if not flag:
                print('block {} is wrong'.format(n+1))
                print(msg)
                shutil.rmtree('./data/pre1')
                shutil.rmtree('./data/pre2')
                return False
        return True

    def resolve_conflicts(self):
        '''
        this is our Consensus Algorithm, it resolves conflicts by replacing
        our chain with the longest one in the network.
        '''
        # essential variables
        addChain = None  # new valid longer chain
        extension = None  # identify how to replace the new chain
        # formal leveldb to replace existing leveldb
        os.mkdir('./data/for1')
        os.mkdir('./data/for2')

        neighbours = self.nodes

        # we are only looking for the chains longer than ours
        current_length = len(self.chain)

        # grab and verify chains from all the nodes in our network
        for node in neighbours:
            # we utilize our own api to construct the list of chains :)
            response = requests.get(f'http://{node}/chain_request')

            if response.status_code == 200:

                length = response.json()['length']
                chain = response.json()['chain']

                # check if the chain is longer and whether the chain is valid
                if length > current_length and self.valid_chain(chain):
                    newChain = []
                    # check the block
                    # identify if the new chain the extension of present chain
                    for n in range(current_length-1, -1, -1):
                        block = chain[n]
                        if block['previous_hash'] == self.chain[n]['previous_hash']:
                            break
                    if n != 0:
                        # update the difference
                        for i in range(n, length):
                            msg, flag = self.valid_come_block(chain[i], chain[i-1])
                            if flag:
                                newChain.append(block)
                            else:
                                newChain = None
                                break
                        # if valid, add blocks to addChain and change current_length
                        if newChain:
                            current_length = length
                            addChain = list(newChain)  # change address of list
                            extension = True
                    else:
                        # make a back-up to check
                        if self.check_chain(chain):
                            # take place the entire chain
                            # delete last time directory
                            shutil.rmtree('./data/for1')
                            shutil.rmtree('./data/for2')
                            os.rename('./data/pre1', './data/for1')
                            os.rename('./data/pre2', './data/for2')
                            current_length = length
                            addChain = list(chain)
                            extension = False

        # add new blocks in our chain if we discover a new longer valid chain
        if addChain:
            if extension:
                for block in addChain:
                    # add block to local
                    self.new_block(
                        proof=block['proof'],
                        stateRoot=block['stateRoot'],
                        previous_hash=block['previous_hash'],
                        timestamp=block['timestamp'],
                        trans=block['transactions']
                    )
                return True
            else:
                # clear blockchain memory
                self.chain = []
                # change the storage
                shutil.rmtree('./data/level1')
                shutil.rmtree('./data/level2')
                os.rename('./data/for1', './data/level1')
                os.rename('./data/for2', './data/level2')
                # add chain to local
                for block in addChain:
                    self.new_block(
                        proof=block['proof'],
                        stateRoot=block['stateRoot'],
                        previous_hash=block['previous_hash'],
                        timestamp=block['timestamp'],
                        trans=block['transactions']
                    )
                return True
        # Our chain is the longest
        shutil.rmtree('./data/for1')
        shutil.rmtree('./data/for2')
        return False

    def valid_transaction(self):
        for tran in self.current_transactions:
            if tran['sender'] == 0:
                # reward for miner
                pass
            elif tran['sender'] == \
                    getAddress(hex2sign(tran['sign']).recover_public_key_from_msg(tran['hash'].encode()).to_hex()):
                # verify the signature
                pass
            else:
                # delete the invalid transaction
                self.current_transactions.remove(tran)
        return True

    def work_before_mine(self):
        '''
        change the world state by transactions
        get state root
        get transaction root

        :returns:
        state root: str,
        flag: bool
        '''
        # find the last world state
        last_block = self.last_block
        last_stateRoot = last_block['stateRoot']
        print(last_stateRoot)
        root = binascii.unhexlify(last_stateRoot)
        # get the world state MPT
        trie = Level1db(root=root)
        # update world state by transactions
        for tran in self.current_transactions:
            sender = tran['sender']
            recipient = tran['recipient']
            value = tran['value']
            # check sender
            if sender != 0:
                # not the reward for miner
                try:
                    balance_sender = int(trie.get(sender.encode()).decode())
                except:
                    # sender not exist
                    trie.close()
                    return '', False
                if value <= balance_sender:
                    balance_sender = balance_sender - value
                else:
                    # no enough balance
                    trie.close()
                    return '', False
            else:
                sender = str(sender)
                balance_sender = 0
            # update the balance of sender
            print(sender.encode())
            print(str(balance_sender).encode())
            trie.update(sender.encode(), str(balance_sender).encode())
            try:
                balance_recipient = int(trie.get(recipient.encode()).decode())
                balance_recipient = balance_recipient + value
            except:
                balance_recipient = value
            # update the balance of recipient
            trie.update(recipient.encode(), str(balance_recipient).encode())

        # get the present state root and transaction root
        stateRoot = trie.root().hex()
        trie.close()
        return stateRoot, True

    def get_transaction(self, tranHash):
        '''
        get transaction by hash

        :param tranHash: str
        :returns: tran: dict, flag: bool
        '''

        level2 = Level2db()
        try:
            tran = level2.getTransaction(tranHash)
            flag = True
        except:
            tran = {'Warning': 'No transaction found!'}
            flag = False
        level2.close()
        return tran, flag

    def get_balance(self, account):
        '''
        get the balance of the given account

        :param account: str
        :returns: flag: bool, balance: str
        '''
        # find the last world state
        last_block = self.last_block
        last_stateRoot = last_block['stateRoot']
        root = binascii.unhexlify(last_stateRoot)
        # get the world state MPT
        state = Level1db(root=root)
        try:
            balance = state.get(account.encode()).decode()
            flag = True
        except:
            balance = 'Account not exist!'
            flag = False
        state.close()
        return balance, flag

    def valid_come_block(self, block, last_block=None, path1=None, path2=None):
        '''
        check whether the received block is valid

        :param block: dict
        :param last_block: dict
        :param path1: str
        :param path2: str
        :return: message: str
        :return: flag: bool
        '''

        if last_block is None:
            # for one received block
            last_block = self.last_block
            # check the index
            if block['index'] != len(self.chain)+1:
                return 'Wrong Index', False

            # check previous hash
            if block['previous_hash'] != self.hash(self.chain[-1]):
                return 'Wrong Previous_hash', False

            # check pow
            if not self.validate_proof(last_block['proof'], block['proof']):
                return 'Wrong Proof of Work', False

        # find the last world state
        print(last_block['stateRoot'])
        last_stateRoot = last_block['stateRoot']
        root = binascii.unhexlify(last_stateRoot)
        # get the world state MPT
        if path1 is None:
            trie = Level1db(root=root)
        else:
            trie = Level1db(root=root, path=path1)
        # connect to level2db
        if path2 is None:
            level2 = Level2db()
        else:
            level2 = Level2db(path=path2)

        # check transactions and world state
        for tran in block['transactions']:
            sender = tran['sender']
            recipient = tran['recipient']
            value = tran['value']
            tran_hash = tran['hash']
            if sender != 0:
                # not the reward for miner
                if not tran['sender'] == \
                       getAddress(hex2sign(tran['sign']).recover_public_key_from_msg(tran['hash'].encode()).to_hex()):
                    # check the signature
                    trie.close()
                    level2.close()
                    return 'Wrong Transaction: Wrong signature', False
                try:
                    balance_sender = int(trie.get(sender.encode()).decode())
                except:
                    # sender not exist
                    trie.close()
                    level2.close()
                    return 'Wrong Transaction: Sender not exist', False
                if value <= balance_sender:
                    balance_sender = balance_sender - value
                else:
                    # no enough balance
                    trie.close()
                    level2.close()
                    return 'Wrong Transaction: No enough balance', False
            else:
                sender = str(sender)
                balance_sender = 0
            # update the balance of sender
            trie.update(sender.encode(), str(balance_sender).encode())
            try:
                balance_recipient = int(trie.get(recipient.encode()).decode())
                balance_recipient = balance_recipient + value
            except:
                balance_recipient = value
            # update the balance of recipient
            trie.update(recipient.encode(), str(balance_recipient).encode())
            # add Tx to transaction trie
            level2.putTx2trie(tran_hash, tran)

        # get the present state root and transaction root
        stateRoot = trie.root().hex()
        transactionRoot = level2.get_tran_hash()
        trie.close()
        level2.close()

        # check the state root and transaction root
        if stateRoot != block['stateRoot']:
            return 'Wrong State Root', False

        if transactionRoot != block['transactionRoot']:
            print(transactionRoot, ' & ', block['transactionRoot'])
            return 'Wrong Transaction Root', False

        return 'Valid Block', True

    def broadcast_block(self, block):
        neighbours = self.nodes
        for node in neighbours:
            response = requests.post(f'http://{node}/nodes/receiveBlock', json=block)


if __name__ == '__main__':
    print(get_basecoin())



