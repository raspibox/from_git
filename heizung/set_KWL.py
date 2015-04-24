#!/usr/bin/python
# coding=utf-8
#
# Skript um die Wohnraumlüftung zu steuern
#   die Relais sind LOW-aktiv
#   
#   Derzeit sind nur die Stufen 0 & 3 implementiert; bei den anderen werden alle Relais auf HIGH gesetzt (somit wieder Stufe 1)
import RPi.GPIO as GPIO
import time
import sys


# Pin Nummern vervenden statt GPIO Nummern
GPIO.setmode(GPIO.BOARD)

# Set all relevant Pins to "HIGH" which switches all of - then CWL runs in level "1"
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.HIGH)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.HIGH)

Pin = ""
KWL_Stufe = int(sys.argv[1])
if KWL_Stufe == 0:    
  Pin = 23
  print("Pin", Pin," auf low")
  GPIO.output(Pin, GPIO.LOW)

elif KWL_Stufe == 1:
elif KWL_Stufe == 2:
elif KWL_Stufe == 3:  
  Pin = 21
  print("Pin", Pin," auf low")
  GPIO.output(Pin, GPIO.LOW)

print("end")
