from gpio import *
from time import *
from ioeclient import *
from physical import *
from bluetooth import *
import math

DEACTIVATE_TIMER = 5; # in seconds
state = 0
current_time = 0

def main():
	setup()
	while True:
		loop()
		

def setup():
    IoEClient.setup({
        "type": "Motion Detector",
        "states": [{
            "name": "On",
            "type": "bool",
            "controllable": False
        }]
    })
    global state
    state = restoreProperty("state", 0)
    setState(state)


def restoreProperty(propertyName, defaultValue):
    value = getDeviceProperty(getName(), propertyName)
    if  not (value is "" or value is None):
        if  type(defaultValue) is int :
            value = int(value)

        setDeviceProperty(getName(), propertyName, value)
        return value
    return defaultValue


def mouseEvent(pressed, x, y, firstPress):
    setState(1)


def loop():
    global state
    global current_time
    if  state == 1 :
        current_time = current_time - 1
        if  current_time <= 0 :
            setState(0)
    
    # This code was added to communicate a electrical signal if detects motion. If no detect, it turns off.      
    if state == 1:
    	digitalWrite(0, HIGH)
    else:
    	digitalWrite(0, LOW)

    sleep(1)


def setState(newState):
    global state
    global DEACTIVATE_TIMER
    global current_time
    state = newState

    if  state is 0 :
        digitalWrite(1, LOW)
    else:
        digitalWrite(1, HIGH)
        current_time = DEACTIVATE_TIMER


    IoEClient.reportStates(state)
    setDeviceProperty(getName(), "state", state)
    

if __name__ == "__main__":
    main()