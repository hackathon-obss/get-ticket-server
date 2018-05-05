import random
import numpy as np
import sklearn
from sklearn.neural_network import MLPClassifier
from numpy import array
islemTipleri = [0,5,10,15,20]
sube1user = []
sube2user = []
trainData = []

def append_to_file(file_name, text):
	f = open(file_name,"a")
	f.write(text+"\n")
	f.close()

def print_to_new_file(file_name, text):
	f = open(file_name,"w+")
	f.write(text)
	f.close()

def read_lines_from_file(file_name):
	f = open(file_name,"r")
	lines = f.readlines()
	f.close()
	return lines

def read_from_file(file_name):
	f = open(file_name,"r")
	text = f.read()
	f.close()
	return text

def getSubeEstimationTime(lst):
    if not lst:
        return 0
    time = 0
    for item in lst:
        time = time + islemTipleri[item[2]]
    return time

def trainSubeData():
    print_to_new_file("allData.txt","")

    for i in range(1000):
        sube1arriveTime = random.randint(0,15)
        sube2arriveTime = random.randint(0,15)
        islemTipi = random.randint(1,4)
        sube1totalTime = getSubeEstimationTime(sube1user)
        sube2totalTime = getSubeEstimationTime(sube2user)
        subeSecimi = 0
        if sube1totalTime+islemTipleri[islemTipi] <= sube2totalTime+islemTipleri[islemTipi]:
            sube1user.append([sube1arriveTime, sube2arriveTime, islemTipi, sube1totalTime+sube2totalTime])
            subeSecimi = 1
        else:
            sube2user.append([sube1arriveTime, sube2arriveTime, islemTipi, sube2totalTime])
            subeSecimi = 2
        trainData.append([sube1arriveTime, sube2arriveTime, islemTipi, sube1totalTime, sube2totalTime, subeSecimi])
    print("train data creation has ended")
    for dt in trainData:
        append_to_file("allData.txt", str(dt))
    """lines = read_lines_from_file("allData1.txt")
    for line in lines:
        line = line.replace("[","").replace("]","").replace(" ","").replace("\n","").split(",")
        trainData.append([int(line[0]),int(line[1]),int(line[2]),int(line[3]),int(line[4]),int(line[5])])
    """
    values = []
    result = []
    for item in trainData:
        values.append([item[0],item[1],item[2],item[3],item[4]])
        result.append(item[5])
    trainValuesNpArray = array(values)
    trainResultNpArray = array(result)
    _solver = 'lbfgs'
    _alpha = 1e-5
    _hiddenLayerSize = 	(50,50,)
    clf = MLPClassifier(solver=_solver, alpha=_alpha, hidden_layer_sizes=_hiddenLayerSize)
    clf.fit(trainValuesNpArray, trainResultNpArray)
    print("train has ended")
    """predicted = clf.predict(array([[2, 3, 3, 0, 0]]))
    print(predicted)
    predicted = clf.predict(array([[15, 0, 1, 15, 0]]))
    print(predicted)
    predicted = clf.predict(array([[0, 0, 4, 15, 5]]))
    print(predicted)
    predicted = clf.predict(array([[13, 6, 1, 15, 25]]))
    print(predicted)
    predicted = clf.predict(array([[5, 10, 2, 20, 25]]))
    print(predicted)

    predicted = clf.predict(array([[8, 5, 4, 30, 25]]))
    print(predicted)
    predicted = clf.predict(array([[4, 5, 4, 30, 45]]))
    print(predicted)
    predicted = clf.predict(array([[13, 9, 1, 50, 45]]))
    print(predicted)
    predicted = clf.predict(array([[1, 12, 1, 50, 50]]))
    print(predicted)
    predicted = clf.predict(array([[4, 14, 2, 55, 50]]))
    print(predicted)"""

def calculateSubeValue(lst, subeNo):
    return lst[subeNo-1] + islemTipleri[lst[2]]

def subeSiraValueHesapla(subeList, subeNo):
    newSubeList = []
    count = 0
    for item in subeList:
        count = count + 1
        #newSubeList.append([item[subeNo-1], islemTipleri[item[2]], calculateSubeValue(item, subeNo)])
        newSubeList.append([item[subeNo-1], islemTipleri[item[2]], count, calculateSubeValue(item, subeNo)])
    subeValues = []
    for item in newSubeList:
        subeValues.append(item[3])
    subeValues.sort()
    for item in newSubeList:
        index = subeValues.index(item[3])
        item[3] = index

    return newSubeList

def trainSubeQueue(subeLst):
    values = []
    result = []
    for item in trainData:
        values.append([item[0],item[1],item[2]])
        result.append(item[3])

    trainValuesNpArray = array(values)
    trainResultNpArray = array(result)

    _solver = 'lbfgs'
    _alpha = 1e-5
    _hiddenLayerSize = 	(50,50,)
    clf = MLPClassifier(solver=_solver, alpha=_alpha, hidden_layer_sizes=_hiddenLayerSize)
    clf.fit(trainValuesNpArray, trainResultNpArray)

    predicted = clf.predict(array([[4, 15, 80]]))
    print(predicted)

def main():
    trainSubeData()
    newSube1List = subeSiraValueHesapla(sube1user, 1)
    newSube2List = subeSiraValueHesapla(sube2user, 2)
    trainSubeQueue(newSube1List)

main()
