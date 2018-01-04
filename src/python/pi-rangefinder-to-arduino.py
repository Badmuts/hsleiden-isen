import serial
import time
import struct

port = '/dev/ttyACM0'

try:
    arduino = serial.Serial(port, 9600)
    time.sleep(2)
    print('Connection to ' + port + 'established succesfully!\n')
except Exception as e:
    print(e)

data = 0
data = arduino.write(struct.pack('>B', 3))
time.sleep(0.1)
data = arduino.write(struct.pack('>B', 7))
time.sleep(0.1)
data = arduino.write(struct.pack('>B', 2))
time.sleep(0.1)
arduino.close()
