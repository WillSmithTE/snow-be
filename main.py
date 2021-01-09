import requests
from util import *
from flask import Flask
from flask_cors import CORS
import json
import os

data = {}

class YearData:
    def __init__(self, date, name, level):
        self.date = date
        self.name = name
        self.level = level

    def __repr__(self):
        print(self.date, self.name, self.level)
        return "-date " + self.date + "-name" + self.name + "-level" + self.level

def getData():
    response = requests.get("https://www.snowyhydro.com.au/wp-content/themes/snowyhydro/inc/getData.php?yearA=2020&yearB=1976").json() 
    for year in response:
        data[year] = 'hi'
        level = response[year]['snowyhydro']['level']
        onlySnow = list(filter(lambda x: 'snow' in x, level))
        yearData = list(map(lambda x : toYearData(x), onlySnow))
        print(yearData)
        data[year] = yearData
        print('data', data)
    return data

def toYearData(level):
    snow = level['snow']
    if not isinstance(snow, list):
        snow = [snow]
    onlySpencersCreek = list(filter(lambda x: x['-name'] == 'Spencers Creek', snow))
    if len(onlySpencersCreek) == 0:
        return None
    date = level['-date']
    name = onlySpencersCreek[0]['-name']
    snow = onlySpencersCreek[0]['#text']
    return YearData(date, name, snow)

data = getData()

app = Flask(__name__)
CORS(app)

@app.route('/api/spencersCreek/<year>', methods=['GET'])
def getSpencersCreekData(year):
    print(data)
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
