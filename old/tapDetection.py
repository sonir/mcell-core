
### http://qiita.com/akira-sasaki/items/848b672db5d7ca647a6b

# coding: utf-8

import smbus
import time

bus = smbus.SMBus(1)
address = 0x1D

def init_ADXL345():
    #bus.write_byte_data(adress, command, value) 
    bus.write_byte_data(address, 0x2D, 0x08)

    bus.write_byte_data(address, 0x2E, 0x70)    #Enable interrupt
    bus.write_byte_data(address, 0x2A, 0x07)    #Enable all axies
    bus.write_byte_data(address, 0x1D, 0x30)    #tap threshould, 62.5 mg/LSB
    bus.write_byte_data(address, 0x21, 0x10)    #tap duration, 625us/LSB
    bus.write_byte_data(address, 0x22, 0x10)    #tap latency, 1.25ms/LSB
    bus.write_byte_data(address, 0x23, 0x50)    #tap window, 1.25ms/LSB

def tapDetection():
    tap = 0
    tap = bus.read_byte_data(address, 0x30)
    tap -= 131 #Remove DATA_READY(128), Watermark(2), and Overrun(1) values
    
    if tap == 64:
        return 1    #tap detected
    else:
        return 0


try:
    init_ADXL345()

    while(1):
        if(tapDetection() ==  1):
            print 'detect your tap!'

        time.sleep(0.005)

except KeyboardInterrupt:
    pass
