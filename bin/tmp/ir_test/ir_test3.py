from machine import Pin, Timer, disable_irq, enable_irq
from time import ticks_us, ticks_diff
import micropython

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

class IRrec():
  #count = 0
  def __init__(self, pnum):
    self.ir = Pin(pnum, Pin.IN)
    self.pnum = pnum
    self.ntime = 0
    self.otime = 0
    self.diff = 0
    self.ledge = 0
    self.signal = ['L Time']
    self.tu = ticks_us
    self.td = ticks_diff
    self.start()
  def start(self):
    self.otime = self.tu()
    self.ir.irq(trigger=Pin.IRQ_FALLING|Pin.IRQ_RISING,handler=self.timeseq_isr)
  def stop(self):
    self.ir.init(mode=Pin.OUT, value=1)
  def print(self):
    print('\n'.join(self.signal))
  def timeseq_isr(self, p):
    #IRrec.count += 1
    #irq = disable_irq()
    self.ntime = self.tu()
    self.diff = self.td(self.ntime, self.otime)
    self.ledge = self.ir.value()
    self.signal.append('{0} {1}'.format(str(self.ledge), str(self.diff)))
    self.otime = self.ntime
    #enable_irq(irq)

def timer_callback(t):
  WD.stop()

if __name__ == '__main__':
  micropython.alloc_emergency_exception_buf(100)
  WD = WatchDog()
  tim = Timer(-1)
  tim.init(mode=Timer.ONE_SHOT, period=TIMEOUT_MS, callback=timer_callback)
  WD.start()
  ir = IRrec(4)
#  enable_irq()
  while WD.value():
    pass
  #disable_irq()
  ir.stop()
  ir.print()
