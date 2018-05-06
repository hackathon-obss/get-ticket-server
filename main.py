from flask import Flask, request
from numpy import array

from newML import algoQueue, createTimeData, trainSubeData
from user import User
from user_sube import UserSube

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = True

timeClf = None
subeClf = None
users = {}
user_sube = {}
sube1 = []
sube2 = []


@app.route('/user', methods=['GET'])
def get_user():
    user = users[request.args.get('uid')]
    return 'uid:' + user.uid + '\neta1:' + user.eta1 + '\neta2:' + user.eta2 + '\noperation:' + user.operation \
           + '\nage:' + user.age


@app.route('/user', methods=['POST'])
def add_user():
    uid = request.form['uid']
    eta1 = request.form['eta1']
    eta2 = request.form['eta2']
    operation = request.form['operation']
    age = request.form['age']
    user = User(uid, eta1, eta2, operation, age)
    users[uid] = user
    time = timeClf.predict(array([[int(age), int(operation)]]))[0]
    user.time = time
    sube = str(subeClf.predict(array([[int(eta1), int(eta2), int(time), sube_total_time(1), sube_total_time(2)]]))[0])
    user.sube = sube
    if sube == '1':
        user.no = len(sube1)
        sube1.append(user)
        algoQueue(sube1, '1')
    else:
        user.no = len(sube2)
        sube2.append(user)
        algoQueue(sube2, '2')
    user_sube[uid] = UserSube(uid, sube, operation)

    for item in sube1:
        if item.uid == uid:
            return '{sube:' + sube + ",lineNo:" + str(item.no) + '}'
    for item in sube2:
        if item.uid == uid:
            return '{sube:' + sube + ",lineNo:" + str(item.no) + '}'

    return 'sube:' + sube


def sube_total_time(sube_number):
    total_time = 0
    if sube_number == 1:
        for user in sube1:
            total_time = total_time + user.time
    else:
        for user in sube2:
            total_time = total_time + user.time
    return total_time


@app.route('/eta', methods=['PUT'])
def update_eta():
    old_eta = user_sube[request.form['uid']].eta
    user_sube[request.form['uid']].eta = request.form['eta']
    user = users[request.form['uid']]
    sube = user.sube
    if sube == '1':
        user.eta1 = request.form['eta']
        for user_in_sube in sube1:
            if user_in_sube.uid == user.uid:
                user_in_sube.eta1 = request.form['eta']
        algoQueue(sube1, '1')
    else:
        user.eta2 = request.form['eta']
        for user_in_sube in sube2:
            if user_in_sube.uid == user.uid:
                user_in_sube.eta2 = request.form['eta']
        algoQueue(sube2, '2')
    return 'old_eta:' + old_eta


@app.route('/lineNo', methods=['GET'])
def get_line_no():
    uid = request.args.get('uid')
    for item in sube1:
        if item.uid == uid:
            return "lineNo:" + str(item.no)
    for item in sube2:
        if item.uid == uid:
            return "lineNo:" + str(item.no)


@app.route('/userx', methods=['POST'])
def delete_user():
    uid = request.form['uid']
    del users[uid]
    del user_sube[uid]
    for user in sube1:
        if user.uid == uid:
            sube1.remove(user)
    for user in sube1:
        if user.uid == uid:
            sube1.remove(user)
    return uid


if __name__ == '__main__':
    timeClf = createTimeData()
    subeClf = trainSubeData(timeClf)
    app.run(host='0.0.0.0')
