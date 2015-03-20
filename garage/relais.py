#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import required modules
import time
import RPi.GPIO as GPIO

# define GPIO pins
GPIO_Rel1 = 23  # Pumpe
GPIO_Rel2 = 24
GPIO_Rel3 = 8                           
GPIO_Rel4 = 25                           
GPIO_In1 = 10                           
GPIO_In2 = 9                           
GPIO_In3 = 11  # Garagentor       1 = offen;      0 = zu                         


# function to measure the distance
def EnableRelais_Pumpe():
  # set trigger to high
  GPIO.output(GPIO_Rel1, False)
  return 1

# main function
def main():
  try:
    print("Enable Pumpen Relais")      
    Distance = EnableRelais_Pumpe()

    while True:
      In1 = GPIO.input(GPIO_In1)
      print("In1:", In1)      
      In2 = GPIO.input(GPIO_In2)
      print("In2:", In2)
      In3 = GPIO.input(GPIO_In3)
      print("In3:", In3)
      time.sleep(2)

  # reset GPIO settings if user pressed Ctrl+C
  except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.output(GPIO_Rel1, False)
    GPIO.output(GPIO_Rel2, False)
    GPIO.output(GPIO_Rel3, False)
    GPIO.output(GPIO_Rel4, False)

  GPIO.cleanup()

if __name__ == '__main__':
  # use GPIO pin numbering convention
  GPIO.setmode(GPIO.BCM)

  # set up GPIO pins
  GPIO.setup(GPIO_Rel1, GPIO.OUT)
  GPIO.setup(GPIO_Rel2, GPIO.OUT)
  GPIO.setup(GPIO_Rel3, GPIO.OUT)
  GPIO.setup(GPIO_Rel4, GPIO.OUT)
  GPIO.setup(GPIO_In1, GPIO.IN)
  GPIO.setup(GPIO_In2, GPIO.IN)  
  GPIO.setup(GPIO_In3, GPIO.IN)

  # set outpt state for relais to "high" as the are "low" enabled
  GPIO.output(GPIO_Rel1, True)
  GPIO.output(GPIO_Rel2, True)
  GPIO.output(GPIO_Rel3, True)
  GPIO.output(GPIO_Rel4, True)


  # call main function
  main()
