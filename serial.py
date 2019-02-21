from timeit import default_timer as timer
import serial
import time

ser = serial.Serial('COM5', 9600, timeout=0, rtscts=1)

TIMEOUT = 2
START_DELAY = 3


time.sleep(START_DELAY)
start = timer()

COMMAND = '0123456789!dsa'
ser.write(bytes(COMMAND, 'ascii'))

while True:
    read = ser.read()
    now = timer()

    if read:
        if not (read in [b'\n', b'\r']):
            print(read)
            start = now

    if now - start > TIMEOUT:
        break


