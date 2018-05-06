from flask import Flask, request
from numpy import array

from newML import createTimeData, algoQueue
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
sube1 = []
sube2 = []


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
    user = User(uid, eta1, eta2, operation, age)
    users[uid] = user
    time = timeClf.predict(array([[int(age), int(operation)]]))[0]
    user.time = time
    sube = str(subeClf.predict(array([[int(eta1), int(eta2), int(time), sube_total_time(1), sube_total_time(2)]]))[0])
    user.sube = sube
    if sube is '1':
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
			return 'sube:' + sube + ",lineNo:" + item.no + '}'
	for item in sube2:
		if item.uid == uid:
			return '{sube:' + sube + ",lineNo:" + item.no + '}'
			
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
    user = users[request.form['uid']]
    sube = user.sube
	if sube is '1':
		user.eta1 = request.form['eta']
		for user in sube1:
			if user.uid is uid:
				user.eta1 = request.form['eta']
		algoQueue(sube1, '1')
	else:
		user.eta2 = request.form['eta']
		for user in sube2:
			if user.uid is uid:
				user.eta2 = request.form['eta']
		algoQueue(sube2, '2')
    return 'old_eta:' + old_eta
	
@app.route('/lineNo', methods=['GET'])
def get_line_no():
	uid = request.args.get('uid')
	for item in sube1:
		if item.uid == uid:
			return "lineNo:" + item.no
	for item in sube2:
		if item.uid == uid:
			return "lineNo:" + item.no

if __name__ == '__main__':
    timeClf = createTimeData()
    subeClf = trainSubeData(timeClf)
    app.run(host='0.0.0.0')
