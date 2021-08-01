#!/usr/bin/env python3
# import necessary modules
import os
import dweepy
import time
import random
import EmulateGPIO as GPIO

_ = os.system("clear")

# ===============================
myThing = "temp_increase_sensor"  # label for communication with dweet.io
# ===============================

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
# Prepare for initilization
GPIO.setup(GreenLEDPin, GPIO.OUT)
GPIO.setup(RedLEDPin, GPIO.OUT)
GPIO.output(GreenLEDPin, False)  # True = set 3.3V on the pin
GPIO.output(RedLEDPin,   False)  # False = set 0V on the pin
print('All LEDs are turned OFF' + '\n')
print(" ")

# main function
def getCurrentTemp():

    GPIO.output(GreenLEDPin, False)  # False = set 0V on the pin
    GPIO.output(RedLEDPin,   True)  # True = set 3.3V on the pin
    print("Activate Red LED") # Red LED for Standby Mode
    print(" ")

    for i in range(4):
        # auto generate temp for input
        tempRange = str(random.randrange(10, 25))

        # print temperature from input
        print("The current temperature is " + (tempRange) + ' degrees.')
        newTempRange = int(tempRange)

        GPIO.output(GreenLEDPin, True)  # True = set 3.3V on the pin
        GPIO.output(RedLEDPin,   False)  # False = set 0V on the pin
        print("Activate Green LED") # Green LED for Checking Temperature (working)

        # conditional statements
        if newTempRange >= 20 and newTempRange <= 25:
            category = "Warm"
            print("The temperature is categorized as " + category)
            print("It is recommended for you to turn off your warmer.")
        elif newTempRange >= 16 and newTempRange <= 19:
            category = "Average"
            print("The temperature is categorized as " + category)
            print("It is recommended for you to turn off the warmer if you're feeling warm.")
        elif newTempRange >= 13 and newTempRange <= 15:
            category = "Cold"
            print("The temperature is categorized as " + category)
            print("It is recommended for you to turn on your wamer.")
        elif newTempRange <= 12:
            category = "Freezing"
            print("The temperature is categorized as " + category)
            print("It is recommended for you to turn on your warmer.")

        # this function sends data to dweet.io
        send_dweet = dweepy.dweet_for(myThing, {"dweet": "Temperature Change"})
        # get the time stamp of the first dweet
        dweet_created = send_dweet['created']
        print("send dweet@" + dweet_created + "\n")
        time.sleep(5)

    GPIO.output(GreenLEDPin, False) # True = set 3.3V on the pin
    GPIO.output(RedLEDPin,   False) #False = set 0V on the pin
    print('Deactivate All LEDs' + '\n') #close all LEDs after process finishes

getCurrentTemp()  # call function