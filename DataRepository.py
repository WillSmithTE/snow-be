from util import read, save

DATA_FILE = 'data.pickle'

def saveData(data):
    save(data, DATA_FILE)
    
def getSavedData():
    return read(DATA_FILE)

DataRepository = {
    saveData: saveData,
    getSavedData: getSavedData
}
