#!/usr/bin/python
# Copyright (c) 2017
# Author: Valdimir Poliakov
# Check the temperature and the humidity 
# every time_to_sleep (s. below) with DHT11 Sensor
# If the humidity > humidity_alert (for example 65%) turn the dryer on
# with help of relay

import sys
import time
import datetime
import logging

from logging.handlers import TimedRotatingFileHandler

import Adafruit_DHT as ADHT
import RPi.GPIO as GPIO

# The humidity alert in %
humidity_alert = 65
# The humidity calibration in % for sensor
humidity_alert_calibration = 25
# The temperature  calibration in Grad Celcius for sensor
temperature_alert_calibration = 0


# The humidity dictionary for On/Off test 
humidity_test = [55, 65, 70, 64, 64, 66, 55]

# GPIO Schema
# 123xxxxxxxxxx
# xxx4x5xxxxxx6
######################################
# 1 - orange (relay plus oder VCC)
# 2 - blue   (DHT minus or Ground)
# 3 - red    (DHT plus)
# 4 - yellow (DHT Signal)
# 5 - green  (relay Signal)
# 6 - black  (relay minus or Ground)
######################################

####### Start of Init of DHT sensor #######
# The DHT11 Sensor is installed on the GPIO 4 (Pin 7)
sensor = ADHT.DHT11
sensor_GPIO_Nr = 4
####### End of Init of DHT sensor #########

####### Start of Init GPIO ##############
# The Relay will be set up on GPIO 17 (Pin 11)    
relay_GPIO_Pin = 11
# Time to leep in seconds (600 seconds = 10 minutes ;-)
time_to_sleep = 600
# Die GPIOs Warnings ingnorieren
GPIO.setwarnings(False)
# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)
# Pin 11 (GPIO 17) auf Output setzen
GPIO.setup(relay_GPIO_Pin, GPIO.OUT)
####### End of Init GPIO ################

########## Start of Main part ##############
# Get humidity and temperature in loop
# If the humidity > <humidity_alert> Then
# Turn the relay on Else Turn the relay off
############################################
if __name__ == '__main__':
    # Log-file-name
    log_file = 'controlDryer.log'
    
    # Create Log-File to log every day in new file
    # The old files will not be deleted
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)
    
    handler = TimedRotatingFileHandler(log_file, when="d", interval=1, backupCount=0)
    logger.addHandler(handler)  
    logger.info('Time(dd.mm.yyyy)|Temp(Celcius)|Humidity(%)')    

    #for counter in range(0, len(humidity_test)):
    while True:

        # Get humidity and temperature
        humidity, temperature = ADHT.read_retry(sensor, sensor_GPIO_Nr)

        # Calibrate sensor
        humidity = humidity - humidity_alert_calibration
        temperature = temperature - temperature_alert_calibration
        
        # Get humidity and temperature for On/Off test
        # humidity = humidity_test[counter]
        
        # Get time of messuring
        dattime = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')

        # Print humidity and temperature
        if humidity is not None and temperature is not None:
            # calibrate the 
            print('Time={0}  Temp={1:0.1f}*  Humidity={2:0.1f}%'.format(dattime, temperature, humidity))
            # logger.info('Time={0}  Temp={1:0.1f}*  Humidity={2:0.1f}%'.format(dattime, temperature, humidity))
            # new format is csv-file with '|' is delimeter for the load in the database database
            logger.info('{0}|{1:0.1f}|{2:0.1f}'.format(dattime, temperature, humidity))
        else:
            # TO DO: try to take the measuring 3 times after that in error case abort
            print('Failed to get reading humidity and temperature. Try again!')
            logger.info('Time={0}  Failed to get reading humidity and temperature. Try again!'.format(dattime))           
            sys.exit(1)        

        if humidity > humidity_alert:
            # Relais an
            GPIO.output(relay_GPIO_Pin, GPIO.HIGH)
        else:
            # Relais aus
            GPIO.output(relay_GPIO_Pin, GPIO.LOW)
            
        # Warte <time_to_sleep> seconds
        time.sleep(time_to_sleep)

    ########## End of Main part ##############

    # Wird zum Putzen of all benoetigt
    # GPIO.cleanup()
    # message = "End of GPIO-Script"
    # print (message)