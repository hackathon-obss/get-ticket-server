from flask import Flask, request

from user import User
from user_sube import UserSube

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = True

users = {}
user_sube = {}


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
    user_sube[uid] = UserSube(uid, 'sube', 'eta')
    return uid


@app.route('/eta', methods=['PUT'])
def update_etas():
    old_eta = user_sube[request.form['uid']].eta
    user_sube[request.form['uid']].eta = request.form['eta']
    return old_eta


if __name__ == '__main__':
    app.run(host='0.0.0.0')
