# import Pubnub, GPIO and time libraries

import sys
import RPi.GPIO as GPIO
import time
import serial
import decimal
import struct

loopcount = 0
# Set serial connection
arduinoSerialData = serial.Serial('/dev/ttyACM0', 9600)


#------------------------------
# Set up PubNub
# Put in Pub/Sub (Use your own keys!)
# Define your PubNub channel
#------------------------------
channel = 'Rangefinder'

# Interacting with the hardware:

GPIO.setmode(GPIO.BCM)

# Set GPIO pins used on breadboard.

TRIG = 20
ECHO = 26
toSend = ''
# Connect the libraries to your GPIO pins
print("Distance Measurement in Progess")
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

# Settle the trigger and wait
GPIO.output(TRIG,False)
time.sleep(2)

# Send a pulse for 10 microseconds.

while True:
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Instatiate a time stamp for when a signal is detected by setting beginning + end values.
    # Then subtract beginning from end to get duration value.

    pulse_start = time.time()
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start

    # Speed of sound at sea-level is 343 m/s.
    # 34300 cm/s = Distance/Time; 34300 cm/s = Speed of sound;
    # "Time" is there and back; divide by 2 to get time-to-object only.
    # So: 34300 = Distance/(Time/2) >>> speed of sound = distance/one-way time

    # Simplify + Flip it: distance = pulse_duration x 17150
    distance = pulse_duration*17150

    # Round out distance for simplicity and print.
    distance = round(distance, 2)
    loopcount+=1
    
    # Publish the measured distance to PubNub

    print("Distance:",distance,"cm")
    print('loopcount:', loopcount)
    if(loopcount == 13):
        print('distance to send: ', int(distance))
        toSend = int(distance)
        print('int to send: ', toSend)
        break
    
    print("Proximity Detected")
    time.sleep(1)


print('Sending data....')
result = arduinoSerialData.write(struct.pack('>B', toSend))
print('result: ', result)
# Clean up GPIO pins + reset
GPIO.cleanup()
sys.exit()
