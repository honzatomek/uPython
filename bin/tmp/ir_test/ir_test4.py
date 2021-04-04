from machine import Pin, Timer, disable_irq, enable_irq
from time import ticks_us, ticks_diff
import micropython

TIMEOUT_MS = 3000

class WatchDog():
  def __init__(self):
    self.__value = False
  def start(self):
    self.__value = True
  def stop(self):
    self.__value = False
  def value(self):
    return self.__value

class IRrec():
  def __init__(self, pin):
    self.pin=pin
    self.ir=Pin(self.pin, Pin.IN)
    self.us=ticks_us
    self.diff=ticks_diff
#    self.ltime=0
    self.times=[]
    self.values=[]
    self.start()
  def start(self):
#    self.ltime=self.us()
#    self.ir.irq(trigger=Pin.IRQ_RISING, handler=self.timeseq_rising)
#    self.ir.irq(trigger=Pin.IRQ_FALLING, handler=self.timeseq_falling)
    self.ir.irq(trigger=Pin.IRQ_FALLING|Pin.IRQ_RISING, handler=self.timeseq_irq)
  def stop(self):
    self.ir.init(self.pin, Pin.OUT)
  def timeseq_irq(self, p):
    self.values.append(1 - p.value())
    self.times.append(self.us())
#  def timeseq_rising(self, p):
#    self.value.append(1)
#    self.times.append(self.us())
#  def timeseq_falling(self, p):
#    self.value.append(0)
#    self.times.append(self.us())
  def process(self):
    for i in range(len(self.values) - 1):
      self.times[i] = self.diff(self.times[i + 1], self.times[i])
    self.times[len(self.values) - 1] = 0
  def print(self):
    print('n Signal Duration')
    print('\n'.join([str(i) + ' ' + str(self.values[i]) + ' ' + str(self.times[i]) for i in range(len(self.times))]))

def timer_callback(t):
  WD.stop()

if __name__ == '__main__':
  WD = WatchDog()
  tim = Timer(-1)
  tim.init(mode=Timer.ONE_SHOT, period=TIMEOUT_MS, callback=timer_callback)
  WD.start()
  ir = IRrec(4)
  while WD.value():
    pass
  ir.stop()
  ir.process()
  ir.print()