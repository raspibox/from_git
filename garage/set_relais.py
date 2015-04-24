#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import required modules
import time
import sys
import RPi.GPIO as GPIO


# define GPIO pins
GPIO_Rel1 = 16  # Pumpe
GPIO_Rel2 = 18  # 
GPIO_Rel3 = 24  # Aussenlicht                         
GPIO_Rel4 = 22                           

RelaisNum = int(sys.argv[1])
RelaisStat = sys.argv[2]

print(RelaisNum)


if RelaisNum == 1:
  Relais = 16
elif RelaisNum == 2:
  Relais = 18
elif RelaisNum == 3:
  Relais = 24
elif RelaisNum == 4:
  Relais = 22
else:
  print('Relais ',RelaisNum, ' does not exist')
  exit 

print('Relais', Relais)
print('RelaisNum = ', RelaisNum)


if sys.argv[2] == "ON":
  print("Relais Status will go to Status: ON")
  RelaisStat = GPIO.LOW # Relais are low active
elif sys.argv[2] == "OFF":
  print("Relais Status will go to Status: OFF")
  RelaisStat = GPIO.HIGH
else:
  print("Planned Relais Status not defined")
print("RelaisStat:",RelaisStat,"T")


# main function
print("Main")
# use GPIO pin numbering convention
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
print(Relais ," ", RelaisStat)
# set up GPIO pins
GPIO.setup(Relais, GPIO.OUT)
# set outpt state for relais to "high" as the are "low" enabled
GPIO.output(Relais, RelaisStat) 
# reset GPIO settings if user pressed Ctrl+C
# except KeyboardInterrupt:
#  print("Measurement stopped by user")
   #GPIO.output(Relais, RelaisStat)

#  GPIO.cleanup()