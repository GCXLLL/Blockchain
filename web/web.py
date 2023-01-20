import hashlib
import os

import requests
from flask import *

from utils import *

# from flask_bootstrap import Bootstrap4

app = Flask(__name__, static_folder='./static')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
# bootstrap = Bootstrap4(app)

chain = None
current_node = '127.0.0.1:5000'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/notarization')
def notarization():
    return render_template('notarization.html')


@app.route('/chain')
def chain():
    global current_node
    try:
        response = requests.get(f'http://{current_node}/chain_request')
    except:
        return render_template('empty_page.html')
    hash = []
    timestamp = []
    tran = []
    if response.status_code == 200:
        length = response.json()['length']
        global chain
        chain = response.json()['chain']

        for block in chain:
            hash.append(hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest())
            timestamp.append(timestamp2time(block['timestamp']))
            tran.append(len(block['transactions']))
        show_chain(length=length, hash=hash, timestamp=timestamp, tran=tran)
        return render_template('chain.html')
    else:
        return render_template('empty_page.html')


@app.route('/management')
def management():
    global current_node
    if session.get('pswd'):

        response = requests.get(f'http://{current_node}/neighbour_request')

        kwargs = {
            "node": current_node,
            "neighbours": response.json()['neighbours']
        }
        return render_template('management.html', **kwargs)
    else:
        pswd = None
        pswd = request.args.get("password")
        if pswd:
            print(pswd)
            if pswd == 'chenxiaoguo':
                session['pswd'] = pswd
                response = requests.get(f'http://{current_node}/neighbour_request')

                kwargs = {
                    "node": current_node,
                    "neighbours": response.json()['neighbours']
                }
                return render_template('management.html', **kwargs)
        print('no pswd')
        return render_template('management_login.html')


@app.route('/getBlock')
def get_block():
    index = request.args.get("index")
    print(index)
    if chain:
        show_block(block=chain[int(index)-1])
    return render_template('block.html')


@app.route('/changeNode', methods=['GET'])
def change_node():
    node = request.args.get("node")
    print(node)
    if node:
        global current_node
        current_node = node
        kwargs = {
            "node": current_node
        }
    return render_template('management.html', **kwargs)


@app.route('/addNode', methods=['GET'])
def add_node():
    node = request.args.get("node")
    print(node)
    if node:
        nodes = {'nodes': node}
        print(nodes)
        global current_node
        response = requests.post(f'http://{current_node}/nodes/add', json=nodes)
        if response.status_code == 200:
            kwargs = {
                "add": json.loads(response.content)['new_node'] + ' has been added'
            }
            return render_template('management.html', **kwargs)
    kwargs = {
        "add": 'Fail to add'
    }
    return render_template('management.html', **kwargs)


@app.route('/changeBasecoin', methods=['GET'])
def change_basecoin():
    node = request.args.get("node")
    print(node)
    if node:
        nodes = {'baseCoin': node}
        global current_node
        response = requests.post(f'http://{current_node}/account/changeBasecoin', json=nodes)
        if response.status_code == 200:
            kwargs = {
                "baseCoin": json.loads(response.content)['BaseCoin']
            }
            return render_template('management.html', **kwargs)
    kwargs = {
        "baseCoin": 'Fail to change'
    }
    return render_template('management.html', **kwargs)


@app.route('/resolve', methods=['GET'])
def resolve_conflict():
    global current_node
    response = requests.get(f'http://{current_node}/nodes/resolve')
    if response.status_code == 200:
        kwargs = {
            "resolve": json.loads(response.content)['message']
        }
        return render_template('management.html', **kwargs)
    kwargs = {
        "resolve": json.loads(response.content)['message']
    }
    return render_template('management.html', **kwargs)


@app.route('/check_balance')
def check_balance():
    node = request.args.get("add")
    print(node)
    nodes = {'account': node}
    global current_node
    try:
        response = requests.post(f'http://{current_node}/account/getBalance', json=nodes)
    except:
        kwargs = {
            "balance": 'Fail to connect to blockchain'
        }
        return render_template('account.html', **kwargs)
    if response.status_code == 200:
        kwargs = {
            "balance": json.loads(response.content)
        }

    elif response.status_code == 500:
        kwargs = {
            "balance": json.loads(response.content)
        }
    else:
        kwargs = {
            "balance": 'Fail to connect to blockchain'
        }
    return render_template('account.html', **kwargs)


@app.route('/create')
def create():
    global current_node
    try:
        response = requests.get(f'http://{current_node}/account/create')
    except:
        kwargs = {
            "address": None,
            "sk": None,
            "warn": 'Fail to connect to Blockchain'
        }
        return render_template('account.html', **kwargs)
    if response.status_code == 200:
        kwargs = {
            "address": response.json()['Account'],
            "sk": response.json()['PrivateKey'],
            "warn": 'Your account is invalid until next block generated!'
        }
    else:
        kwargs = {
            "address": None,
            "sk": None,
            "warn": 'Fail to connect to Blockchain'
        }
    return render_template('account.html', **kwargs)


@app.route('/new_trans')
def new_trans():
    nodes = {
        'sender': request.args.get("sender"),
         'recipient': request.args.get("recipient"),
         'amount': request.args.get("amount"),
         'data': request.args.get("data"),
         'sk': request.args.get("sk")
             }
    global current_node
    try:
        response = requests.post(f'http://{current_node}/transaction/new', json=nodes)
    except:
        kwargs = {
            "new": 'Fail to connect to blockchain'
        }
        return render_template('notarization.html', **kwargs)
    if response.status_code == 200:
        kwargs = {
            "new": 'Transaction Hash: ' + response.json()['transaction hash'],
            "message": response.json()['message']
        }

    elif response.status_code == 400:
        kwargs = {
            "new": 'Value is missed'
        }

    else:
        kwargs = {
            "new": 'Fail to connect to blockchain'
        }
    return render_template('notarization.html', **kwargs)


@app.route('/get_trans')
def get_trans():
    node = request.args.get("hash")
    print(node)
    nodes = {'hash': node}
    global current_node
    try:
        response = requests.post(f'http://{current_node}/transaction/find', json=nodes)
    except:
        kwargs = {
            "sender": None,
            "recipient": None,
            "value": None,
            "data": 'Fail to connect to blockchain'
        }
        return render_template('notarization.html', **kwargs)
    if response.status_code == 200:
        kwargs = json.loads(response.content)

    elif response.status_code == 500:
        kwargs = {
            "sender": None,
            "recipient": None,
            "value": None,
            "data": json.loads(response.content)['Warning']
        }
    else:
        kwargs = {
            "sender": None,
            "recipient": None,
            "value": None,
            "data": 'Fail to connect to blockchain'
        }
    return render_template('notarization.html', **kwargs)


@app.route('/empty_page')
def empty_page():
    return render_template('empty_page.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)