#!usr/bin/env python3

#Dependencies
import dweepy
import EmulateGPIO as GPIO
from IPython.display import clear_output
import time
import os
import sys
from tabulate import tabulate
import random
import requests
import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime

####################






#NEW
#====================================================
# MQTT shit 
MQTT_Broker = "172.16.0.12"
MQTT_Port = 1883
Keep_Alive_Interval = 45
topic = "iot"

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


def updateFanMqtt(applianceFan, statusFan, speedFan, editedBy, topic):
	fanData = {}
	fanData['appliance'] = applianceFan
	fanData['status'] = statusFan
	fanData['speed'] = speedFan
	fanData['editedBy'] = editedBy
    #fanData['editedBy'] = editedBy
    #fanData['editedby'] = editedBy
	#Humidity_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
	fanDataJson = json.dumps(fanData)
	print("Publishing fan data... ")
	publishToTopic(topic, fanDataJson)



#====================================================









#others
_=os.system("clear") #clear screen/terminal
def nl():
	print('\n') #prints new line when function is called
####################

##################################################################
myThing = "0353B_sensor" #Add value: add your dweet thing name
##################################################################

##################################################################
#setting up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
_=os.system("clear")

#FAN
fanSwitchPin = 10
GPIO.setup(fanSwitchPin, GPIO.OUT)
GPIO.output(fanSwitchPin, False) #True = set 3.3V on the pin.
                                #False = set 0V on the pin.

fanSpeed1Pin = 11
GPIO.setup(fanSpeed1Pin, GPIO.OUT)
GPIO.output(fanSpeed1Pin,   False) #True = set 3.3V on the pin. 
                                #False = set 0V on the pin.

fanSpeed2Pin = 12
GPIO.setup(fanSpeed2Pin, GPIO.OUT)
GPIO.output(fanSpeed2Pin,   False) #True = set 3.3V on the pin. 
                                #False = set 0V on the pin.

fanSpeed3Pin = 13
GPIO.setup(fanSpeed3Pin, GPIO.OUT)
GPIO.output(fanSpeed3Pin,   False) #True = set 3.3V on the pin. 
                                #False = set 0V on the pin.

thermostatSwitchPin = 9
GPIO.setup(fanSwitchPin, GPIO.OUT)
GPIO.output(fanSwitchPin, False)

applianceFan = "Dyson Ceiling Fan"
statusFan = "OFF"
speedFan = 0 #Slow/Medium/High
editedBy = "XZ"


_=os.system("clear") #clear screen/terminal
##################################################################

print (tabulate([[applianceFan, statusFan, speedFan]], ["applianceFan", "statusFan", "speedFan"], tablefmt="grid"))
print (tabulate(["The fan is " + statusFan]))
print('----------------------------------------------------------')
print('Dweeting in progress (Dyson Ceiling Fan)...')

old_dweet = dweepy.dweet_for(myThing, {"status": statusFan, "speed" : speedFan, "editedBy" : editedBy }) #this function sends data to dweet.io
old_created = old_dweet['created'] #get the time stamp of the first dweet
print('Dweet successfully sent @' , old_created + '\n')
url = "http://172.17.0.2:8080/add/" + "fan" + "?status=" + statusFan + "&speed=%s" %speedFan + "&editedBy=" + editedBy
url1 = "http://172.17.0.2:8080/add/" + "fan" + "?status=" + statusFan + "&speed=%s" %speedFan + "&editedBy=" + editedBy
print(url) 
print(requests.put(url))
print(url1) 
print(requests.put(url1))

# url = "http://172.17.0.2:8080/add/" + "fan" + "?status=" + statusFan + "&speed=%s" %speedFan + "&editedBy=" + editedBy
# print(requests.put(url))
# updateFanMqtt(applianceFan, statusFan, speedFan, editedBy, topic)



def starto():
    global old_dweet
    global old_created
    global applianceFan
    global statusFan
    global speedFan
    global applianceThermostat
    global statusThermostat
    global tempThermostat
    global topic
    counter = 0
    global MQTT_Broker 
    global MQTT_Port 
    global Keep_Alive_Interval
    global editedBy

    while True:
        new_dweet = dweepy.get_latest_dweet_for(myThing) #get latest dweet
        new_created = new_dweet[0]["created"] #put the created value of the lastest dweet into a variable
        newStatusFan = new_dweet[0]["content"]["status"]
        newSpeedFan = new_dweet[0]["content"]["speed"]
        editedByFan = new_dweet[0]["content"]["editedBy"]
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
            print('Turn the fan ' + newStatusFan)
            print('Set speed to ' + str(newSpeedFan))
            #print(newhm)
            old_created = new_created


            if newStatusFan == "on":
                statusFan = "ON"
                if statusFan == "ON":
                    nl()
                    print('----------------------------------------------------------')
                    if newSpeedFan == speedFan:
                        statusFan = "ON"
                        print('Your fan is on and already spinning at that speed!')
                        print (tabulate([[applianceFan, statusFan, speedFan]], ["applianceFan", "StatusFan", "SpeedFan"], tablefmt="grid"))
                        print (tabulate(["The fan is " + statusFan]))
                    elif newSpeedFan == 1:
                        statusFan = "ON"
                        speedFan = 1
                        updateFanMqtt(applianceFan, statusFan, speedFan, editedByFan, topic)
                        print("Your fan's speed has been updated!")
                        print (tabulate([[applianceFan, statusFan, speedFan]], ["applianceFan", "StatusFan", "SpeedFan"], tablefmt="grid"))
                        print (tabulate(["The fan is " + statusFan]))
                    elif newSpeedFan == 2:
                        statusFan = "ON"
                        speedFan = 2
                        updateFanMqtt(applianceFan, statusFan, speedFan, editedByFan, topic)
                        print("Your fan's speed has been updated!")
                        print (tabulate([[applianceFan, statusFan, speedFan]], ["applianceFan", "StatusFan", "SpeedFan"], tablefmt="grid"))
                        print (tabulate(["The fan is " + statusFan]))
                    elif newSpeedFan == 3:
                        statusFan = "ON"
                        speedFan = 3
                        updateFanMqtt(applianceFan, statusFan, speedFan, editedByFan, topic)
                        print("Your fan's speed has been updated!")
                        print (tabulate([[applianceFan, statusFan, speedFan]], ["applianceFan", "StatusFan", "SpeedFan"], tablefmt="grid"))
                        print (tabulate(["The fan is " + statusFan]))
                else:
                    print('Your fan is not running Please turn it on first!')
                    print (tabulate([[applianceFan, statusFan, speedFan]], ["applianceFan", "StatusFan", "SpeedFan"], tablefmt="grid"))
                    print (tabulate(["The fan is " + statusFan]))
            
            elif newStatusFan == "off":
                if statusFan == "OFF":
                    nl()
                    print('----------------------------------------------------------')
                    print('Your fan is already switched off!')
                    print (tabulate([[applianceFan, statusFan, speedFan]], ["applianceFan", "Status", "Speed"], tablefmt="grid"))
                    print (tabulate(["The fan is " + statusFan]))
                else:
                    nl()
                    print('----------------------------------------------------------')
                    statusFan = "OFF"
                    speedFan = 0
                    updateFanMqtt(applianceFan, statusFan, speedFan, editedByFan, topic)
                    print("Your fan has been switched off!")
                    print (tabulate([[applianceFan, statusFan, speedFan]], ["applianceFan", "Status", "Speed"], tablefmt="grid"))
                    print (tabulate(["The fan is " + statusFan]))

                    
        
            time.sleep(10)


def main():
    starto()
main()
