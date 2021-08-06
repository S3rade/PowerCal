#!/bin/python3

#Dependencies
import dweepy
import EmulateGPIO as GPIO
from IPython.display import clear_output
import time
import os
import sys
from tabulate import tabulate
import requests
import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime

##################################################################
# MQTT  
MQTT_Broker = "172.16.0.12"
MQTT_Port = 1883
Keep_Alive_Interval = 45
topic = "Cost/Sensors"

def on_connect(client, userdata, rc):
	if rc != 0:
		pass
		print("Unable to connect to MQTT Broker...")
	else:
		print("Connected with MQTT Broker: " + str(MQTT_Broker))

def on_publish(client, userdata, mid):
	pass
		
def on_disconnect(client, userdata, rc):
	if rc !=0:
		pass
		
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.tls_set('/root/cost_vol/scripts/cacert/ca.crt')
mqttc.username_pw_set("cost", password="cost")
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))		

def publishToTopic(topic, message):
	mqttc.publish(topic,message)
	print ("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
	print("")


def updateDoorMqtt(applianceDoor, statusDoor, editedbyDoor, topic):
	data = {}
	data['appliance'] = applianceDoor
	data['status'] = statusDoor
	data['editedby'] = editedbyDoor
	#Humidity_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
	dataJson = json.dumps(data)
	print("Publishing fan data... ")
	publishToTopic(topic, dataJson)

##################################################################
#others
_=os.system("clear") #clear screen/terminal
def nl():
    print('\n') #prints new line when function is called
####################

##################################################################
myThing = "LLLALALAALLAALLLLALLLLALLALALAALAALALALLLAAAAALLLLLAALALAALLLLAALLLLLLALAALdoor" #Add value: add your dweet thing name
##################################################################

##################################################################
#setting up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
_=os.system("clear")

doorSwitchPin = 1
GPIO.setup(doorSwitchPin, GPIO.OUT)
GPIO.output(doorSwitchPin, False) #True = set 3.3V on the pin.
                                #False = set 0V on the pin.

applianceDoor = "garageDoor"
statusDoor = "close"
editedbyDoor = "Admin"

_=os.system("clear") #clear screen/terminal
##################################################################

print (tabulate([[applianceDoor, statusDoor, editedbyDoor]], ["applianceDoor", "statusDoor", "editedbyDoor"], tablefmt="grid"))
print (tabulate(["The door is " + statusDoor]))
print('----------------------------------------------------------')
print('Dweeting in progress (Garage Door)...')
url = "http://172.16.0.13:8080/add/" + "garageDoor" + "?status=" + statusDoor + "&editedby=" + editedbyDoor
print(url) 
print(requests.put(url))

url1 = "http://172.17.0.13:8080/add/" + "garageDoor" + "?status=" + statusDoor + "&editedby=" + editedbyDoor
print(url1) 
print(requests.put(url1))

old_dweet = dweepy.dweet_for(myThing, {"status": statusDoor , "editedby": editedbyDoor}) #this function sends data to dweet.io
old_created = old_dweet['created'] #get the time stamp of the first dweet
print('Dweet successfully sent @' , old_created + '\n')

def starto():
    global old_dweet
    global old_created
    global old_created
    global applianceDoor
    global statusDoor
    #global editedbyDoor
    global topic
    counter = 0
    global MQTT_Broker 
    global MQTT_Port 
    global Keep_Alive_Interval

    while True:
        new_dweet = dweepy.get_latest_dweet_for(myThing) #get latest dweet
        new_created = new_dweet[0]["created"] #put the created value of the lastest dweet into a variable
        newStatusDoor = new_dweet[0]["content"]["status"]
        neweditedbyDoor = new_dweet[0]["content"]["editedby"]
        if new_created != old_created: #check to see if the the old dweet is different from the new dweet
            mqttc = mqtt.Client()
            mqttc.on_connect = on_connect
            mqttc.on_disconnect = on_disconnect
            mqttc.on_publish = on_publish
            mqttc.tls_set('/root/cost_vol/scripts/cacert/ca.crt')
            mqttc.username_pw_set("cost", password="cost")
            mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
            counter += 1
            _=os.system("clear") #clear screen/terminal
            #print("A New dweet detected! {" + str(counter) + "} ",end='\n')
            print('----------------------------------------------------------')
            print("A New remote command has been detected!",end='\n')
            #print(old_dweet)
            print('Request to:')
            print('Turn the door ' + newStatusDoor)
            #print(newhm)
            old_created = new_created

            if newStatusDoor == "open":
                if statusDoor == "OPEN":
                    nl()
                    print('----------------------------------------------------------')
                    print (tabulate(["The Garage Door is already" + statusDoor]))
                    updateDoorMqtt(applianceDoor, statusDoor, neweditedbyDoor, topic)
                    print (tabulate([[applianceDoor, statusDoor, neweditedbyDoor]], ["applianceDoor", "statusDoor", "editedbyDoor"], tablefmt="grid"))
                    print (tabulate(["The door is " + statusDoor]))
                else:
                    nl()
                    print('----------------------------------------------------------')
                    statusDoor = "OPEN"
                    updateDoorMqtt(applianceDoor, statusDoor, neweditedbyDoor, topic)
                    print("Your door has been opened!")
                    print (tabulate([[applianceDoor, statusDoor, neweditedbyDoor]], ["applianceDoor", "statusDoor", "editedbyDoor"], tablefmt="grid"))
                    print (tabulate(["The door is " + statusDoor]))

            elif newStatusDoor == "close":
                if statusDoor == "CLOSE":
                    nl()
                    print('----------------------------------------------------------')
                    print (tabulate(["The Garage Door is already" + statusDoor]))
                    updateDoorMqtt(applianceDoor, statusDoor, neweditedbyDoor, topic)
                    print (tabulate([[applianceDoor, statusDoor, neweditedbyDoor]], ["applianceDoor", "statusDoor", "editedbyDoor"], tablefmt="grid"))
                    print (tabulate(["The door is " + statusDoor]))
                else:
                    nl()
                    print('----------------------------------------------------------')
                    statusDoor = "CLOSE"
                    updateDoorMqtt(applianceDoor, statusDoor, neweditedbyDoor, topic)
                    print("Your door has been closed!")
                    print (tabulate([[applianceDoor, statusDoor, neweditedbyDoor]], ["applianceDoor", "statusDoor", "editedbyDoor"], tablefmt="grid"))
                    print (tabulate(["The door is " + statusDoor]))

            time.sleep(10)

def main():
    starto()
main()