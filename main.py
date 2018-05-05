from flask import Flask, request

from user import User

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = True

users = {}


@app.route('/user', methods=['GET'])
def get_user():
    user = users[request.args.get('uid')]
    return 'uid:' + user.uid + '\neta1:' + user.eta1 + '\neta1:' + user.eta1 + '\noperation:' + user.operation


@app.route('/user', methods=['POST'])
def add_user():
    uid = request.form['uid']
    eta1 = request.form['eta1']
    eta2 = request.form['eta2']
    operation = request.form['operation']
    users[uid] = User(uid, eta1, eta2, operation)
    return uid


@app.route('/etas', methods=['PUT'])
def update_etas():
    uid = request.form['uid']
    user = users[uid]
    user.eta1 = request.form['eta1']
    user.eta2 = request.form['eta2']
    return uid


if __name__ == '__main__':
    app.run(host='0.0.0.0')
