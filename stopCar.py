# -*- coding: utf8 -*-
import RPi.GPIO as GPIO
import time
import rddSocket.server as serverS
import Queue
import threading
import rddPi.distance as distance;

LED = 22
left_back = 11
left_go = 12
right_go = 13
right_back = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(left_go, GPIO.OUT)
GPIO.setup(left_back, GPIO.OUT)
GPIO.setup(right_go, GPIO.OUT)
GPIO.setup(right_back, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)


def LED_UP():
    GPIO.output(LED, 1)


def LED_DOWN():
    GPIO.output(LED, 0)


def LED_SHINE():
    pass


def go():
    GPIO.output(right_back, 0)
    GPIO.output(left_back, 0)

    GPIO.output(right_go, 1)
    GPIO.output(left_go, 1)


def back():
    GPIO.output(right_go, 0)
    GPIO.output(left_go, 0)

    GPIO.output(right_back, 1)
    GPIO.output(left_back, 1)


def right():
    GPIO.output(right_back, 0)
    GPIO.output(left_back, 1)

    GPIO.output(right_go, 0)
    GPIO.output(left_go, 0)


def left():
    GPIO.output(right_go, 0)
    GPIO.output(left_go, 0)

    GPIO.output(left_back, 0)
    GPIO.output(right_back, 1)


def stop():
    GPIO.output(right_back, 0)
    GPIO.output(left_back, 0)

    GPIO.output(right_go, 0)
    GPIO.output(left_go, 0)
    # GPIO.cleanup()

delay = 0.1
commonds = Queue.Queue()

def layback():
    time.sleep(delay)
    stop()

def execCommond():
    while True:
        cmd = commonds.get()
        if cmd == "w":
            go()
            layback()
        elif cmd == "a":
            left()
            layback()
        elif cmd == "d":
            right()
            layback()
        elif cmd == "s":
            back()
            layback()
        elif cmd == " ":
            stop()
        elif cmd == "q":
            stop()
            GPIO.cleanup()
            exit(0)
        else:
            stop()
            pass

def resoveCommond(cmd):
    print(cmd)
    commonds.put(cmd)
    if cmd == "q":
        exit(0)

stop()
GPIO.cleanup();