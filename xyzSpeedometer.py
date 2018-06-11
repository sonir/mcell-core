#! usr/bin/python

pre = [1.0, 1.0, 1.0]

def getSpeed(current):
  speed = [0.0, 0.0, 0.0]
  for i in range(0, 3):
    sp = abs(pre[i] - current[i])
    if sp < 0.01:
      sp = 0
    speed[i] = sp
    pre[i] = current[i]

  return speed
