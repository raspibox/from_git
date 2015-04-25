#!/usr/bin/python
# coding=utf-8
#
# Skript um die Wohnraumlüftung abzufragen
#   die Relais sind LOW-aktiv
#   
#   Derzeit sind nur die Stufen 0 & 3 implementiert; bei den anderen werden alle Relais auf HIGH gesetzt (somit wieder Stufe 1)
import RPi.GPIO as GPIO
import time
import sys

debug = 0

# Pin Nummern vervenden statt GPIO Nummern
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Set all relevant Pins to "HIGH" which switches all of - then CWL runs in level "1"
GPIO.setup(23, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)


Stufe_0 = GPIO.input(23)
Stufe_3 = GPIO.input(21)
if Stufe_0 == 0:
  if debug: 
    print ("KWL Stufe 0") 
  else:
    print("0")
elif Stufe_3 == 0:
  if debug: 
    print ("KWL Stufe 3") 
  else: 
    print("3")
else:
  if debug: 
    print ("KWL Stufe 1") 
  else: 
    print("1")




if debug: print("end")
