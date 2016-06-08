#!/usr/bin/python
#coding: utf-8

import RPi._GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

SW = [7, 8, 10, 11, 12, 13, 15, 16]

for i in range(0, 8):
    GPIO.setup(SW[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def isPushed(ch):
    key_in = GPIO.input(ch)
    if key_in == 0:
        return 1
    else:
        return 0

try:
    while 1:
        for i in range(0, 8):
            print i,
            print ' : ',
            print isPushed(SW[i])
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

GPIO.cleanup()
