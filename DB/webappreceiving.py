#! /usr/bin/env python3

import os
import time
import paho.mqtt.client as mqtt
import re
_=os.system("clear")

#MQTT Details
broker="172.16.0.12"
port = 1883
client = mqtt.Client("IOT-DB-Subscriber")
client.username_pw_set(username= "root",password="kali")
certfilepath= "/root/iot_vol/scripts/cacert/ca.crt"
client.tls_set(certfilepath,tls_version=2)
client.tls_insecure_set(False)
appliance_list = ['Airycon', 'Lights']

#MQTT Functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code".format(str(rc)))
    client.subscribe("iot")

def on_message(client, userdata, msg):
    Messagereceived = True
    apayload = str(msg.payload)
    newpayload = apayload[2:-1]
    appliance_msg = newpayload
    #print (appliance_msg)
    #filter by appliance name and status
    split_msg = appliance_msg.split(":")
    split_msg_sorted = sorted(split_msg)
    #print(split_msg_sorted)
    appliance_name = split_msg_sorted[0].split(":")
    appliance_status = split_msg_sorted[1].split(":")
    #print (appliance_list)
    #If appliance name inside
    appliance_name = str(appliance_name)
    appliance_name = appliance_name[2:-2]
    print (appliance_name)
    print(appliance_list)
    if appliance_name in appliance_list:
        position = appliance_list.index(appliance_name)
        appliance_status = str(appliance_status)
        appliance_status = appliance_status[2:-2]
        print (appliance_status)
        position = position + 1
        device_id = str(position) 
        if appliance_status == "OFF":
            deviceStatus = "0"
            os.system('curl http://172.16.0.13:8080/db/update/'+device_id+'?"Status='+deviceStatus+'"')
            Messagereceived=False
        else:
            deviceStatus = "1"
            os.system('curl http://172.16.0.13:8080/db/update/'+device_id+'?"Status='+deviceStatus+'"')
            Messagereceived=False
    else:
        deviceStatus= "0"
        print("Appliance name not recognised")
        print ("Adding Appliance into the Database")
        os.system('curl http://172.16.0.13:8080/db/add/'+appliance_name+'?"Status='+deviceStatus+'"')
        appliance_list.append(appliance_name)
        Messagereceived=False
        print(appliance_list)


connected=False

client.username_pw_set(username="root",password="kali")
client.on_connect = on_connect
client.connect(broker)
client.on_message = on_message
client.loop_start()
while connected != True:
    time.sleep(0.1)
    
while Messagereceived != True:
    time.sleep(0.1)
client.loop_stop()