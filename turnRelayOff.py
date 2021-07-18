#!/usr/bin/python
# Copyright (c) 2017
# Author: Valdimir Poliakov
# Turn off the GPIO 17 (Pin 11)
# On GPIO 17 should be setuped the relay 
# to turn off the analog device

import time
import RPi.GPIO as GPIO

# The Relay will be set up on GPIO 17 (Pin 11)    
relay_GPIO_Pin = 11

# Die GPIOs Warnings ingnorieren
GPIO.setwarnings(False)

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

# Pin 11 (GPIO 17) auf Output setzen
GPIO.setup(relay_GPIO_Pin, GPIO.OUT)

# Relais aus
GPIO.output(relay_GPIO_Pin, GPIO.LOW)

# Wird zum Putzen of all benoetigt
GPIO.cleanup()

# message = "End of GPIO-Script"
# print (message)
