
#!/usr/bin/python
# coding=utf-8
#
# Skript um die Aussenbeleuchtung zu steuern
#   die Relais sind LOW-aktiv
#   

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

import RPi.GPIO as GPIO
import time

print("Use Pin 24 (GPIO08)")
# Pin Nummern vervenden statt GPIO Nummern
GPIO.setmode(GPIO.BOARD)

REL3 = 24 # Relais 3 ist verbunden mit Pin 24 am Connector

GPIO.setup(REL3, GPIO.OUT)
print("Relais 3 an (LOW)")
GPIO.output(REL3, GPIO.LOW)
time.sleep(15)
print("Relais 3 wieder aus (HIGH)")
GPIO.output(REL3, GPIO.HIGH)
time.sleep(5)

# aufräumen
GPIO.cleanup()
print("end")
