# import Pubnub, GPIO and time libraries

import sys
import RPi.GPIO as GPIO
import time
import serial
import struct

port = '/dev/ttyACM0'
# arduino = serial.Serial(port, 9600)

GPIO.setmode(GPIO.BCM)

# Set GPIO pins used on breadboard.
# rangefinder 1
TRIGONE = 20
ECHOONE = 26
# rangefinder 2
TRIGTWO = 12
ECHOTWO = 6
# Connect the libraries to your GPIO pins
print("Distance Measurement in Progess")
GPIO.setup(TRIGONE, GPIO.OUT)
GPIO.setup(ECHOONE, GPIO.IN)
GPIO.setup(TRIGTWO, GPIO.OUT)
GPIO.setup(ECHOTWO, GPIO.IN)

# Settle the trigger and wait
GPIO.output(TRIGONE, False)
GPIO.output(TRIGTWO, False)
time.sleep(2)

waitTime = 15
oldtime = time.time()
sensor1Active = False
sensor2Active = False
bothactive = False
sensor1TimeStart = None
sensor2TimeStart = None
sensor1TimeEnd = None
sensor2TimeEnd = None
pulse_one_start = None
pulse_two_start = None
pulse_one_end = None
pulse_two_end = None
boatspassed = []

standard_distance1 = 0
standard_distance2 = 0
for x in range(0, 3):
    GPIO.output(TRIGONE, True)
    time.sleep(0.00001)
    GPIO.output(TRIGONE, False)

    pulse_one_start = time.time()
    while GPIO.input(ECHOONE)==0:
        pulse_one_start = time.time()

    while GPIO.input(ECHOONE)==1:
        pulse_one_end = time.time()

    pulse_one_duration = pulse_one_end - pulse_one_start
    distance_one = pulse_one_duration*17150
    distance_one = round(distance_one, 2)

    standard_distance1 += distance_one

    GPIO.output(TRIGTWO, True)
    time.sleep(0.00001)
    GPIO.output(TRIGTWO, False)

    pulse_two_start = time.time()
    while GPIO.input(ECHOTWO)==0:
        pulse_two_start = time.time()

    while GPIO.input(ECHOTWO)==1:
        pulse_two_end = time.time()

    pulse_two_duration = pulse_two_end - pulse_two_start
    distance_two = pulse_two_duration*17150
    distance_two = round(distance_two, 2) 
    
    standard_distance2 += distance_two
    time.sleep(1)

standard_distance1 = standard_distance1 / 3
standard_distance2 = standard_distance2 / 3
 
print("setup done.....")
# Send a pulse for 10 microseconds.
while True:
    GPIO.output(TRIGONE, True)
    time.sleep(0.00001) 
    GPIO.output(TRIGONE, False)

    # Instatiate a time stamp for when a signal is detected by setting beginning + end values.
    # Then subtract beginning from end to get duration value.
    while GPIO.input(ECHOONE)==0:
        pulse_one_start = time.time()

    while GPIO.input(ECHOONE)==1:
        pulse_one_end = time.time()

    pulse_one_duration = pulse_one_end - pulse_one_start
    distance_one = pulse_one_duration*17150
    distance_one = round(distance_one, 2)
    
    if distance_one < standard_distance1 - 30:
        if sensor1Active == False:
            sensor1TimeStart = time.time()
            sensor1Active = True
    elif distance_one >= standard_distance1 - 30 and sensor1Active == True:
        sensor1Active = False
        sensor1TimeEnd = time.time()

   # pulse_duration = pulse_one_end - pulse_one_start
    GPIO.output(TRIGTWO, True)
    time.sleep(0.00001)
    GPIO.output(TRIGTWO, False)

    while GPIO.input(ECHOTWO)==0:
        pulse_two_start = time.time()

    while GPIO.input(ECHOTWO)==1:
        pulse_two_end = time.time()

    pulse_two_duration = pulse_two_end - pulse_two_start
    distance_two = pulse_two_duration*17150
    distance_two = round(distance_two, 2)
    
    if distance_two < standard_distance2 - 30:
        if sensor2Active == False:
            sensor2TimeStart = time.time()
            sensor2Active = True
    elif distance_two >= standard_distance2 - 30 and sensor2Active == True:
        sensor2Active = False
        sensor2TimeEnd = time.time() 

    if sensor1Active == True and sensor2Active == True:
        print('beide zijn actief')
        bothactive = True

    if sensor1Active == False and sensor2Active == False and bothactive == True:
        print('is actief geweest')
        boatspassed.append(waitTime - sensor1TimeStart + oldtime)
        boatspassed.append(waitTime - sensor1TimeEnd + oldtime)
        boatspassed.append(waitTime - sensor2TimeStart + oldtime)
        boatspassed.append(waitTime - sensor2TimeEnd + oldtime)
        sensor1TimeStart = None
        sensor1TimeEnd = None
        sensor2TimeStart = None
        sensor2TimeEnd = None
        bothactive = False


    # check
    if time.time() - oldtime > waitTime:
        print(waitTime, " secs have passed") 
        passingString = ""
        if(len(boatspassed) > 1):
            for p in boatspassed:
                p = int(p)
                passingString += str(p) + " "
            passingString = passingString[:-1]
            passingString += ';'
            
            print(passingString)

        del boatspassed[:]
        oldtime = time.time()
        # arduino.write("3600 3200;2200 2100")
    time.sleep(1)

# Clean up GPIO pins + reset
GPIO.cleanup()
sys.exit()