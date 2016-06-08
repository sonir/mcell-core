#!usr/bin/python

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


import time
import spidev

class mcp3008:
  def __init__(self):
    self.spi = spidev.SpiDev()
    self.spi.open(0,0)
    self.data = 0.0
    self.value = 0.0
    self.volts = 0.0
    self.temp = 0.0

  def readAdc(self, channel):
    self.adc = self.spi.xfer2([1,(8+channel)<<4,0])
    self.data = ((self.adc[1]&3) << 8) + self.adc[2]
    self.data = self.data/1023.0
    return self.data


  def getVolts(self):
    self.volts = (self.data * 3.3) / float(1023)
    self.volts = round(self.volts,4)
    return self.volts

  def getTemp(self):
    self.temp = (100 * self.volts) - 50.0
    self.temp = round(self.temp,4)
    return self.temp

  def getValue(self):
    self.value = (self.data*3.3) / float(1023)
    self.value = round(self.value, 4)
    self.value = self.value/1023.0
    return self.value

  def __del__(self):
    self.spi.close()


if __name__ == '__main__':
  try:
    adc = mcp3008()

    while True:
      for i in range(0, 8):
        data = adc.readAdc(i)
        print("adc  : {:8} ".format(data))
        volts = adc.getVolts()
        temp = adc.getTemp()
        print("volts: {:8.2f}".format(volts))
        print("temp : {:8.2f}".format(temp))

      time.sleep(5)

  except KeyboardInterrupt:
      pass
