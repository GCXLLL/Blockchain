from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt
import hashlib

def getAddress(pk_hex):
    '''Change publickey to blockchain address'''
    return hashlib.sha256(pk_hex.encode()).hexdigest()[24:]

if __name__ == '__main__':
    eth_k = generate_eth_key()
    sk_hex = eth_k.to_hex()
    print('Privatekey: ', sk_hex)
    pk = eth_k.public_key
    pk_hex = pk.to_hex()
    print('Publickey: ', pk_hex)

    '''Sign and verify'''
    data = b'this is a test'
    data1 = b'this is a test'
    print(eth_k.sign_msg(data).recover_public_key_from_msg(data))
    # print(eth_k.sign_msg(data).verify_msg(data1, eth_k.public_key))

    '''Encryption'''
    # mtext = encrypt(sk_hex, data)
    # print(mtext)
    # ptext = decrypt(pk_hex, mtext)
    # print(ptext)

    print(getAddress(pk_hex) == getAddress(eth_k.sign_msg(data).recover_public_key_from_msg(data).to_hex()))
