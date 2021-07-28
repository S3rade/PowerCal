#! /usr/bin/env python3

import os
import time
import paho.mqtt.client as mqtt
import re
import os
_=os.system("clear" 

#MQTT Details
broker ="172.16.0.12"
port = 1883
client = mqtt.Client("IOT-WebDB-Subscriber")
client.username_pw_set(username= "root",password="kali")

#MQTT Functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)

def on_publish(client, userdata,result):
  	print ("Data is being Published \n")

def on_disconnect(client, userdata, rc):
    print("Broker has Disconnected!")

while True:
    
def on_message(client, userdata, message):
    Messagereceived =True

    appliance_msg = str(message.payload.decode("utf-8"))
    topic = str(message.topics)

    #filter by appliance name and status
    appliance_msg = appliance_msg.split(",")
    split_msg_sorted = sorted(split_msg)
    print(split_msg_sorted)

    appliance_name = split_msg_sorted[1].split(":")[1]
    appliance_status = split_msg_sorted[2].split(":")[1]

    appliance_list = ['Aircon', 'Lights']
    #If appliance name inside
    if appliance_name in appliance_list:
        position = appliance_list.index(appliance_name)
        print(position) 
        if (position == 0):
            device_id = "1"
            deviceStatus = "1"
        elif (position == 1):
            device_id = "2"
            device_status= "1"
    else:
        print("Appliance name not recognised")
    
    os.system('curl http://172.16.0.13:8080/update/'+device_id+'?"DeviceStatus='+deviceStatus+'"')
Messagereceived=False

connected=False

client.username_pw_set(username="",password="")
client.on_message = on_message
client.connect(broker)
client.on_connect = on_connect
client.subscribe("farm")
client.loop_start()
while connected != True:
    time.sleep(0.1)
    
while Messagereceived != True:
    time.sleep(0.1)
client.loop_stop()