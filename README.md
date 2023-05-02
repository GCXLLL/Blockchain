# Blockchain Client Node Program

This project is a blockchain mode client program written in Python 3 based on Flask, following the mechanisms of Ethereum blockchain. I have realized all basic functions such as mining, creating account, creating transactions, inter-node interaction, etc.

## Dependence

All the packets used in this project are listed in requirement.txt.

## Interact with the Blockchain

Since this blockchain system is based on Flask, all functions will be called by http requests.

First of all, you can download a [postman](https://www.postman.com/) for debugger.

Then, you can start the program by creating a directory and node1.py as below.

```python
from app import*

app.run(host='0.0.0.0', port=5000)
```

Start the server by running node1.py. We can use different ports to simulate different nodes, but different directory should be created to separate them.

In addtion, after shutting down the node server, when we can start it once again, all data will be still there.

## Functions

We can use the postman to send http requests to call different functions by instructions below

### Init the node 

As we start to use the blockchain node client program, we should init it to generate the genesis block.

We can directly send a GET request to http://localhost:5000/init

```
[
    "Succeed to init the blockchain",
    200
]
```



### Mine

Mining is an important function to generate new blocks. In my blockchain, Pow algorithm was used and whenever a node generate a new block,  it would broadcast to all its meighbour nodes.

We can directly send a GET request to http://localhost:5000/mine

```
[
    {
        "index": 2,
        "message": "Forged new block.",
        "previous_hash": "5a3db850e56630b55fbe745136fcfd87be6e237e2219c77db88a996d08f86f68",
        "proof": 35293,
        "receiptsRoot": "833656ebc9f9d9b6a24e3110897d47339f650b216c62c7b9a0e2a9249be724ae",
        "stateRoot": "0185a29618fa20866022741e84de2083d122a4f0e4d0543ef8e83e2192531821",
        "transactionRoot": "833656ebc9f9d9b6a24e3110897d47339f650b216c62c7b9a0e2a9249be724ae",
        "transactions": [
            {
                "data": "Mining",
                "hash": "b194a75a2513591164c6be8e502cba1b43080811bd1efd3fbadaa6cdc5e0ed98",
                "recipient": "80f02d34453142a45ec3e117dc5b1f25388f584b",
                "sender": 0,
                "sign": null,
                "value": 100
            }
        ]
    },
    200
]
```



### Show Chain

We can use this function to show the entire chain by sending GET request to http://localhost:5000/chain

```
{
    "chain": [
        {
            "index": 1,
            "previous_hash": 1,
            "proof": 100,
            "receiptsRoot": "56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
            "stateRoot": "8689a41144d805ce6087fedb34654321df0e856a3abed39c8753c5d66784d0ac",
            "timestamp": 1673440248.1338701,
            "transactionRoot": "56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
            "transactions": [
                {
                    "data": 0,
                    "hash": 0,
                    "recipient": "80f02d34453142a45ec3e117dc5b1f25388f584b",
                    "sender": 0,
                    "sign": 0,
                    "value": 100
                }
            ]
        },
        {
            "index": 2,
            "previous_hash": "5a3db850e56630b55fbe745136fcfd87be6e237e2219c77db88a996d08f86f68",
            "proof": 35293,
            "receiptsRoot": "833656ebc9f9d9b6a24e3110897d47339f650b216c62c7b9a0e2a9249be724ae",
            "stateRoot": "0185a29618fa20866022741e84de2083d122a4f0e4d0543ef8e83e2192531821",
            "timestamp": 1673440348.7719,
            "transactionRoot": "833656ebc9f9d9b6a24e3110897d47339f650b216c62c7b9a0e2a9249be724ae",
            "transactions": [
                {
                    "data": "Mining",
                    "hash": "b194a75a2513591164c6be8e502cba1b43080811bd1efd3fbadaa6cdc5e0ed98",
                    "recipient": "80f02d34453142a45ec3e117dc5b1f25388f584b",
                    "sender": 0,
                    "sign": null,
                    "value": 100
                }
            ]
        }
    ],
    "length": 2
}
```



### Create Accounts

We can create a new account by sending GET request to http://localhost:5000/account/create

```
[
    {
        "Account": "72a7fe36670a20dc3b5b4909a83f39cabb94e96c",
        "PrivateKey": "0fd1114468ed5ad287d3e6efeaa1fe23a199ba66ae31aafd76d616b50b1110c4"
    },
    200
]
```

```
[
    {
        "Account": "b706e49b10e1abf7120b75a74421b55140e943f3",
        "PrivateKey": "f97c580adc0fc40110a92c1e64a45149f9ad47496bc84059e983de7a48602125"
    },
    200
]
```

From then on, we have created two accounts. However, a new block should be created to record the accounts, and we need to call mine function again.

```
[
    {
        "index": 3,
        "message": "Forged new block.",
        "previous_hash": "c8e4c2cae8d907903947917a9dc315aa345da7fead08aaf1f3f2d092d3cb7389",
        "proof": 35089,
        "receiptsRoot": "9792e3ea62cea757c01e33779cec779e2685e1b19b01bb7827650669188c4cfb",
        "stateRoot": "be665a1699e10646ebc25e5ed830e1d094c090d771a3b942775db408b4105fd7",
        "transactionRoot": "9792e3ea62cea757c01e33779cec779e2685e1b19b01bb7827650669188c4cfb",
        "transactions": [
            {
                "data": "Creating",
                "hash": "b8c5e0aafe96d9659011d6b80843c64aff8803e6d7a17e287017b5f95382cb36",
                "recipient": "72a7fe36670a20dc3b5b4909a83f39cabb94e96c",
                "sender": 0,
                "sign": null,
                "value": 100
            },
            {
                "data": "Creating",
                "hash": "a5e1f3788d0255b131f99431f44496ff52110976011765fe3475df031aaf4d2c",
                "recipient": "b706e49b10e1abf7120b75a74421b55140e943f3",
                "sender": 0,
                "sign": null,
                "value": 100
            },
            {
                "data": "Mining",
                "hash": "0e170f4ade91469d30eb0b6fe466b34504e4785d8a09ff432ae4e790d30b68e1",
                "recipient": "80f02d34453142a45ec3e117dc5b1f25388f584b",
                "sender": 0,
                "sign": null,
                "value": 100
            }
        ]
    },
    200
]
```

It is clear that these two accounts have been recorded in the block. For future operations, whenever a new account is created, 100 will be sent.



### Look up balance of an account

We can look up the balance of an account by making a POST request to http://localhost:5000/account/getBalance with a body containing essential data. Let's make this call using the cURL:

```http
curl -X POST -H "Content-Type: application/json" -d '{
 "account": "72a7fe36670a20dc3b5b4909a83f39cabb94e96c"
}' "http://localhost:5000/account/getBalance"
```

```
[
    "100",
    200
]
```

It can be found there are 100 in the account.



### Change Basecoin

Basecoin is the account where the award for mining is sent. Whenever a node is inited, a basecoin will be created. We can change it by making a POST request to http://localhost:5000/account/changeBasecoin with a body containing essential data. Let's make this call using the cURL:

```http
curl -X POST -H "Content-Type: application/json" -d '{
 "baseCoin": "72a7fe36670a20dc3b5b4909a83f39cabb94e96c"
}' "http://localhost:5000/account/changeBasecoin"
```



### Create New Transactions

Now, we have an account and we can send money to other account by creating a transaction. Meanwhile, some message can be reacorded in the transaction. It can be created by making a POST request to http://localhost:5000/transaction/new with a body containing essential data. Let's make this call using the cURL:

```http
curl -X POST -H "Content-Type: application/json" -d '{
 "sender": "b706e49b10e1abf7120b75a74421b55140e943f3",
 "recipient": "72a7fe36670a20dc3b5b4909a83f39cabb94e96c",
 "amount": 5,
 "data": "Hello World",
 "sk": "f97c580adc0fc40110a92c1e64a45149f9ad47496bc84059e983de7a48602125"
}' "http://localhost:5000/transaction/new"
```

where sk is the private key which is used to make signature.

```
[
    {
        "message": "Transaction will be added to the Block 4",
        "transaction hash": "710457f6d64ac95d6f5bbb5431e8e526911492f92a9475332bc8d499db87b628"
    },
    200
]
```

Just as creating accounts, we should wait for the generation of a new block. If the 4th block is mined, then we can see that the transaction has been recorded in the block.

```
[
    {
        "index": 4,
        "message": "Forged new block.",
        "previous_hash": "3fed5cf7044413815c3651f8babeef749a668451579964e78ec0f28acdfcb8e9",
        "proof": 119678,
        "receiptsRoot": "054214ed850d3fede9a0b265e61a6345bb09787fe61f8e80231dda700a26afea",
        "stateRoot": "181750860f76b9d94e69d9567a23aa69f4e97c5b2c54f3232a547ae16e75ef4d",
        "transactionRoot": "054214ed850d3fede9a0b265e61a6345bb09787fe61f8e80231dda700a26afea",
        "transactions": [
            {
                "data": "Hello World",
                "hash": "710457f6d64ac95d6f5bbb5431e8e526911492f92a9475332bc8d499db87b628",
                "recipient": "72a7fe36670a20dc3b5b4909a83f39cabb94e96c",
                "sender": "b706e49b10e1abf7120b75a74421b55140e943f3",
                "sign": "9afeb7fd8444febdcaeff856c176364daf806804c712c9e178daad65e2bb2b1028cc0fbcae1065683a8290ebd4c6a4ad07b22a09fbfbffa24ae9ffc4c7cb84e500",
                "value": 10
            },
            {
                "data": "Mining",
                "hash": "314d62326de094f40dff2360772f770a9b74812d53111fb254cda47bffddff51",
                "recipient": "80f02d34453142a45ec3e117dc5b1f25388f584b",
                "sender": 0,
                "sign": null,
                "value": 100
            }
        ]
    },
    200
]
```

We can find that the money of our account decreases by 10, while the other increases by 10.

```
[
    "90",
    200
]
```

```
[
    "110",
    200
]
```



### Look up for Transactions

We can look up for a transaction with its hash by making a POST request to http://localhost:5000/transaction/find with a body containing essential data. Let's make this call using the cURL:

```http
curl -X POST -H "Content-Type: application/json" -d '{
 "hash": "710457f6d64ac95d6f5bbb5431e8e526911492f92a9475332bc8d499db87b628"
}' "http://localhost:5000/transaction/find"
```

The transaction is shown as below

```
[
    {
        "data": "Hello World",
        "hash": "710457f6d64ac95d6f5bbb5431e8e526911492f92a9475332bc8d499db87b628",
        "recipient": "72a7fe36670a20dc3b5b4909a83f39cabb94e96c",
        "sender": "b706e49b10e1abf7120b75a74421b55140e943f3",
        "sign": "9afeb7fd8444febdcaeff856c176364daf806804c712c9e178daad65e2bb2b1028cc0fbcae1065683a8290ebd4c6a4ad07b22a09fbfbffa24ae9ffc4c7cb84e500",
        "value": 10
    },
    200
]
```



### Add Neighbour Nodes 

There are various nodes in blockchain network. We can start another blockchain node client program by creating another directory and node2.py following the methods mentioned above by changing the port number.

```python
from app import*

app.run(host='0.0.0.0', port=5001)
```

We can use one node to add another node as neighbours by making a POST request to http://localhost:5000/nodes/add with a body containing essential data. Let's make this call using the cURL:

```http
curl -X POST -H "Content-Type: application/json" -d '{
 "nodes": ["http://127.0.0.1:5001"]
}' "http://localhost:5000/nodes/add"
```

Then, the node can be successfully added.

```
{
    "all_nodes": [
        "127.0.0.1:5001"
    ],
    "message": "New nodes have been added"
}
```



### Resolve the Conflict

If two nodes' chain are different from each other, we should follow the longest chain principle to avoid conflict. I designed a function to resolve the conflict by making a GET request to http://localhost:5000/nodes/add. SInce the chain is longer than its neighbours, it is authoritative.

```
{
  "message": "Our chain is authoritative."
}
```

Instead, if we resolve the conflict from the other node by making a GET request to http://localhost:5001/nodes/add, its chain will be replaced.

```
{
    "message": "Our chain was replaced.",
    "new_chain": [
        {
            "index": 1,
            "previous_hash": 1,
            "proof": 100,
            "receiptsRoot": "56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
            "stateRoot": "8689a41144d805ce6087fedb34654321df0e856a3abed39c8753c5d66784d0ac",
            "timestamp": 1673440248.1338701,
            "transactionRoot": "56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
            "transactions": [
                {
                    "data": 0,
                    "hash": 0,
                    "recipient": "80f02d34453142a45ec3e117dc5b1f25388f584b",
                    "sender": 0,
                    "sign": 0,
                    "value": 100
                }
            ]
        },
        {
            "index": 2,
            "previous_hash": "5a3db850e56630b55fbe745136fcfd87be6e237e2219c77db88a996d08f86f68",
            "proof": 35293,
            "receiptsRoot": "833656ebc9f9d9b6a24e3110897d47339f650b216c62c7b9a0e2a9249be724ae",
            "stateRoot": "0185a29618fa20866022741e84de2083d122a4f0e4d0543ef8e83e2192531821",
            "timestamp": 1673440348.7719,
            "transactionRoot": "833656ebc9f9d9b6a24e3110897d47339f650b216c62c7b9a0e2a9249be724ae",
            "transactions": [
                {
                    "data": "Mining",
                    "hash": "b194a75a2513591164c6be8e502cba1b43080811bd1efd3fbadaa6cdc5e0ed98",
                    "recipient": "80f02d34453142a45ec3e117dc5b1f25388f584b",
                    "sender": 0,
                    "sign": null,
                    "value": 100
                }
            ]
        },
        {
            "index": 3,
            "previous_hash": "c8e4c2cae8d907903947917a9dc315aa345da7fead08aaf1f3f2d092d3cb7389",
            "proof": 35089,
            "receiptsRoot": "9792e3ea62cea757c01e33779cec779e2685e1b19b01bb7827650669188c4cfb",
            "stateRoot": "be665a1699e10646ebc25e5ed830e1d094c090d771a3b942775db408b4105fd7",
            "timestamp": 1673441117.340822,
            "transactionRoot": "9792e3ea62cea757c01e33779cec779e2685e1b19b01bb7827650669188c4cfb",
            "transactions": [
                {
                    "data": "Creating",
                    "hash": "b8c5e0aafe96d9659011d6b80843c64aff8803e6d7a17e287017b5f95382cb36",
                    "recipient": "72a7fe36670a20dc3b5b4909a83f39cabb94e96c",
                    "sender": 0,
                    "sign": null,
                    "value": 100
                },
                {
                    "data": "Creating",
                    "hash": "a5e1f3788d0255b131f99431f44496ff52110976011765fe3475df031aaf4d2c",
                    "recipient": "b706e49b10e1abf7120b75a74421b55140e943f3",
                    "sender": 0,
                    "sign": null,
                    "value": 100
                },
                {
                    "data": "Mining",
                    "hash": "0e170f4ade91469d30eb0b6fe466b34504e4785d8a09ff432ae4e790d30b68e1",
                    "recipient": "80f02d34453142a45ec3e117dc5b1f25388f584b",
                    "sender": 0,
                    "sign": null,
                    "value": 100
                }
            ]
        },
        {
            "index": 4,
            "previous_hash": "3fed5cf7044413815c3651f8babeef749a668451579964e78ec0f28acdfcb8e9",
            "proof": 119678,
            "receiptsRoot": "054214ed850d3fede9a0b265e61a6345bb09787fe61f8e80231dda700a26afea",
            "stateRoot": "181750860f76b9d94e69d9567a23aa69f4e97c5b2c54f3232a547ae16e75ef4d",
            "timestamp": 1673442517.4400344,
            "transactionRoot": "054214ed850d3fede9a0b265e61a6345bb09787fe61f8e80231dda700a26afea",
            "transactions": [
                {
                    "data": "Hello World",
                    "hash": "710457f6d64ac95d6f5bbb5431e8e526911492f92a9475332bc8d499db87b628",
                    "recipient": "72a7fe36670a20dc3b5b4909a83f39cabb94e96c",
                    "sender": "b706e49b10e1abf7120b75a74421b55140e943f3",
                    "sign": "9afeb7fd8444febdcaeff856c176364daf806804c712c9e178daad65e2bb2b1028cc0fbcae1065683a8290ebd4c6a4ad07b22a09fbfbffa24ae9ffc4c7cb84e500",
                    "value": 10
                },
                {
                    "data": "Mining",
                    "hash": "314d62326de094f40dff2360772f770a9b74812d53111fb254cda47bffddff51",
                    "recipient": "80f02d34453142a45ec3e117dc5b1f25388f584b",
                    "sender": 0,
                    "sign": null,
                    "value": 100
                }
            ]
        }
    ]
}
```

It is clear that the new chain is as the same as the chain we created before for the other node.



### MIne when Synchronized

SInce we have add the neighours for two nodes and resolve the conflict, they are now synchronized. If there are a new block generated by one of the nodes, the other will reveive the broadcast and update its chain after verifying the coming block.

We firstly mine in one node by sending the Post request to http://localhost:5001/mine, the fifth block will be generated.

```
[
    {
        "index": 5,
        "message": "Forged new block.",
        "previous_hash": "4af8905a25dd8fe39c1c233b372cd3463e7b28cbc5d6a70993b6d82a7d11763e",
        "proof": 146502,
        "receiptsRoot": "4f3ebf274afc19d57457e0db5dfe34812f3d5e1927cf562f5475d26cd32fa4f8",
        "stateRoot": "7d90cca2e1b706d478cd15923ee49ec99e3ce0aa37a89ea1e9fb9f6370f47b70",
        "transactionRoot": "4f3ebf274afc19d57457e0db5dfe34812f3d5e1927cf562f5475d26cd32fa4f8",
        "transactions": [
            {
                "data": "Mining",
                "hash": "422129ac4948f7ac9f3840e5ab7abcf29765c5c8d4c98ab1deab9002492a0b0b",
                "recipient": "91f0f034b1be75b60bb2c4e18e46cfc836c13fc1",
                "sender": 0,
                "sign": null,
                "value": 100
            }
        ]
    },
    200
]
```

Then, we can show the chain of the other node, and the fifth block is the same.

```
{
    "chain": [
        {
            "index": 1,
            "previous_hash": 1,
            "proof": 100,
            "receiptsRoot": "56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
            "stateRoot": "8689a41144d805ce6087fedb34654321df0e856a3abed39c8753c5d66784d0ac",
            "timestamp": 1673440248.1338701,
            "transactionRoot": "56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
            "transactions": [
                {
                    "data": 0,
                    "hash": 0,
                    "recipient": "80f02d34453142a45ec3e117dc5b1f25388f584b",
                    "sender": 0,
                    "sign": 0,
                    "value": 100
                }
            ]
        },
        {
            "index": 2,
            "previous_hash": "5a3db850e56630b55fbe745136fcfd87be6e237e2219c77db88a996d08f86f68",
            "proof": 35293,
            "receiptsRoot": "833656ebc9f9d9b6a24e3110897d47339f650b216c62c7b9a0e2a9249be724ae",
            "stateRoot": "0185a29618fa20866022741e84de2083d122a4f0e4d0543ef8e83e2192531821",
            "timestamp": 1673440348.7719,
            "transactionRoot": "833656ebc9f9d9b6a24e3110897d47339f650b216c62c7b9a0e2a9249be724ae",
            "transactions": [
                {
                    "data": "Mining",
                    "hash": "b194a75a2513591164c6be8e502cba1b43080811bd1efd3fbadaa6cdc5e0ed98",
                    "recipient": "80f02d34453142a45ec3e117dc5b1f25388f584b",
                    "sender": 0,
                    "sign": null,
                    "value": 100
                }
            ]
        },
        {
            "index": 3,
            "previous_hash": "c8e4c2cae8d907903947917a9dc315aa345da7fead08aaf1f3f2d092d3cb7389",
            "proof": 35089,
            "receiptsRoot": "9792e3ea62cea757c01e33779cec779e2685e1b19b01bb7827650669188c4cfb",
            "stateRoot": "be665a1699e10646ebc25e5ed830e1d094c090d771a3b942775db408b4105fd7",
            "timestamp": 1673441117.340822,
            "transactionRoot": "9792e3ea62cea757c01e33779cec779e2685e1b19b01bb7827650669188c4cfb",
            "transactions": [
                {
                    "data": "Creating",
                    "hash": "b8c5e0aafe96d9659011d6b80843c64aff8803e6d7a17e287017b5f95382cb36",
                    "recipient": "72a7fe36670a20dc3b5b4909a83f39cabb94e96c",
                    "sender": 0,
                    "sign": null,
                    "value": 100
                },
                {
                    "data": "Creating",
                    "hash": "a5e1f3788d0255b131f99431f44496ff52110976011765fe3475df031aaf4d2c",
                    "recipient": "b706e49b10e1abf7120b75a74421b55140e943f3",
                    "sender": 0,
                    "sign": null,
                    "value": 100
                },
                {
                    "data": "Mining",
                    "hash": "0e170f4ade91469d30eb0b6fe466b34504e4785d8a09ff432ae4e790d30b68e1",
                    "recipient": "80f02d34453142a45ec3e117dc5b1f25388f584b",
                    "sender": 0,
                    "sign": null,
                    "value": 100
                }
            ]
        },
        {
            "index": 4,
            "previous_hash": "3fed5cf7044413815c3651f8babeef749a668451579964e78ec0f28acdfcb8e9",
            "proof": 119678,
            "receiptsRoot": "054214ed850d3fede9a0b265e61a6345bb09787fe61f8e80231dda700a26afea",
            "stateRoot": "181750860f76b9d94e69d9567a23aa69f4e97c5b2c54f3232a547ae16e75ef4d",
            "timestamp": 1673442517.4400344,
            "transactionRoot": "054214ed850d3fede9a0b265e61a6345bb09787fe61f8e80231dda700a26afea",
            "transactions": [
                {
                    "data": "Hello World",
                    "hash": "710457f6d64ac95d6f5bbb5431e8e526911492f92a9475332bc8d499db87b628",
                    "recipient": "72a7fe36670a20dc3b5b4909a83f39cabb94e96c",
                    "sender": "b706e49b10e1abf7120b75a74421b55140e943f3",
                    "sign": "9afeb7fd8444febdcaeff856c176364daf806804c712c9e178daad65e2bb2b1028cc0fbcae1065683a8290ebd4c6a4ad07b22a09fbfbffa24ae9ffc4c7cb84e500",
                    "value": 10
                },
                {
                    "data": "Mining",
                    "hash": "314d62326de094f40dff2360772f770a9b74812d53111fb254cda47bffddff51",
                    "recipient": "80f02d34453142a45ec3e117dc5b1f25388f584b",
                    "sender": 0,
                    "sign": null,
                    "value": 100
                }
            ]
        },
        {
            "index": 5,
            "previous_hash": "4af8905a25dd8fe39c1c233b372cd3463e7b28cbc5d6a70993b6d82a7d11763e",
            "proof": 146502,
            "receiptsRoot": "4f3ebf274afc19d57457e0db5dfe34812f3d5e1927cf562f5475d26cd32fa4f8",
            "stateRoot": "7d90cca2e1b706d478cd15923ee49ec99e3ce0aa37a89ea1e9fb9f6370f47b70",
            "timestamp": 1673453535.2584958,
            "transactionRoot": "4f3ebf274afc19d57457e0db5dfe34812f3d5e1927cf562f5475d26cd32fa4f8",
            "transactions": [
                {
                    "data": "Mining",
                    "hash": "422129ac4948f7ac9f3840e5ab7abcf29765c5c8d4c98ab1deab9002492a0b0b",
                    "recipient": "91f0f034b1be75b60bb2c4e18e46cfc836c13fc1",
                    "sender": 0,
                    "sign": null,
                    "value": 100
                }
            ]
        }
    ],
    "length": 5
}
```

