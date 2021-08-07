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
#Username and password to connect
client.username_pw_set(username= "root",password="kali")
#Cacert files parameters
certfilepath= "/root/cost_vol/scripts/cacert/ca.crt"
client.tls_set(certfilepath,tls_version=2)
client.tls_insecure_set(False)
#appliance_list defined for later use in functions below
appliance_list = ['Aircon', 'TV']

#MQTT Functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code".format(str(rc)))
    client.subscribe("iot")

def on_message(client, userdata, msg):
    Messagereceived = True
    #Converting the payload to string first then stripping the first 2 characters and the last one
    apayload = str(msg.payload)
    newpayload = apayload[2:-1]
    appliance_msg = newpayload
    print (appliance_msg) #//For testing

    #Spliting the message by the delimiter and sorting it
    split_msg = appliance_msg.split(":")
    #split_msg_sorted = sorted(split_msg)
    #print(split_msg_sorted)  #/For testing

    #Appending the splitted messages into variables
    appliance_name = split_msg[0].split(":")
    appliance_status = split_msg[1].split(":")
    
    #print (appliance_list) //For testing

    #If appliance name inside
    #Converting to string and stripping first 2 and last 2 characters
    appliance_name = str(appliance_name)
    appliance_name = appliance_name[2:-2]
    #print(appliance_name, appliance_status)
    #Converting the status into string and stripping first 2 and last 2 characters
    appliance_status = str(appliance_status)
    appliance_status = appliance_status[2:-2]
    #print (appliance_status) //For testing
    #print (appliance_name) //For testing

    if appliance_name in appliance_list:
        #Translating the position of the appliance name into the appliance_list
        position = appliance_list.index(appliance_name)
        

        #Since python arrays start with 0, we start with 1 to make it same as the device_id
        position = position + 1
        device_id = str(position)

        if appliance_status == "OFF":
            deviceStatus = "0" 
            os.system('curl http://172.16.0.13:8080/db/update/'+device_id+'?"Status='+deviceStatus+'"')
            Messagereceived=False #Loop breaking
        else:
            deviceStatus = "1"
            os.system('curl http://172.16.0.13:8080/db/update/'+device_id+'?"Status='+deviceStatus+'"')
            Messagereceived=False #Loop breaking
    else:
        print("Appliance name not recognised")
        print ("Adding Appliance into the Database") #Since appliance not recognised, we need to add it into the db
        if appliance_status == "OFF":
            deviceStatus = "0" 
            os.system('curl http://172.16.0.13:8080/db/add/'+ appliance_name+'?"Status='+deviceStatus+'"')
            appliance_list.append(appliance_name) #Once added, append the new appliance name into the appliance_list to make the list updated and remove double adding
            Messagereceived=False
            #print(appliance_list)
        else:
            deviceStatus = "1"
            os.system('curl http://172.16.0.13:8080/db/add/'+ appliance_name+'?"Status='+deviceStatus+'"')
            appliance_list.append(appliance_name) #Once added, append the new appliance name into the appliance_list to make the list updated and remove double adding
            Messagereceived=False
            #print(appliance_list)


connected=False

client.username_pw_set(username="root",password="kali") #Username and password for authentication
client.on_connect = on_connect #Define callback function for successful connection
client.connect(broker) #Connection params
client.on_message = on_message # Define callback function for receipt of a message
client.loop_start()
while connected != True:
    time.sleep(0.1) #Breaks the loop when connected = false
    
while Messagereceived != True:
    time.sleep(0.1) #Breaks the loop when Messagereceived = false
client.loop_stop()
