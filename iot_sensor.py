#!/usr/bin/env python3

#Import MQTT connector module.
import paho.mqtt.client as mqtt 

# Import the dweepy module that is a collection of functions that make it  easier to communicate with dweet.io 
import dweepy

myThing = "0353B_sensor" #Add value: add your dweet thing name

# Import the GPIO modules to control the GPIO pins of the Raspberry Pi, Uncomment the following only when testing on a physcial Rasberry Pi
#Comment the following when testing on a Raspbian VM
#import RPi.GPIO as GPIO

# Import the Mock GPIO modules to control the Mock GPIO pins of the Raspberry Pi,Uncomment the following when testing on a Raspbian VM
# Comment the following when testing on a physcial Rasberry Pi
import EmulateGPIO as GPIO

# Import to clear cell output with code
from IPython.display import clear_output

# Import the time module to control the timing of your application (e.g. add delay, etc.)
import time

import os
_=os.system("clear")

#Setup hardware, Set the desired pin numbering scheme:
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Create variables for the GPIO PINs the LEDs are connected to
# the PIN of the green LED
GreenLEDPin = 20   #Add values: add the pin number for the green LED
# the PIN of the red LED
RedLEDPin   = 21   #Add values: add the pin number for the red LED

# Setup the direction of the GPIO pins - either INput or OUTput, The PINs that connect LEDs must be set to OUTput mode:
GPIO.setup(GreenLEDPin, GPIO.OUT)
GPIO.setup(RedLEDPin, GPIO.OUT)
GPIO.output(GreenLEDPin, False) # True = set 3.3V on the pin
GPIO.output(RedLEDPin,   False) #False = set 0V on the pin
print('All LEDs are turned OFF' + '\n')

#MQTT Details
broker="172.16.0.12"
port = 1883
client = mqtt.Client("IOT-Sensor-Publisher")
client.username_pw_set(username= "root",password="kali")


#MQTT Functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)

def on_publish(client, userdata,result):
  	print ("Data is being Published \n")

def on_disconnect(client, userdata, rc):
    print("Broker has Disconnected!")


while True:
	
	# Asks the user to select the LED. Put the response into a variable.
	lit = input("Is the Device on or off ? (o)n to ON or (f) to OFF ? (q) to quit: ")
    
	# convert the input to lowercase and put it in another variable.
	lit1 = lit.lower()

	#Set the LED state based on the user input
	if lit1 == "f": #If the user chose the Turn OFF the Device
		print("Turning Off the Device")
		GPIO.output(GreenLEDPin, False) # False = set 0V on the pin
		GPIO.output(RedLEDPin,   True)  # True = set 3.3V on the pin
		print('sending dweet...')

		#MQTT codes		
		client.connect(broker) #Connects to broker
		client.loop_start()
		print('Publishing ... ') 
		client.publish("iot/Aircon","OFF")		
		print('Published !')
		time.sleep(4)
		client.loop_stop()
		client.disconnect()
		

		old_dweet = dweepy.dweet_for(myThing, {"dweet": "Red"}) #this function sends data to dweet.io
		old_created = old_dweet['created'] #get the time stamp of the first dweet
		
		print('send dweet@' , old_created + '\n')
		break

	elif  lit1 == "o": #If the user chose the Turn ON the Device
		print("Turning On the Device")
		GPIO.output(GreenLEDPin, True) # True = set 3.3V on the pin
		GPIO.output(RedLEDPin,   False) #False = set 0V on the pin
		print('sending dweet...')

		#MQTT codes		
		client.connect(broker) #Connects to broker
		client.loop_start()
		print('Publishing ... ') 
		client.publish("iot/Aircon","ON")		
		print('Published !')
		time.sleep(4)
		client.loop_stop()
		client.disconnect()

		old_dweet = dweepy.dweet_for(myThing, {"dweet": "Green"}) #this function sends data to dweet.io
		old_created = old_dweet['created'] #get the time stamp of the first dweet
		print('send dweet@' , old_created + '\n')
		break

	elif  lit1 == "q": #If the user chose to quit the program
		GPIO.output(GreenLEDPin, False) # True = set 3.3V on the pin
		GPIO.output(RedLEDPin,   False) #False = set 0V on the pin
		print('Quiting Programme' + '\n')
		exit()

	else:  #If the user entered something other than o, f, or q.
		print("Please enter (o)n to ON or (f) to OFF ? (q) to quit:")



counter = 0

while True:
	new_dweet = dweepy.get_latest_dweet_for(myThing) #get latest dweet
	new_created = new_dweet[0]["created"] #put the created value of the lastest dweet into a variable
	if new_created != old_created: #check to see if the the old dweet is different from the new dweet
		counter += 1
		print(str(counter) + " New dweet detected!",end='\n')
		old_created = new_created

		if lit1 == "o":
			print('receive new dweet@' , new_created)
			print("Turning Off the Device")
			GPIO.output(GreenLEDPin, False) # False = set 0V on the pin
			GPIO.output(RedLEDPin,   True)  # True = set 3.3V on the pin
			
			#MQTT codes		
			client.connect(broker) #Connects to broker
			client.loop_start()
			print('Publishing ... ') 
			client.publish("iot/Aircon","OFF")		
			print('Published !')
			time.sleep(4)
			client.loop_stop()
			client.disconnect()

			lit1 = "f"
			print()

		elif lit1 == "f":
			print('receive new dweet@' , new_created)
			print("Turning On the Device")
			GPIO.output(GreenLEDPin, True) 
			GPIO.output(RedLEDPin,   False)
			
			#MQTT codes		
			client.connect(broker) #Connects to broker
			client.loop_start()
			print('Publishing ... ') 
			client.publish("iot/Aircon","ON")		
			print('Published !')
			time.sleep(4)
			client.loop_stop()
			client.disconnect()

			lit1 = "o"
			print()
	time.sleep(1)
