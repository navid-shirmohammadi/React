import RPi.GPIO as GPIO
import time

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
p.start(3)
delay_time = 0.5

try:
	for i in range(4, 11):
		p.ChangeDutyCycle(i)
		time.sleep(delay_time)
	for i in range(9, 2):
		p.ChangeDutyCycle(i)
		time.sleep(delay_time)

except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()
