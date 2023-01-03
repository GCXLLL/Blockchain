from level1db import Level1db
import binascii

from mpt import MerklePatriciaTrie
# old_trie = Level1db()
# for n in range(100):
#     value = f'df{n}'
#     old_trie.update(value.encode(), b'ddd')
#
# print(old_trie.root().hex())
# root = old_trie.root()

# root = binascii.unhexlify('1f877b48a1e60d54a41747e5c674a6ced40353480c5ad3fcbee94f8ea3322fac')
# print(root)
# # root = binascii.unhexlify('ca83206464856464646664')
# # print(root)
# trie = Level1db(root=root)
#
# for n in range(10):
#     value = f'df{n}'
#     print(trie.get(value.encode()))
# sender = str(0)
# trie.update(b'dd', b'dddfd')
# print(trie.root().hex())


# old_root = trie.root()
# old_root_hash = trie.root_hash()
#
# print("Root is {}".format(old_root))
# print("Root hash is {}".format(old_root_hash.hex()))

def create_file(string):
    with open('./test', 'w') as f:
        f.write(string)


with open("test/node1/data/baseCoin.txt", "r") as f:
    print(f.read())