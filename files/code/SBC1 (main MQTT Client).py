from cli import *
from gui import *
import json
import mqttclient
from time import *
from gpio import *

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
	
	# It is verified if the program receives a message with the topic "LED".
	if msg.count("/LED") == 1:
		# Check if the Payload is "on" or "off". If it is neither of the 2 above, take no action.
		if msg.count("on") == 1:
			# If the payload is "on", the LED turns on, if it is "off" it turns off.
			digitalWrite(0, HIGH)
		elif msg.count("off") == 1:
			digitalWrite(0, LOW)
	# The same is done with all the others. With doors and windows, "open" and "close" are used instead of "on" and "off".
	elif msg.count("/AIR") == 1:
		if msg.count("on") == 1:
			digitalWrite(1, HIGH)
		elif msg.count("off") == 1:
			digitalWrite(1, LOW)
	elif msg.count("/COFFEE") == 1:
		if msg.count("on") == 1:
			digitalWrite(2, HIGH)
		elif msg.count("off") == 1:
			digitalWrite(2, LOW)
	elif msg.count("/FAN") == 1:
		if msg.count("on") == 1:
			digitalWrite(3, HIGH)
		elif msg.count("off") == 1:
			digitalWrite(3, LOW)
	elif msg.count("/DOOR") == 1:
		if msg.count("open") == 1:
			digitalWrite(4, HIGH)
		elif msg.count("close") == 1:
			digitalWrite(4, LOW)
	elif msg.count("/GARAGE") == 1:
		if msg.count("open") == 1:
			digitalWrite(5, HIGH)
		elif msg.count("close") == 1:
			digitalWrite(5, LOW)
	elif msg.count("/WATER") == 1:
		if msg.count("on") == 1:
			digitalWrite(6, HIGH)
		elif msg.count("off") == 1:
			digitalWrite(6, LOW)
	elif msg.count("/LAWN") == 1:
		if msg.count("on") == 1:
			digitalWrite(7, HIGH)
		elif msg.count("off") == 1:
			digitalWrite(7, LOW)
	elif msg.count("/LAMP") == 1:
		if msg.count("on") == 1:
			digitalWrite(8, HIGH)
		elif msg.count("off") == 1:
			digitalWrite(8, LOW)
	elif msg.count("/WINDOW") == 1:
		if msg.count("open") == 1:
			digitalWrite(9, HIGH)
		elif msg.count("close") == 1:
			digitalWrite(9, LOW)
	elif msg.count("/ALL") == 1:
		if msg.count("on") == 1:
			digitalWrite(0, HIGH)
			digitalWrite(1, HIGH)
			digitalWrite(2, HIGH)
			digitalWrite(3, HIGH)
			digitalWrite(4, HIGH)
			digitalWrite(5, HIGH)
			digitalWrite(6, HIGH)
			digitalWrite(7, HIGH)
			digitalWrite(8, HIGH)
			digitalWrite(9, HIGH)
		elif msg.count("off") == 1:
			digitalWrite(0, LOW)
			digitalWrite(1, LOW)
			digitalWrite(2, LOW)
			digitalWrite(3, LOW)
			digitalWrite(4, LOW)
			digitalWrite(5, LOW)
			digitalWrite(6, LOW)
			digitalWrite(7, LOW)
			digitalWrite(8, LOW)
			digitalWrite(9, LOW)
	
	CLI.exit()

def on_gui_update(msg, data):
	GUI.update(msg, json.dumps(data))

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
	
	# It waits 70 seconds for the DHCP protocol to work successfully.
	delay(70000)
	# The program connects to the broker with the "cisco1" user.
	mqttclient.connect("4.2.5.2", "cisco1", "cisco1")
	# In each process 2 seconds of delay is added so that the process is carried out well, because these methods work with MQTT packets.
	delay(2000)
	# Subscribes to the indicated topic.
	mqttclient.subscribe("/LED")
	delay(2000)
	mqttclient.subscribe("/COFFEE")
	delay(2000)
	mqttclient.subscribe("/FAN")
	delay(2000)
	mqttclient.subscribe("/DOOR")
	delay(2000)
	mqttclient.subscribe("/GARAGE")
	delay(2000)
	mqttclient.subscribe("/WATER")
	delay(2000)
	mqttclient.subscribe("/LAWN")
	delay(2000)
	mqttclient.subscribe("/LAMP")
	delay(2000)
	mqttclient.subscribe("/WINDOW")
	delay(2000)
	mqttclient.subscribe("/AIR")
	delay(2000)
	mqttclient.subscribe("/ALL")
	
	while True:
		delay(60000)

if __name__ == "__main__":
	main()
