import time 
from time import sleep  
import RPi.GPIO as GPIO 

GPIO.setmode(GPIO.BCM)

INPUT_PINS = [21, 20, 16, 26, 19, 13, 6] 

[GPIO.setup(pin, GPIO.IN) for pin in INPUT_PINS]

while True:
    output = []
    for pin in INPUT_PINS:
        if (GPIO.input(pin) == True):
            # load is turned off.
            value = 0
        else:
            #now 20 watt load is turned ON!.
            value = 1 
        output.append(value)
    print(output)
    sleep(1) 
