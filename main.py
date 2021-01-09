import requests
from util import *
from flask import Flask
from flask_cors import CORS
import json
import os

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

def getData():
    listData = []
    i = 2011
    while i < 2020:
        [first, second] = [str(i), str(i+1)]
        response = requests.get("https://www.snowyhydro.com.au/wp-content/themes/snowyhydro/inc/getData.php?yearA=" + first + "&yearB=" + second).json() 
        for year in response:
            level = response[year]['snowyhydro']['level']
            onlySnow = list(filter(lambda x: 'snow' in x, level))
            yearData = list(map(lambda x : toYearData(x), onlySnow))
            for thing in yearData:
                print(thing)
            noNullsYearData = list(filter(lambda x : x is not None, yearData))
            print('-------[')
            for thing in yearData:
                print(thing)
            listData.append(Data(year, noNullsYearData))
        i += 2
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

data = getData()

app = Flask(__name__)
CORS(app)

@app.route('/api/spencersCreek/<year>', methods=['GET'])
def getSpencersCreekData(year):
    return json.dumps(data, default=lambda x: x.__dict__)

app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)


# type ForeignYearData struct {
# 	Snowyhydro SnowyHydro `json:"snowyhydro`
# }

# type SnowyHydro struct {
# 	Level []Level `json:"level`
# }

# type Level struct {
# 	Date string      `json:"-date`
# 	Snow interface{} `json:"snow`
# }

# type Snow struct {
# 	Name      string `json:"-name`
# 	Text      string `json:"#text`
# 	Timestamp string `json:"-dataTimestamp`
# }

# 		yearData := raw[year].Snowyhydro.Level
