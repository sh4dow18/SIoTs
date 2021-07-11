from cli import *
from gui import *
import json
import mqttclient
from time import *
from gpio import *

again = False

def guiEvent(type, args):
	data = json.loads(args)
	
	mqttclient.init()
	
	if type == "state":
		GUI.update("state", json.dumps(mqttclient.state()))
	elif type == "connect":
		mqttclient.connect(data["broker_address"], data["username"], data["password"])
	elif type == "disconnect":
		mqttclient.disconnect()
	elif type == "subscribe":
		mqttclient.subscribe(data["topic"])
	elif type == "unsubscribe":
		mqttclient.unsubscribe(data["topic"])
	elif type == "publish":
		mqttclient.publish(data["topic"], data["payload"], data["qos"])

def cliEvent(type, args):
	if type == "invoked" and args[0] == "mqttclient":
		if len(args) < 2 or len(args) > 1 and args[1] == "-?" or args[1] == "/?":
			print_cli_usage()
			CLI.exit()
		elif len(args) > 1 and args[1] != "-?" and args[1] != "/?":
			mqttclient.init()
			
			if len(args) > 2 and len(args) < 6 and args[1] == "connect":
				username = ""
				password = ""
				
				if len(args) > 3:
					username = args[3]
					
					if len(args) == 5:
						password = args[4]
				
				mqttclient.connect(args[2], username, password)
			elif len(args) == 2 and args[1] == "disconnect":
				mqttclient.disconnect()
			elif len(args) == 3 and args[1] == "subscribe":
				mqttclient.subscribe(args[2])
			elif len(args) == 3 and args[1] == "unsubscribe":
				mqttclient.unsubscribe(args[2])
			elif len(args) == 5 and args[1] == "publish":
				mqttclient.publish(args[2], args[3], args[4])
			elif len(args) == 2 and args[1] == "display-last-message":
				messages = mqttclient.state()["messages"]
				
				if len(messages) > 0:
					print messages[-1]
				
				print ""
				CLI.exit()
			elif len(args) == 2 and args[1] == "display-all-messages":
				messages = mqttclient.state()["messages"]
				
				for message in messages:
					print message
				
				print ""
				CLI.exit()
			elif len(args) == 2 and args[1] == "display-last-event":
				events = mqttclient.state()["events"]
				
				if len(events) > 0:
					print events[-1]
				
				print ""
				CLI.exit()
			elif len(args) == 2 and args[1] == "display-all-events":
				events = mqttclient.state()["events"]
				
				for event in events:
					print event
				
				print ""
				CLI.exit()
			else:
				print_cli_usage()
				CLI.exit()
	elif type == "interrupted":
		CLI.exit()

def print_cli_usage():
	print "MQTT Client"
	print ""
	print "Usage:"
	print "mqttclient connect <broker address> [username] [password]"
	print "mqttclient disconnect"
	print "mqttclient subscribe <topic>"
	print "mqttclient unsubscribe <topic>"
	print "mqttclient publish <topic> <payload> <qos>"
	print "mqttclient display-last-message"
	print "mqttclient display-all-messages"
	print "mqttclient display-last-event"
	print "mqttclient display-all-events"
	print ""

def on_connect(status, msg, packet):
	if status == "Success" or status == "Error":
		print status + ": " + msg
	elif status == "":
		print msg

	CLI.exit()

def on_disconnect(status, msg, packet):
	if status == "Success" or status == "Error":
		print status + ": " + msg
	elif status == "":
		print msg
	
	CLI.exit()

def on_subscribe(status, msg, packet):
	if status == "Success" or status == "Error":
		print status + ": " + msg
	elif status == "":
		print msg
	
	CLI.exit()

def on_unsubscribe(status, msg, packet):
	if status == "Success" or status == "Error":
		print status + ": " + msg
	elif status == "":
		print msg
	
	CLI.exit()

def on_publish(status, msg, packet):
	if status == "Success" or status == "Error":
		print status + ": " + msg
	elif status == "":
		print msg
	
	CLI.exit()

def on_message_received(status, msg, packet):
	if status == "Success" or status == "Error":
		print status + ": " + msg
	elif status == "":
		print msg
	
	CLI.exit()

def on_gui_update(msg, data):
	GUI.update(msg, json.dumps(data))

def loop():
	# Calls the global variable "again"
	global again
	
	# If it receives an electrical signal from the smoke detector, it sends a signal to the fan and the siren.
	if digitalRead(0) == HIGH:
		digitalWrite(1, HIGH)
		digitalWrite(2, HIGH)
	else:
		digitalWrite(1, LOW)
		digitalWrite(2, LOW)
	
	# If it receives an electrical signal from the motion detector, an electrical signal is sent to the camera
	# and a message is also sent to the broker in order to open the door connected to SBC 3. The variable
	# "again" is used to send only one message for the door.
	if digitalRead(3) == HIGH:
		digitalWrite(4, HIGH)
		if again is False:
			mqttclient.publish("/DOOR2", "open", "0")
			again = True
	else:
		digitalWrite(4, LOW)
		if again is True:
			mqttclient.publish("/DOOR2", "close", "0")
			again = False


def main():
	GUI.setup()
	CLI.setup()
	mqttclient.init()
	mqttclient.onConnect(on_connect)
	mqttclient.onDisconnect(on_disconnect)
	mqttclient.onSubscribe(on_subscribe)
	mqttclient.onUnsubscribe(on_unsubscribe)
	mqttclient.onPublish(on_publish)
	mqttclient.onMessageReceived(on_message_received)
	mqttclient.onGUIUpdate(on_gui_update)
	
	# Wait 80 seconds for the DHCP protocol to work correctly and also not to interfere with all SBC 1 packets.
	delay(80000)
	# Connects to the Broker
	mqttclient.connect("4.2.5.2", "cisco2", "cisco2")
	
	while True:
		# The "loop" function is executed infinitely.
		loop()

if __name__ == "__main__":
	main()
