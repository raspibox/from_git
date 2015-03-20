#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import required modules
import os
import time
import RPi.GPIO as GPIO

# define GPIO pins
GPIOTrigger = 27
GPIOEcho    = 17



# function to measure the distance
def MeasureDistance():
  # set trigger to high
  GPIO.output(GPIOTrigger, True)

  # set trigger after 10µs to low
  time.sleep(0.00001)
  GPIO.output(GPIOTrigger, False)

  # store initial start time
  StartTime = time.time()

  # store start time
  while GPIO.input(GPIOEcho) == 0:
    StartTime = time.time()

  # store stop time
  while GPIO.input(GPIOEcho) == 1:
    StopTime = time.time()

  # calculate distance
  TimeElapsed = StopTime - StartTime
  Distance = (TimeElapsed * 34300) / 2

  return Distance

# main function
def main():
  try:
    while True:
      Distance = MeasureDistance()
      
      print("Measured Distance = %.1f cm" % Distance)
      fFuellstand = 210.0 - Distance
      print("Füllhöhe          = %.1f cm" % fFuellstand)      
      
      fVolumen = 3.141 * 1 * (fFuellstand / 100)
      print("Restinhalt        = %.2f m3" % fVolumen)
      print("----")
      fVol_proz = (fVolumen / 4.9) * 100
      print (fVol_proz)

      ret=os.system("curl -d \"\" http://10.0.0.50/middleware.php/data/81a5a3e0-3919-11e4-845f-53a328f742e1.json?value=" + str(fVol_proz))
      print (ret)
      time.sleep(1)

  # reset GPIO settings if user pressed Ctrl+C
  except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()

if __name__ == '__main__':
  # use GPIO pin numbering convention
  GPIO.setmode(GPIO.BCM)

  # set up GPIO pins
  GPIO.setup(GPIOTrigger, GPIO.OUT)
  GPIO.setup(GPIOEcho, GPIO.IN)

  # set trigger to false
  GPIO.output(GPIOTrigger, False)

  # call main function
  main()
