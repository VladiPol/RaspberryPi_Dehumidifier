#!/usr/bin/python
# Copyright (c) 2021
# Author: Vladimir Poliakov
import sys
import time
import datetime

import Adafruit_DHT as ADHT
import RPi.GPIO as GPIO

# Schwellenwert fuer die Luftgfeuchtigkeit setzen
humidity_alert = 65
# Zeit fuer ein Pause in Sekunden (600 Sekunden = 10 Minuten ;-)
time_to_sleep = 600

####### START: Init GPIO ##############
# The DHT11 Signal Sensor ist auf dem GPIO 4 (Pin 7) 
sensor = ADHT.DHT11
sensor_GPIO_Nr = 4
# Das Relais ist auf dem GPIO 17 (Pin 11)    
relay_GPIO_Pin = 11
# Die GPIOs Warnings ingnorieren
GPIO.setwarnings(False)
# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)
# Pin 11 (GPIO 17) auf Output setzen
GPIO.setup(relay_GPIO_Pin, GPIO.OUT)
####### END: Init GPIO ##############

########## START: Main part ##############
# Luftfeuchtigkeit und Temperature 
# in der endlosen Schleife ermitteln
# Falls Luftfeuchtigkleit groesser als der Schwellenwert,
# dann wird das Relais bzw. der Luftentfeuchter eingeschaltet
############################################
if __name__ == '__main__':    
    try:
        while True:

            # Luftfeuchtigkeit und Temperature via DHT Sensor ermitteln
            humidity, temperature = ADHT.read_retry(sensor, sensor_GPIO_Nr)            
            
            # Zeit zum Protokollieren ermitteln
            dattime = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')

            # Logging in die Console
            if humidity is not None and temperature is not None:                
                print('Time={0}  Temp={1:0.1f}*  Humidity={2:0.1f}%'.format(dattime, temperature, humidity))                
            else:
                # TO DO: try to take the measuring 3 times after that in error case abort
                print('Failed to get reading humidity and temperature. Try again!')                
                sys.exit(1)        

            # Pruefen, ob der kritischen Wert der Luftfeuchtigkeit ueberschritten wurde
            if humidity > humidity_alert:
                # Relais an
                GPIO.output(relay_GPIO_Pin, GPIO.HIGH)
            else:
                # Relais aus
                GPIO.output(relay_GPIO_Pin, GPIO.LOW)
                
            # Warte <time_to_sleep> seconds
            time.sleep(time_to_sleep)

    except KeyboardInterrupt:
        # "Aufrauemen" nach dem Keyboard Interruption
        GPIO.cleanup()
        print ('End of GPIO-Script')
    except Exception as error:        
        raise error
    ########## END: Main part ############## 