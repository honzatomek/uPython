# -*- coding: utf-8 -*-

# general imports
import sys
import os
import time

#import machine
from machine import Timer, Pin

START = time.time()
TIMEOUT_MS = 5000
TIME_LOOP = 10000


def print_callback(t):
  now = time.time()
  print('{0} s - This is callback'.format(now - START))


def main():
  tim = Timer(1)
  tim.init(mode=Timer.PERIODIC, period=TIME_LOOP, callback=print_callback)
#  tim.init(mode=Timer.ONE_SHOT, period=TIMEOUT_MS, callback=print_callback)
  led = Pin(2, Pin.OUT, 1)
  for i in range(60):
    now = time.time()
    print('{0} s : {1} - This is main loop.'.format(now - START, i))
    led.value(not led.value())
    time.sleep(1)
  tim.deinit()
  led.value(1)
  
  
if __name__ == '__main__':
  main()