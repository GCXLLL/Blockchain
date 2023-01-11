# from ecies.utils import generate_eth_key, generate_key, hex2prv
from coincurve.utils import get_valid_secret
from ecies import encrypt, decrypt
import hashlib
from eth_keys import keys


def generate_sk():
    return keys.PrivateKey(get_valid_secret())


def getAddress(pk_hex):
    '''Change publickey to blockchain address'''
    return hashlib.sha256(pk_hex.encode()).hexdigest()[24:]


def sk2hex(sk):
    return sk.to_hex()[2:]


def hex2sk(sk_hex):
    return keys.PrivateKey(bytes.fromhex(sk_hex))


def sign2hex(sign):
    return sign.to_hex()[2:]


def hex2sign(sign_hex):
    return keys.Signature(bytes.fromhex(sign_hex))


if __name__ == '__main__':
    eth_k = generate_sk()
    print(bytes.fromhex(get_valid_secret().hex()))
    print(type(eth_k))
    sk_hex = sk2hex(eth_k)
    print('Privatekey: ', sk_hex)
    sk = hex2sk(sk_hex)
    print(type(sk))

    pk = eth_k.public_key
    pk_hex = pk.to_hex()
    print('Publickey: ', pk_hex)

    '''Sign and verify'''
    data = b'this is a test'
    data1 = b'this is a test'
    sign = eth_k.sign_msg(data)
    sign_hex = sign2hex(sign)
    print(sign_hex)
    sign_new = hex2sign(sign_hex)

    print(type(sign_new))
    print(sign_new.recover_public_key_from_msg(data))
    # print(eth_k.sign_msg(data).verify_msg(data1, eth_k.public_key))

    # '''Encryption'''
    # # mtext = encrypt(sk_hex, data)
    # # print(mtext)
    # # ptext = decrypt(pk_hex, mtext)
    # # print(ptext)
    # sign = sk.sign_msg(data)
    #
    # all = {'sign': sign}
    # print(all)
    # print(getAddress(pk_hex) == getAddress(all['sign'].recover_public_key_from_msg(data).to_hex()))
