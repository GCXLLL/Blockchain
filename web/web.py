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
    response = requests.get('http://127.0.0.1:5000/chain_request')
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
    if session.get('pswd'):
        return render_template('management.html')
    else:
        pswd = None
        pswd = request.args.get("password")
        if pswd:
            print(pswd)
            if pswd == 'chenxiaoguo':
                session['pswd'] = pswd
                return render_template('management.html')
        print('no pswd')
        return render_template('management_login.html')


@app.route('/getBlock')
def get_block():
    index = request.args.get("index")
    print(index)
    if chain:
        show_block(block=chain[int(index)-1])
    return render_template('block.html')


@app.route('/empty_page')
def empty_page():
    return render_template('empty_page.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)