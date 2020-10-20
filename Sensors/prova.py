from Sensors.thread import IlMioThread
from random import randint
import json

data = ""


def creareJson(data):
    data_out = json.dumps(data)
    data_in = json.loads(data_out)


def createSensor():
    global data
    with open('attributes.json') as configFile:
        data = json.load(configFile)
        configFile.close()


def setSensor(data):
    for count in range(0, len(data)):
        for sensors in data.__getitem__(count)['Sensors']:
            sensors['Value'] = randint(1, 10)
    return data


createSensor()

for t in range(0, len(data)):
    thread = IlMioThread(data.__getitem__(t), None)
    thread.start()
