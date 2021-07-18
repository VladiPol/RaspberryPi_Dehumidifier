#!/usr/bin/python
# Copyright (c) 2017
# Author: Valdimir Poliakov
# Turn on for 10 seconds the GPIO 17 (Pin 11)
# On GPIO 17 will be setup the relay to turn on
# the analog device

import time
import RPi.GPIO as GPIO

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

# Pin 11 (GPIO 17) auf Output setzen
GPIO.setup(11, GPIO.OUT)

# LED an
GPIO.output(11, GPIO.HIGH)

# Warte 10 s
time.sleep(10)

# LED aus
GPIO.output(11, GPIO.LOW)

# Wird zum Putzen of all benoetigt
GPIO.cleanup()

# message = "End of GPIO-Script"
# print (message)