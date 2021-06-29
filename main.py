from flask import Flask
from flask_cors import CORS
import json
import os
from DataService import isDataOutdated, getSavedData, updateData
import logging

logging.basicConfig()
logging.root.setLevel(logging.INFO)

if not getSavedData():
    updateData()

app = Flask(__name__)
CORS(app)

@app.route('/api/spencersCreek', methods=['GET'])
def getSpencersCreekData():
    return json.dumps(getSavedData(), default=lambda x: x.__dict__)

@app.route('/api/refreshData', methods=['POST'])
def refreshData():
    message = None
    if isDataOutdated():
        updateData()
        message = 'Data has been refreshed'
    else:
        message = 'No new data found to refresh'
    logging.info(message)
    return json.dumps({'response': message}), 200, {'ContentType': 'application/json'}

app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
