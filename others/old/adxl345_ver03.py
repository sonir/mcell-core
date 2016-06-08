import smbus
import time

bus = smbus.SMBus(1)
address = 0x1D

xyz_adr = [0x32, 0x34, 0x36]


def init_ADXL345():
  bus.write_byte_data(address, 0x2D, 0x08)

  bus.write_byte_data(address, 0x2E, 0x70)    #Enable interrupt
  bus.write_byte_data(address, 0x2A, 0x07)    #Enable all axies
  bus.write_byte_data(address, 0x1D, 0x30)    #tap threshould, 62.5 mg/LSB
  bus.write_byte_data(address, 0x21, 0x10)    #tap duration, 625us/LSB
  bus.write_byte_data(address, 0x22, 0x10)    #tap latency, 1.25ms/LSB
  bus.write_byte_data(address, 0x23, 0x50)    #tap window, 1.25ms/LSB


def measure_acc():
  acc = [ 0, 0, 0]
  for i in range(0, 3):
    #read lower bytes of each axis
    acc0 = bus.read_byte_data(address, xyz_adr[i])
    #read higher bytes of each axis
    acc1 = bus.read_byte_data(address, xyz_adr[i]+1)

    #unite 2byte datas into 10byte
    acc[i] = (acc1 << 8) + acc0

    #check if 10th byte is 10
    if acc[i] > 0x1FF:
      #minus
      acc[i] = (65536 - acc[i]) * -1

    acc[i] = acc[i] * 3.9/1000    #range -1 to 1
    acc[i] = acc[i] + 1.0
    acc[i] = acc[i]/2.0 #range 0 to 1

  return acc

def tapDetection():
    tap = 0
    tap = bus.read_byte_data(address, 0x30)
    tap -= 131 #Remove DATA_READY(128), Watermark(2), and Overrun(1) values

    if tap == 64:
        return 1    #tap detected
    else:
        return 0


if __name__ == '__main__':
  try:
    init_ADXL345()
    while 1:
      if tapDetection() == 1:
        print 'detect your tap!'

      print measure_acc()
      time.sleep(0.1)

  except KeyboardInterrupt:
    pass
