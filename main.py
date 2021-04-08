from flask import Flask
from flask_cors import CORS
import json
import os
from DataService import getData

CACHE = os.getenv('CACHE', 'True') == 'True'

data = getData(CACHE)

app = Flask(__name__)
CORS(app)


@app.route('/api/spencersCreek', methods=['GET'])
def getSpencersCreekData():
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
