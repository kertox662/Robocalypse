import json as js

def loadSettings(sFile = "data/configs.json"):
    with open(sFile) as jsonFile:
        data = js.load(jsonFile)
    return data