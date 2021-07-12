from gpio import *
from time import *
from ioeclient import *
from physical import *
import math
from environment import *

ENVIRONMENT_NAME = "Smoke"

state = 0
level = 0.0
ALARM_LEVEL = 40

def main():
    setup()
    while True:
		loop()
		
def setup():
    IoEClient.setup({
        "type": "Smoke Detector",
        "states": [{
            "name": "Alarm",
            "type": "bool",
            "controllable": False
        },
        {
            "name": "Level",
            "type": "number",
            "controllable": False
        }]
    })

    restoreProperty("Alarm Level", 40)
    IoEClient.onInputReceive(onInputReceiveDone)
    add_event_detect(0, detect)
    state = restoreProperty("state", 0)
    setState(state)
    

def onInputReceiveDone(data):
    processData(data, True)
    
def detect():
    processData(customRead(0), False)

def restoreProperty(propertyName, defaultValue):
    value = getDeviceProperty(getName(), propertyName)
    if  not (value is "" or value is None):
        if  type(defaultValue) is int :
            value = int(value)

        setDeviceProperty(getName(), propertyName, value)
        return value
    return defaultValue

def loop():
    global ENVIRONMENT_NAME
    value = Environment.get(ENVIRONMENT_NAME)
    if value >= 0:
        setLevel(Environment.get(ENVIRONMENT_NAME))
    # This code was added to see the smoke value and send a electrical signal when it
    # detects the value is more than 0.2:
    print(value)
    if value >= 0.2:
    	digitalWrite(0, HIGH)
    else:
    	digitalWrite(0, LOW)
    sleep(1)


def processData(data, bIsRemote):
    if len(data) <= 0 :
        return
    data = data.split(",")
    setState(int(data[0]))


def sendReport():
    global state
    global level
    report = str(state) + "," + str(level);   # comma seperated states
    IoEClient.reportStates(report)
    setDeviceProperty(getName(), "state", state)
    setDeviceProperty(getName(), "level", level)


def setState(newState):
    global state
    state = newState

    if newState is 0:
        digitalWrite(1, LOW)
    else:
        digitalWrite(1, HIGH)

    sendReport()


def setLevel(newLevel):
    global level
    if level == newLevel:
        return

    level = newLevel
    if level > ALARM_LEVEL:
        setState(1)
    else:
        setState(0)

    sendReport()

if __name__ == "__main__":
    main()