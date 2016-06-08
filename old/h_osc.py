import OSC

self.ip_adr = "224.0.0.1"
self.port = "58787"
self.adr = "/ch1"
self.bank = 0
self.val = 0

def init(adr, port):
  self.osc = OSC.OSCClient()
  self.dest = (adr, port)

def send(ch, *args):
  self.msg = OSC.OSCMessage()
  self.msg.append(ch)
  for i in args:
    self.msg.append(i)
  osc.sendto(msg, self.dest)


def OSCsend(adr, ch, val):
  client = OSC.OSCClient()
  OSCaddress = (ip_adr, port)

  msg = OSC.OSCMessage()

  msg.setAddress(adr)
  msg.append(ch)
  msg.append(val)
  client.sendto(msg, OSCaddress)
