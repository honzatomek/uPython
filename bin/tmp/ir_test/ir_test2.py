from machine import Pin, Timer
from time import ticks_us, ticks_diff

TIMEOUT_MS = 2000

class WatchDog():
  def __init__(self):
    self.__value = False
  def start(self):
    self.__value = True
  def stop(self):
    self.__value = False
  def value(self):
    return self.__value

def timer_callback(t):
  WD.stop()

if __name__ == '__main__':
  WD = WatchDog()
  tim = Timer(-1)
  num = 0
  ir = Pin(4, Pin.IN)
  ir.off()
  val = ir.value()
  signal = ['N L Time']
  tim1 = ticks_us()
  tim2 = tim1
  WD.start()
  tim.init(mode=Timer.ONE_SHOT, period=TIMEOUT_MS, callback=timer_callback)
  while WD.value():
    if ir.value() is not val:
      tim2 = ticks_us()
      val = not val # ir.value()
      num += 1
      signal.append('{0} {1} {2}'.format(str(num), str(val), str(ticks_diff(tim2, tim1))))
      tim1 = tim2
    pass
  print('Signal:')
  #print('\n'.join(['\t'.join(f) for f in signal]))
  #print(str(signal))
  print('\n'.join(signal))
