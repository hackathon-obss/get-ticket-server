import random

from numpy import array
from sklearn.neural_network import MLPClassifier

from user import User

sube1user = []
sube2user = []
trainData = []


def append_to_file(file_name, text):
    f = open(file_name, "a")
    f.write(text + "\n")
    f.close()


def print_to_new_file(file_name, text):
    f = open(file_name, "w+")
    f.write(text)
    f.close()


def read_lines_from_file(file_name):
    f = open(file_name, "r")
    lines = f.readlines()
    f.close()
    return lines


def read_from_file(file_name):
    f = open(file_name, "r")
    text = f.read()
    f.close()
    return text


def getSubeEstimationTime(lst):
    if not lst:
        return 0
    time = 0
    for item in lst:
        time = time + item[2]
    return time


# yas gruplarina gore sure datasi olusturur. valuelari yas ve islem typei result ise sure olarak kullanilacak
def createTimeData():
    timeTrainData = []
    sampleSize = 400
    for x in range(sampleSize):
        age = random.randint(20, 35)
        activityType = random.randint(1, 4)
        if activityType == 1:
            sure = random.randint(5, 10)
        elif activityType == 2:
            sure = random.randint(10, 15)
        elif activityType == 3:
            sure = random.randint(15, 20)
        elif activityType == 4:
            sure = random.randint(20, 25)
        timeTrainData.append([age, activityType, sure])

    for x in range(sampleSize):
        age = random.randint(35, 60)
        activityType = random.randint(1, 4)
        if activityType == 1:
            sure = random.randint(5, 15)
        elif activityType == 2:
            sure = random.randint(10, 20)
        elif activityType == 3:
            sure = random.randint(15, 25)
        elif activityType == 4:
            sure = random.randint(20, 30)
        timeTrainData.append([age, activityType, sure])

    for x in range(sampleSize):
        age = random.randint(60, 85)
        activityType = random.randint(1, 4)
        if activityType == 1:
            sure = random.randint(10, 15)
        elif activityType == 2:
            sure = random.randint(10, 25)
        elif activityType == 3:
            sure = random.randint(15, 30)
        elif activityType == 4:
            sure = random.randint(25, 35)
        timeTrainData.append([age, activityType, sure])

    values = []
    result = []
    for item in timeTrainData:
        values.append([item[0], item[1]])
        result.append(item[2])

    trainValuesNpArray = array(values)
    trainResultNpArray = array(result)
    _solver = 'lbfgs'
    _alpha = 1e-5
    _hiddenLayerSize = (50, 100,)
    clf = MLPClassifier(solver=_solver, alpha=_alpha, hidden_layer_sizes=_hiddenLayerSize)
    clf.fit(trainValuesNpArray, trainResultNpArray)
    print("Time data train ended")
    return clf


def trainSubeData(timeClf):
    for i in range(1200):
        sube1arriveTime = random.randint(0, 15)
        sube2arriveTime = random.randint(0, 15)
        islemTipi = random.randint(1, 4)
        age = random.randint(20, 85)
        sube1totalTime = getSubeEstimationTime(sube1user)
        sube2totalTime = getSubeEstimationTime(sube2user)
        subeSecimi = 0
        predictedTime = timeClf.predict(array([[age, islemTipi]]))
        if sube1totalTime + predictedTime <= sube2totalTime + predictedTime:
            sube1user.append([sube1arriveTime, sube2arriveTime, predictedTime[0], sube1totalTime])
            subeSecimi = 1
        else:
            sube2user.append([sube1arriveTime, sube2arriveTime, predictedTime[0], sube2totalTime])
            subeSecimi = 2
        trainData.append(
            [sube1arriveTime, sube2arriveTime, predictedTime[0], sube1totalTime, sube2totalTime, subeSecimi])
    print("train data creation has ended")
    """print_to_new_file("subeData.txt","")
    for item in trainData:
        append_to_file("subeData.txt", str(item))
    lines = read_lines_from_file("subeData.txt")
    for line in lines:
        line = line.replace("[","").replace("]","").replace(" ","").replace("\n","").split(",")
        trainData.append([int(line[0]),int(line[1]),int(line[2]),int(line[3]),int(line[4]),int(line[5])])"""
    values = []
    result = []
    for item in trainData:
        values.append([item[0], item[1], item[2], item[3], item[4]])
        result.append(item[5])
    trainValuesNpArray = array(values)
    trainResultNpArray = array(result)
    _solver = 'lbfgs'
    _alpha = 1e-5
    _hiddenLayerSize = (50, 100,)
    clf = MLPClassifier(solver=_solver, alpha=_alpha, hidden_layer_sizes=_hiddenLayerSize)
    clf.fit(trainValuesNpArray, trainResultNpArray)
    return clf
    """predicted = clf.predict(array([[10, 15, 15, 0, 0]]))
    print(predicted)
    predicted = clf.predict(array([[0, 2, 15, 15, 0]]))
    print(predicted)
    predicted = clf.predict(array([[14, 9, 25, 15, 15]]))
    print(predicted)
    predicted = clf.predict(array([[10, 9, 15, 40, 15]]))
    print(predicted)
    predicted = clf.predict(array([[13, 7, 16, 40, 30]]))
    print(predicted)"""


def algoQueue(lst, sube):
    for j in range(len(lst)):
        i = len(lst) - 1
        while i > 0:
            eta = int(lst[i].get_eta())
            if eta < 5:
                break
            eta = int(lst[i].get_eta())
            time = int(lst[i].time)
            previous_eta = int(lst[i - 1].get_eta())
            if eta + time < previous_eta:
                temp2 = lst[i].no
                lst[i].no = lst[i - 1].no
                lst[i - 1].no = temp2
                temp = lst[i]
                lst[i] = lst[i - 1]
                lst[i - 1] = temp
            i = i - 1


if __name__ == '__main__':
    user1 = User('1', '6', '3', '4', '6')
    user1.time = 1
    user1.sube = '1'
    user1.no = 4
    user2 = User('2', '8', '3', '4', '6')
    user2.time = 2
    user2.no = 3
    user2.sube = '1'
    user3 = User('3', '10', '3', '4', '6')
    user3.time = 3
    user3.no = 2
    user3.sube = '1'
    user4 = User('4', '12', '3', '4', '6')
    user4.time = 4
    user4.no = 1
    user4.sube = '1'
    user5 = User('5', '14', '3', '4', '6')
    user5.time = 5
    user5.no = 0
    user5.sube = '1'
    lst = [user5, user4, user3, user2, user1]
    algoQueue(lst, '1')
    for user in lst:
        print(user.uid, user.no)
