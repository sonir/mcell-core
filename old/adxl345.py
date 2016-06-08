import smbus
import time

class adxl345:
  def __init__(self):
    self.bus = smbus.SMBus(1)
    self.address = 0x1D
    self.xyz_adr = [0x32, 0x34, 0x36]

    self.bus.write_byte_data(self.address, 0x2D, 0x08)

    self.bus.write_byte_data(self.address, 0x2E, 0x70)    #Enable interrupt
    self.bus.write_byte_data(self.address, 0x2A, 0x07)    #Enable all axies
    self.bus.write_byte_data(self.address, 0x1D, 0x30)    #tap threshould, 62.5 mg/LSB
    self.bus.write_byte_data(self.address, 0x21, 0x10)    #tap duration, 625us/LSB
    self.bus.write_byte_data(self.address, 0x22, 0x10)    #tap latency, 1.25ms/LSB
    self.bus.write_byte_data(self.address, 0x23, 0x50)    #tap window, 1.25ms/LSB



  def measure_acc(self):
    self.acc = [ 0, 0, 0]
    for i in range(0, 3):
      #read lower bytes of each axis
      self.acc0 = self.bus.read_byte_data(self.address, self.xyz_adr[i])
      #read higher bytes of each axis
      self.acc1 = self.bus.read_byte_data(self.address, self.xyz_adr[i]+1)

      #unite 2byte datas into 10byte
      self.acc[i] = (self.acc1 << 8) + self.acc0

      #check if 10th byte is 10
      if self.acc[i] > 0x1FF:
        #minus
        self.acc[i] = (65536 - self.acc[i]) * -1

      self.acc[i] = self.acc[i] * 3.9/1000    #range -1 to 1
      self.acc[i] = self.acc[i] + 1.0
      self.acc[i] = self.acc[i]/2.0 #range 0 to 1

    return self.acc

  def tapDetection(self):
      self.tap = 0
      self.tap = self.bus.read_byte_data(self.address, 0x30)
      self.tap -= 131 #Remove DATA_READY(128), Watermark(2), and Overrun(1) values

      if self.tap == 64:
          return 1   #tap detected
      else:
          return 0


if __name__ == '__main__':
  try:
    acc = dev_adxl345.adxl345()

    while 1:
      if acc.tapDetection() == 1:
        print 'detect your tap!'

      print acc.measure_acc()
      time.sleep(0.1)

  except KeyboardInterrupt:
    pass
