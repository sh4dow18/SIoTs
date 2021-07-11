from options import Options
from time import *
import math
from physical import *
from gpio import *
from environment import Environment
from ioeclient import IoEClient
#from pyjs import *


WATERLEVEL_RATE = 0.1 # 0.1 cm per second        # var WATERLEVEL_RATE
HUMIDITY_RATE = 5. / 3600 # 5% per hour        # var HUMIDITY_RATE
VOLUME_AT_RATE = 100000.        # var VOLUME_AT_RATE
MAX_RATE = 1.e6        # var MAX_RATE
state = 0 # 0 off, 1 on        # var state

def setup ():
    global state
    
    IoEClient.setup({
        "type": "Lawn Sprinkler",
        "states": [{
            "name": "Status",
            "type": "bool",
            "controllable": True
        }]
    })

    
    IoEClient.onInputReceive(lambda rinput: processData(rinput, True))

    def on_event_detect(): 
        processData(customRead(0), False)
    add_event_detect(0,  on_event_detect)
	"""
	# The following code was changed:
	state = restoreProperty("state", 0)
	setState(state)
	"""
	# To this:
	# When an electrical signal is received, the lawn sprinkler turns on. If the signal does not arrive, it turns off.
    if digitalRead(0) == HIGH:
    	setState(1)
    else:
    	setState(0)



def restoreProperty (propertyName, defaultValue):
    value = getDeviceProperty(getName(), propertyName)        # var value
    if value:
        if isinstance(defaultValue, (int, float)):
            value = int(value)

        setDeviceProperty(getName(), propertyName, value)
        return value
    

    return defaultValue



def mouseEvent (pressed, x, y, firstPress):
    if firstPress:
        setState(( 0  if state  else 1 ) )



def processData (data, bIsRemote):
    if len(data) <= 0:
        return
    setState(int(data))



def setState (newState):
    global state
    state = newState

    digitalWrite(5, state)
    customWrite(0, state)
    IoEClient.reportStates(state)
    setDeviceProperty(getName(), "state", state)
    updateEnvironment()




def updateEnvironment ():
    if state == 1:
        volumeRatio = VOLUME_AT_RATE / Environment.getVolume()        # var volumeRatio
        Environment.setContribution("Water Level", WATERLEVEL_RATE * volumeRatio, MAX_RATE, True)
        Environment.setContribution("Humidity", HUMIDITY_RATE * volumeRatio, MAX_RATE, True)
    else:
        Environment.setContribution("Water Level", 0, 0, True)
        Environment.setContribution("Humidity", 0, 0, True)


if __name__ == "__main__":
    setup()
    # And also this was added to execute the setup infinitely:
    while True:
        #loop()
        setup()

