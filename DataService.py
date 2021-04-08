import requests
from util import read, save
from flask import Flask
from flask_cors import CORS
import json
import os
from DataRepository import getSavedData, saveData
from datetime import datetime

class Data:
    def __init__(self, year, data):
        self.year = year
        self.data = data


class YearData:
    def __init__(self, date, name, snow):
        self.date = date
        self.name = name
        self.snow = snow

    def __repr__(self):
        return "-date " + self.date + "-name" + self.name + "-snow" + str(self.snow) + "\n"


def getData(cache = True):
    listData = getSavedData()
    if listData is None or not cache:
        listData = []
        i = 1976
        lastYear = datetime.now().year - 1
        while i <= lastYear:
            [first, second] = [str(i), str(i+1)]
            response = requests.get("https://www.snowyhydro.com.au/wp-content/themes/snowyhydro/inc/getData.php?yearA=" + first + "&yearB=" + second).json()
            for year in response:
                level = response[year]['snowyhydro']['level']
                onlySnow = list(filter(lambda x: 'snow' in x, level))
                yearData = list(map(lambda x: toYearData(x), onlySnow))
                noNullsYearData = list(filter(lambda x: x is not None, yearData))
                if len(noNullsYearData):
                    listData.append(Data(year, noNullsYearData))
            i += 2
        saveData(listData)
    return listData


def toYearData(level):
    snow = level['snow']
    if not isinstance(snow, list):
        snow = [snow]
    onlySpencersCreek = list(filter(lambda x: x['-name'] == 'Spencers Creek', snow))
    if len(onlySpencersCreek) == 0:
        return None
    date = level['-date']
    name = onlySpencersCreek[0]['-name']
    snow = float(onlySpencersCreek[0]['#text'])
    return YearData(date, name, snow)

def isDataOutdated():
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
