# RPi,B Rev2 GPIO:  26-pin header
# --------------------------------
#         +3V3  1  2   +5V
# GPIO2   SDA1  3  4   +5V
# GPIO3   SCL1  5  6   GND
# GPIO4   GCLK  7  8   TXD0  GPIO14
#          GND  9  10  RXD0  GPIO15
# GPIO17  GEN0  11 12  GEN1  GPIO18
# GPIO27  GEN2  13 14  GND
# GPIO22  GEN3  15 16  GEN4  GPIO23
#         +3V3  17 18  GEN5  GPIO24
# GPIO10  MOSI  19 20  GND
# GPIO9   MISO  21 22  GEN6  GPIO25
# GPIO11  SCLK  23 24  CE0_N GPIO8
#          GND  25 26  CE1_N GPIO7

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
