import os
import shutil

from level1db import Level1db
import binascii

from level2db import Level2db
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

level = Level2db(path='./test1')
tran = {
            'data': 'Mining',
            'hash': '3bb275e6539a41baa866a6ff9d304abc8e200ac8c97970c5e3f7ff0baf9f90b0',
            'recipient': 'd601f6d2df1abc6724ffaf4a0aafd759316d2493',
            'sender': 0,
            'sign': None,
            'value': 100
}
level.putTx2trie('3bb275e6539a41baa866a6ff9d304abc8e200ac8c97970c5e3f7ff0baf9f90b0', tran)
print(level.get_tran_hash())
level.close()

