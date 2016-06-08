#!/usr/bin/python

import RPi.GPIO as GPIO

pins = [7, 8, 10, 11, 12,13, 15, 16]
pre_status = [0, 0, 0, 0, 0, 0, 0, 0]

def initGPIO():
  GPIO.setmode(GPIO.BOARD)
  for i in range(len(pins)):
    GPIO.setup(pins[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def getValue(ch):
  key_in = GPIO.input(pins[ch])
  if key_in == 0:
    return 1
  else:
    return 0

def isChanged(ch):
  status = GPIO.input(pins[ch])
  if status == pre_status[ch]:
    return 0
  else:
    pre_status[ch] = status
    return 1

