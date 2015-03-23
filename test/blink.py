#!/usr/bin/python
# coding=utf-8
#
# Blink
#
# LED mit Vorwiderstand an Pin
#   
import RPi.GPIO as GPIO
import time

print("Start")
# Pin Nummern vervenden statt GPIO Nummern
GPIO.setmode(GPIO.BOARD)

# Pin 26
GPIO.setup(26, GPIO.OUT)
while true:
	print("26 auf low")
	GPIO.output(26, GPIO.LOW)
	time.sleep(0.5)
	print("26 auf high")
	GPIO.output(26, GPIO.HIGH)
	time.sleep(0.5)


# aufräumen
GPIO.cleanup()
print("end")
