#! /usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time

TRIG = 32;
ECHO = 22;

def checkdist():
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.000001)
    GPIO.output(TRIG, GPIO.LOW)

    t0 = time.time()
    while GPIO.input(ECHO) == GPIO.LOW:
        if time.time() - t0 > 0.5:
            print("trig error")
            return 0.0
        pass

    t1 = time.time()
    while GPIO.input(ECHO) == GPIO.HIGH:
        if time.time() - t1 > 0.5:
            print("echo error")
            return 0.0
        pass

    t2 = time.time()
    return (t2-t1)*340/2

GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ECHO,GPIO.IN)
time.sleep(1)

print("wow")

try:
    while True:
        print('Distance: ',checkdist() * 100," cm")
        time.sleep(0.3)
except KeyboardInterrupt:
    GPIO.cleanup()
