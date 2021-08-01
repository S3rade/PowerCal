#!/usr/bin/env python3
#import necessary modules
import os
import dweepy
import time
import EmulateGPIO as GPIO

_ = os.system("clear")

# ===================
myThing = "temp_change_sensor"  # Add value: add your dweet thing name
# ===================

# Setup hardware
# Set the desired pin numbering scheme:
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Create variables for the GPIO PINs the LEDs are connected to
# ============================================
# the PIN of the green LED
GreenLEDPin = 20  # Add values: add the pin number for the green LED
# the PIN of the red LED
RedLEDPin = 21  # Add values: add the pin number for the red LED
# =============================================

# Setup the direction of the GPIO pins - either INput or OUTput
# The PINs that connect LEDs must be set to OUTput mode:
# Prepare for initialization
GPIO.setup(GreenLEDPin, GPIO.OUT)
GPIO.setup(RedLEDPin, GPIO.OUT)
GPIO.output(GreenLEDPin, False)  # True = set 3.3V on the pin
GPIO.output(RedLEDPin,   False)  # False = set 0V on the pin
print('All LEDs are turned OFF' + '\n')

#MQTT Details
broker="iot-mqtt"
port = 1883
client = mqtt.Client("IOT-Sensor-Publisher")
client.username_pw_set(username= "root",password="kali")
certfilepath= "/root/cost_vol/scripts/cacert/ca.crt"
client.tls_set(certfilepath,tls_version=2)
client.tls_insecure_set(False)


while True:

    # Asks the user to select the LED. Put the response into a variable.
    startProg = input("Enter (o)n to start or (q) to quit: ")

    # convert the input to lowercase and put it in another variable.
    startProg1 = startProg.lower()

    # start program [ red = standby, green = active]
    if startProg1 == "o":  
        print("Activate Red LED")
        GPIO.output(GreenLEDPin, False)  # False = set 0V on the pin
        GPIO.output(RedLEDPin,   True)  # True = set 3.3V on the pin
        print('sending dweet...')
        old_dweet = dweepy.dweet_for(myThing, {"dweet": "Red"}) # this function sends data to dweet.io
        old_created = old_dweet['created'] # get the time stamp of the first dweet
        print('send dweet@', old_created + '\n')
        break

    elif startProg1 == "q":  # If the user chose to quit the program
        GPIO.output(GreenLEDPin, False)  # False = set 0V on the pin
        GPIO.output(RedLEDPin,   False)  # False = set 0V on the pin
        print('Deactivate All LEDs' + '\n')
        exit()

    else:  # If the user entered something other than r or q.
        print("Please enter (r) to start or (q) to quit.")

counter = 0

while True:
    new_dweet = dweepy.get_latest_dweet_for(myThing)  # get latest dweet
    new_created = new_dweet[0]["created"] # put the created value of the lastest dweet into a variable
    if new_created != old_created:  # check to see if the the old dweet is different from the new dweet
        counter += 1
        print(str(counter) + " New dweet detected!")
        old_created = new_created

        startProg1 == "r"
        print('receive new dweet@', new_created)
        print("Activate Green LED")
        GPIO.output(GreenLEDPin, True)
        GPIO.output(RedLEDPin,   False)
        startProg1 = "g"
        print()

        time.sleep(5)  # after 5 second delay, set LED back to red

        print("Activate Red LED")
        GPIO.output(GreenLEDPin, False)  # False = set 0V on the pin
        GPIO.output(RedLEDPin,   True)  # True = set 3.3V on the pin
        print()