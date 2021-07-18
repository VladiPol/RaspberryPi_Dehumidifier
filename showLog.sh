# This is the wrapper for the dryer
# This shell call python script to turn 
# the relay off

cd /home/pi/GPIO_Dryer

if [ -z "$1" ];
  then
    tail controlDryer.log
  else
    if [ $# -eq 1 -o "$1" -eq "$1" ] 2>/dev/null;
      then
       tail --lines=$1 controlDryer.log
    fi
fi

exit