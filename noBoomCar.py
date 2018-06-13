# -*- coding: utf8 -*-
import RPi.GPIO as GPIO
import time
import Queue
import threading
import rddPi.distance as distance

left_go = 11
left_back = 12
right_go = 13
right_back = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(left_go, GPIO.OUT)
GPIO.setup(left_back, GPIO.OUT)
GPIO.setup(right_go, GPIO.OUT)
GPIO.setup(right_back, GPIO.OUT)
distance.init()

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

def execCommond(cmd):
    if cmd == "w":
        go()
    elif cmd == "a":
        left()
    elif cmd == "d":
        right()
    elif cmd == "s":
        back()
    else:
        stop()

def checkDistance():
    start = time.time()
    while time.time() - start <= 30:
        dis = distance.check()
        if dis != 0.0 and dis <= 30:
            runThreadExec("a")
        else:
            runThreadExec("w")
        time.sleep(.2)
    stop()
    GPIO.cleanup()

def runThreadExec(cmd):
    exeCmd = threading.Thread(target=execCommond, name='execCommond', args=(cmd,))
    exeCmd.start()

try:
    runThreadExec("w")
    checkDis = threading.Thread(target=checkDistance, name='checkDistance')
    checkDis.start()
except KeyboardInterrupt:
    GPIO.cleanup()

