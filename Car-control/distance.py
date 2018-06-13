#! /usr/bin/python3
# -*- coding:utf-8 -*-

' distance help raspberry to check the distance using HC-SR04 '

__author__ = ' real dirty dark '

import RPi.GPIO as GPIO;
import time as time

TRIG = 32;
ECHO = 22;

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ECHO, GPIO.IN)

# 向 TRIG 输出长于 10us 的高电平
def trig():
    GPIO.output(TRIG,GPIO.HIGH)
    time.sleep(0.000001)
    GPIO.output(TRIG,GPIO.LOW)

# 计算 ECHO 输入的高点平长度并返回(cm)
def echo():
    wait_echo = time.time()
    while GPIO.input(ECHO) == GPIO.LOW:
        if time.time() - wait_echo > 0.5:
            raise Exception("Trig Error")
        pass
    echo_in = time.time()
    while GPIO.input(ECHO) == GPIO.HIGH:
        if time.time() - echo_in > 0.5:
            raise Exception("Echo Error")
        pass
    echo_out = time.time()
    return ( echo_out - echo_in ) * 340 * 100 / 2

def check():
    try:
        trig()
        return echo()
    except:
        raise;

def test():
    try:
        print("--- START ---")
        init()
        time.sleep(1)
        for i in range(1000):
            dis = check()
            time.sleep(.2)
            print("dis: ", dis,"cm")
        print("--- END ---")
    except BaseException as err:
        print(err)
        GPIO.cleanup()

if __name__ == '__main__':
    test()