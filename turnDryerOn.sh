# This is the wrapper for the dryer
# This shell call python script to check 
# the temperature and the humidity 
# every minute with DHT11 Sensor.
# If the the humidity > 65% the dryer
# will be turn on

cd /home/pi/GPIO_Dryer
sudo ./controlDryer.py
exit