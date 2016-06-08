#!/usr/bin/python
# -*- coding: utf-8 -*-

#SOURCE : https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008

### SPI CONNECTION ###
# VDD -> 3.3V
# VREF -> 3.3V
# AGND -> GND
# DGND -> GND
# CLK -> SCLK(23)
# DOUT -> MISO(21)
# DIN -> MOSI(19)
# CS / SHDN -> CE0(24)

# Digital inputs
# 7, 8, 10, 11, 12 ,13, 15, 16

# OSC info
# address : /ch1
# 0 ~ 7 : Digital In
# address : /ch2
# 0 ~ 7 : analog In
# adddress : /ch3
# 0 : tap detection
# 1 ~ 3 : x, y, z acc


import OSC
import RPi.GPIO as GPIO
import smbus
import time
import sys
import spidev
import adxl345
import commands

port = 57137
ip_adr = '224.0.0.1'
#ip_adr = '133.27.22.21' #damac11
spi = spidev.SpiDev()
spi.open(0,0)

#Digital inputs
Din = [7, 8, 10, 11, 12, 13, 15, 16]
pre_din = [0, 0, 0, 0, 0, 0, 0, 0]

def readAdc(channnel):
  adc = spi.xfer2([1, (8+channnel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def convertVolts(data):
  volts = (data*3.3) / float(1023)
  volts = round(volts, 4)
  return volts

def convertValue(data):
  value = (data*3.3) / float(1023)
  value = round(value, 4)
  value = value/1023.0
  return value


def OSCsend(adr, ch, val):
  client = OSC.OSCClient()
  OSCaddress = (ip_adr, port)

  msg = OSC.OSCMessage()

  msg.setAddress(adr)
  msg.append(ch)
  msg.append(val)
  client.sendto(msg, OSCaddress)

def initGPIO():
  for i in range(0, 8):
    GPIO.setup(Din[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def isPushed(ch):
    key_in = GPIO.input(ch)
    if key_in == 0:
        return 1
    else:
        return 0


if __name__ == '__main__':
  try:
    adxl345.init_ADXL345()

    #GPIO setting
    GPIO.setmode(GPIO.BOARD)
    for n in range(0, 8):
      GPIO.setup(Din[n], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    print('Loop Started')

    while 1:
      #OSCsend("/info", 0, commands.getoutput('ifconfig'))
      #measure digital in
      for n in range(0, 8):
        sw_in = isPushed(Din[n])
        #print("D"+ str(n) +" : " + str(sw_in))
        if sw_in != pre_din[n]:
          OSCsend("/ch1", n, sw_in)

          pre_din[n] = sw_in

      #measure analog in
      for i in range(0, 8):
        data = readAdc(i)
        #print("adc  : {:8} ".format(data)),
        #print ' '
        volts = convertValue(data)
        #print("volts: {:8.2f}".format(volts))
        OSCsend("/ch2", i, data)

      #measure tap
      isTapped = adxl345.tapDetection()
      if isTapped == 1:
          #print 'detect your tap!'
        OSCsend("/ch3", 3, isTapped)

      #measure acc
      acc = adxl345.measure_acc()
      #print acc
      for i in range(0, 3):
        OSCsend("/ch3", i , acc[i])

      time.sleep(0.05)

  except KeyboardInterrupt:
      spi.close()
      sys.exit(0)
