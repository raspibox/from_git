#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import required modules
import time
import sys
import RPi.GPIO as GPIO

debug = 0


# define GPIO pins
GPIO_Rel1 = 16  # Pumpe
GPIO_Rel2 = 18  # 
GPIO_Rel3 = 24  # Aussenlicht                         
GPIO_Rel4 = 22                           

RelaisNum = int(sys.argv[1])
#RelaisStat = sys.argv[2]

if debug: print(RelaisNum)


if RelaisNum == 1:
  Relais = 16
elif RelaisNum == 2:
  Relais = 18
elif RelaisNum == 3:
  Relais = 24
elif RelaisNum == 4:
  Relais = 22
else:
  if debug: print('Relais ',RelaisNum, ' does not exist')
  exit 

if debug: print('Relais', Relais)
if debug: print('RelaisNum = ', RelaisNum)




# main function
if debug: print("Main")
# use GPIO pin numbering convention
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# set up GPIO pins
GPIO.setup(Relais, GPIO.OUT)
# set outpt state for relais to "high" as the are "low" enabled
Status = GPIO.input(Relais)
if debug: print ("Status is:",Status)
if Status == 0:
  print("ON")
elif Status == 1:
  print("OFF")
else:
  print("Error; wrong returncode")
  
   
# reset GPIO settings if user pressed Ctrl+C
# except KeyboardInterrupt:
#  print("Measurement stopped by user")
   #GPIO.output(Relais, RelaisStat)

#  GPIO.cleanup()