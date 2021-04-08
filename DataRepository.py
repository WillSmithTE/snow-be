from util import read, save

DATA_FILE = 'data.pickle'

DataRepository = {
    saveData: saveData,
    getSavedData: getSavedData
}

def saveData(data):
    save(data, DATA_FILE)
    
def getSavedData():
    return read(DATA_FILE)
