import sonilab.sl_metro
import sonilab.sl_osc_send as osc
import sonilab.get_ip as ip
import params

interval = 3.0
metro = sonilab.sl_metro.Metro(interval)
sender = osc.slOscSend(params.ip, params.port)

#OSC_SETUP
ADR_IP_UPDATE = "/ip"

def update():
  if metro.update():
    sender.send(ADR_IP_UPDATE, ip.param("wlan0"))


