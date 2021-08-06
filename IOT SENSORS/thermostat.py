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
# MQTT setup 
MQTT_Broker = "172.17.0.4"
MQTT_Port = 8883
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

def updateThermostatMqtt(applianceThermostat, statusThermostat, tempThermostat, editedBy, topic):
	thermostatData = {}
	thermostatData['appliance'] = applianceThermostat
	thermostatData['status'] = statusThermostat
	thermostatData['temp'] = tempThermostat
	thermostatData['editedBy'] = editedBy
	thermostatDataJson = json.dumps(thermostatData)
	print("Publishing thermostat data... ")
	publishToTopic(topic, thermostatDataJson)
#====================================================

#====================================================
#TELEGRAM BOT
def telegram_bot_sendtext(bot_message):

    bot_token = '1901275375:AAES0FFP74rtGuXr9BHAk5RFTtWXnv3akyE'
    bot_chatID = '-554653012'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    #print("TESTING")

    return response.json()
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


#THERMOSTAT
thermostatSwitchPin = 9
GPIO.setup(thermostatSwitchPin, GPIO.OUT)
GPIO.output(thermostatSwitchPin, False)

applianceThermostat = "Nest Thermostat"
statusThermostat = "ON"
tempThermostat = 15 #Slow/Medium/High
editedBy = "XZ"


_=os.system("clear") #clear screen/terminal
##################################################################

print (tabulate([[applianceThermostat, statusThermostat, tempThermostat]], ["ApplianceThermostat", "StatusThermostat", "TemperatureThermostat"], tablefmt="grid"))
print (tabulate(["The thermostat is " + statusThermostat]))
print('----------------------------------------------------------')
print('Dweeting in progress (Nest Thermostat)...')

old_dweet = dweepy.dweet_for(myThing, {"status": statusThermostat, "temp" : tempThermostat, "editedBy" : editedBy }) #this function sends data to dweet.io
old_created = old_dweet['created'] #get the time stamp of the first dweet
print('Dweet successfully sent @' , old_created + '\n')
url = "http://172.17.0.2:8080/add/" + "thermostat" + "?status=" + statusThermostat + "&temp=%s" %tempThermostat + "&editedBy=" + editedBy
url1 = "http://172.17.0.2:8080/add/" + "thermostat" + "?status=" + statusThermostat + "&temp=%s" %tempThermostat + "&editedBy=" + editedBy
print(requests.put(url))
print(requests.put(url1))

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
        newStatusThermostat = new_dweet[0]["content"]["status"]
        newTempThermostat = new_dweet[0]["content"]["temp"]
        editedByThermostat = new_dweet[0]["content"]["editedBy"]
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
            print('Turn the thermostat ' + newStatusThermostat)
            print('----------------------------------------------------------')
            #print(newhm)
            old_created = new_created

            if newStatusThermostat == "on":
                tempThermostat = newTempThermostat
                statusThermostat = newStatusThermostat
                updateThermostatMqtt(applianceThermostat, statusThermostat, tempThermostat, editedByThermostat, topic)
                if tempThermostat >= 25:
                    url = 'https://dweet.io/dweet/for/costfan'
                    myobj = {'status': 'on', 'speed': '2'}

                    print('----------------------------------------------------------')
                elif tempThermostat < 25:
                    url = 'https://dweet.io/dweet/for/costfan'
                    myobj = {'status': 'off', 'speed': '0'}


                    print('----------------------------------------------------------')
                nl()
               
                print (tabulate([[applianceThermostat, statusThermostat, tempThermostat]], ["Appliance", "Status", "Temperature"], tablefmt="grid"))
                print (tabulate(["The thermostat is " + statusThermostat]))

            elif newStatusThermostat == "off":
                if statusThermostat == "OFF":
                    nl()
                    print('----------------------------------------------------------')
                    print('Your thermostat is already switched off!')
                    print (tabulate([[applianceThermostat, statusThermostat, tempThermostat]], ["Appliance", "Status", "Temperature"], tablefmt="grid"))
                    print (tabulate(["The thermostat is " + statusThermostat]))
                else:
                    nl()
                    print('----------------------------------------------------------')
                    statusThermostat = "OFF"
                    tempThermostat = 0
                    print("Your thermostat has been switched off!")
                    updateThermostatMqtt(applianceThermostat, statusThermostat, tempThermostat, editedByThermostat, topic)
                    print (tabulate([[applianceThermostat, statusThermostat, tempThermostat]], ["Appliance", "Status", "Temperature"], tablefmt="grid"))
                    print (tabulate(["The thermostat is " + statusThermostat]))
        elif statusThermostat in ("ON", "on"):
            nl()
            print('----------------------------------------------------------')
            print('Current temperature:' + str(tempThermostat))
            if tempThermostat >= 25:
                url = 'https://dweet.io/dweet/for/xztest'
                myobj = {'status': 'on', 'speed': '2'}

               
                print('The temperate of the room has surpassed 25 degrees! The fan has been turned on to speed 2!!')
                print('----------------------------------------------------------')
               
                randTemp = random.randint(0, 24)
                tempThermostat = randTemp
                updateThermostatMqtt(applianceThermostat, statusThermostat, tempThermostat, editedByThermostat, topic)
                time.sleep(20)
            elif tempThermostat < 25:
                url = 'https://dweet.io/dweet/for/xztest'
                myobj = {'status': 'off', 'speed': '0'}

                #x = requests.post(url, data = myobj)
                print('The temperate of the room has gone below 25 degrees! The fan has been turned of to save electricity!!')
                print('----------------------------------------------------------')
                
                
                randTemp = random.randint(25, 60)
                tempThermostat = randTemp
                updateThermostatMqtt(applianceThermostat, statusThermostat, tempThermostat, editedByThermostat, topic)
                time.sleep(20)
              



def main():
    starto()
main()