#!/usr/bin/python
# coding=utf-8
#
# Blink
#
# LED mit Vorwiderstand an Pin
#   
import RPi.GPIO as GPIO
import time
import sys


print("Start")
# Pin Nummern vervenden statt GPIO Nummern

pin 	   = int(sys.argv[1])
pin_status = sys.argv[2]


print(pin_status)
if pin_status == '1':
	print("1")	
	status = 'GPIO.HIGH'
else:
	status = 'GPIO.LOW'
print(status)

GPIO.setmode(GPIO.BOARD)

# Pin 26
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, status)


# GPIO.cleanup()
print("end")
