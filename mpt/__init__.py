# -*- coding: utf-8 -*-
"""
    mpt
    ~~~~~
    Python implementation of Merkle Patricia Trie.

    :copyright: © 2019 by Igor Aleksanov.

    :license: MIT, see LICENSE for more details.
"""

__version__ = '0.1.0'


from .mpt import MerklePatriciaTrie
from .hash import keccak_hash
from .nibble_path import NibblePath
from .node import Node

name = "mpt"



