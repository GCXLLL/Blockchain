from flask import Flask, render_template
# from flask_bootstrap import Bootstrap4

app = Flask(__name__, static_folder='./static')
# bootstrap = Bootstrap4(app)


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
    return render_template('chain.html')


@app.route('/management')
def management():
    return render_template('management.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)