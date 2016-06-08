
import OSC
import time

port = 57137
ip_adr = '224.0.0.1'


def OSCsend(adr, ch, val):
  client = OSC.OSCClient()
  OSCaddress = (ip_adr, port)

  msg = OSC.OSCMessage()

  msg.setAddress(adr)
  msg.append(ch)
  msg.append(val)
  client.sendto(msg, OSCaddress)



if __name__ == '__main__':
  try:
    while 1:
      OSCsend("/ch8", 0, 1)
      time.sleep(0.1)

  except KeyboardInterrupt:
    pass
