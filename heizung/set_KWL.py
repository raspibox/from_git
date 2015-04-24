#!/usr/bin/python
# coding=utf-8
#
# Skript um die Wohnraumlüftung zu steuern
#   die Relais sind LOW-aktiv
#   
import RPi.GPIO as GPIO
import time

print("start 23 = grün = IN4 = Stufe 0")
# Pin Nummern vervenden statt GPIO Nummern
GPIO.setmode(GPIO.BOARD)

# Pin 23 (GPIO 11)
GPIO.setup(23, GPIO.OUT)
print("23 auf low")
GPIO.output(23, GPIO.LOW)
time.sleep(15)
print("23 auf high")
GPIO.output(23, GPIO.HIGH)
time.sleep(5)

print("start 21 = gelb = IN2 = Stufe 3")

# Pin 21 (GPIO 9)
GPIO.setup(21, GPIO.OUT)
print("23 auf low")
GPIO.output(21, GPIO.LOW)
time.sleep(15)
print("21 auf high")
GPIO.output(21, GPIO.HIGH)
time.sleep(5)

# aufräumen
GPIO.cleanup()
print("end")
