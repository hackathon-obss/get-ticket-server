from flask import Flask, request
from numpy import array

from newML import createTimeData
from newML import trainSubeData
from user import User
from user_sube import UserSube

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = True

timeClf = None
subeClf = None
users = {}
user_sube = {}


@app.route('/user', methods=['GET'])
def get_user():
    user = users[request.args.get('uid')]
    return 'uid:' + user.uid + '\neta1:' + user.eta1 + '\neta2:' + user.eta1 + '\noperation:' + user.operation


@app.route('/user', methods=['POST'])
def add_user():
    uid = request.form['uid']
    eta1 = request.form['eta1']
    eta2 = request.form['eta2']
    operation = request.form['operation']
    age = request.form['age']
    users[uid] = User(uid, eta1, eta2, operation, age)
    time = timeClf.predict(array([[int(age), int(operation)]]))[0]
    sube = str(subeClf.predict(array([[int(eta1), int(eta2), int(time), sube_total_time(1), sube_total_time(2)]]))[0])
    user_sube[uid] = UserSube(uid, sube, operation)
    return 'sube:' + sube


def sube_total_time(sube_number):
    total_time = 0
    for uid in user_sube:
        if user_sube[uid].sube is sube_number:
            total_time = total_time + int(user_sube[uid].operation) * 5
    return total_time


@app.route('/eta', methods=['PUT'])
def update_eta():
    old_eta = user_sube[request.form['uid']].eta
    user_sube[request.form['uid']].eta = request.form['eta']
    return 'old_eta:' + old_eta


if __name__ == '__main__':
    timeClf = createTimeData()
    subeClf = trainSubeData(timeClf)
    app.run(host='0.0.0.0')
