from mpt import MerklePatriciaTrie
import plyvel
import rlp
import json

class Level2db:
    def __init__(self):
        self.db = plyvel.DB('./testdb', create_if_missing=True)
        self.transaction = {}
        self.block = {}
        self.receipt = {}

    def classify(self):
        with self.db.iterator() as it:
            for k, v in it:
                key = k.decode()
                if key[0] == 'b':
                    self.block[key[1:]] = json.loads(rlp.decode(v).decode())
                elif key[0] == 'r':
                    self.receipt[key[1:]] = json.loads(rlp.decode(v).decode())
                elif key[0] == 't':
                    self.transaction[key[1:]] = json.loads(rlp.decode(v).decode())

    def getBlock(self, index):
        self.classify()
        return self.block[index]

    def getTransaction(self, index):
        self.classify()
        return self.transaction[index]

    def getReceipt(self, index):
        self.classify()
        return self.receipt[index]

    def putBlock(self, index: str, content):
        self.db.put(b'b'+index.encode(), rlp.encode(json.dumps(content)))

    def putTransaction(self, index: str, content):
        self.db.put(b't'+index.encode(), rlp.encode(json.dumps(content)))

    def putReceipt(self, index: str, content):
        self.db.put(b'r'+index.encode(), rlp.encode(json.dumps(content)))


if __name__ == '__main__':
    block1 = {'d': '1', 'c': '2'}
    state = Level2db()
    state.putBlock('1', block1)
    print(state.getBlock('1'))
