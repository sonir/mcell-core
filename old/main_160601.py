#!/usr/bin/python
# -*- coding: utf-8 -*-

### SPI CONNECTION ###
# VDD -> 3.3V
# VREF -> 3.3V
# AGND -> GND
# DGND -> GND
# CLK -> SCLK(23)
# DOUT -> MISO(21)
# DIN -> MOSI(19)
# CS / SHDN -> CE0(24)

# Digital inputs : 7, 8, 10, 11, 12 ,13, 15, 16

# OSC info
# address : /ch1
# 0 ~ 7 : Digital In
# address : /ch2
# 0 ~ 7 : analog In, value : 0 ~ 1.0
# adddress : /ch3
# 0 ~ 2 : x, y, z acc
import sys
import time

import sonilab.sl_osc_send as osc
import sonilab.sl_metro
import sonilab.accelerator as acc
import sonilab.adc as adc
import sonilab.halt
from sonilab import osc_receive, event
import params
import ip_send as ip
import lib.din as din
import wait_ip
#DEVICE SETUP
DIN_MAX_NUM = 8
DIN_CH_MIN = 0
ADC_MAX_NUM = 8
ADC_CH_MIN = 0
ACC_TAP_BANK = 3
ACC_TAPPED_STATE = 1
ACC_AXIS_MAX = 3
ACC_AXIS_MIN = 0


#Instanciates
interval = 0.1
waiting = 1

#Instanciates
metro = sonilab.sl_metro.Metro(interval)
receiver = osc_receive.OscReceive(57138)
sender = osc.slOscSend(params.ip, params.port)


#OSC SETUP
ADR_DIN = "/ch1"
ADR_ADC = "/ch2"
ADR_ACC = "/ch3"
#RECEIVE
def halt(vals):
  print "halt was invoked"
  sonilab.halt.run()
  print "halt was done."

event.add("/halt",halt)
receiver.setup("/halt")



if __name__ == '__main__':
  print 'Hi mCell is here'
  while wait_ip.param("wlan0") == False:
      print 'waiting for ip'
      time.sleep(1)
  print 'IP is ready. My IP is : ',
  print wait_ip.param("wlan0")
  time.sleep(5)

  try:
    din.initGPIO()


    while True:

      #Check digital states
      for n in range(DIN_CH_MIN, DIN_MAX_NUM):
        if din.isChanged(n) == 1:
          sender.send(ADR_DIN, n, din.getValue(n))
      #measure tap
      if acc.tapDetection() == 1:
        sender.send(ADR_ACC, ACC_TAP_BANK, ACC_TAPPED_STATE)

      #Send IP Address constantly
      ip.update()

      #Send adc and acc params to sound module with interval time
      if metro.update():
        #measure analog in
        for ch in range(ADC_CH_MIN, ADC_MAX_NUM):
          val = adc.read(ch)
          sender.send(ADR_ADC,ch, val)
        #measure acc
        xyz = acc.measure()
        for i in range(ACC_AXIS_MIN, ACC_AXIS_MAX):
          sender.send(ADR_ACC, i, xyz[i])


  except KeyboardInterrupt:
      receiver.terminate()
      adc.release()
      sys.exit(0)
