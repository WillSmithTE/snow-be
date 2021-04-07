from DataService import getData
from util import read, save
from DataRepository import getSavedData

def hasNewData():
    latestSavedDate = getLatestSavedDate()
    if latestSavedDate:
        newData = getData(False)
        newLastDate = getLatestDate(newData)
        return latestSavedDate != newLastDate
    else:
        return False

def getLatestSavedDate():
    savedData = getSavedData()
    return getLatestDate(savedData)

def getLatestDate(data):
    lastYearData = data[len(data) - 1].data
    latestDate = lastYearData[len(lastYearData) - 1].date
    return latestDate
