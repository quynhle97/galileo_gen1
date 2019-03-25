#!/usr/bin/python

import mraa
import time

PWM_PIN = 5
pwm = mraa.Pwm(PWM_PIN)
pwm.period_us(2000)        # Set the period as 5000 us or 5ms

pwm.enable(True)           # enable PWM
value = 0

delta = 0.05               # Used to manipulate duty cycle of the pulse

while 1:
    
    if (value >= 1):
        # Itensity at max, need to reduce the duty cycle, set -ve delta
        value = 1
        delta = -0.05
    elif (value <=0):
        value = 0
        # Intensity at lowest, set a +ve delta
	delta = 0.05
	
    pwm.write(value) # Set the duty cycle
    
    value = value + delta

    time.sleep(0.2)
