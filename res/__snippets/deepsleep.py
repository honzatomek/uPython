# embedded modules
print('\n[i] importting embedded modules')
import machine
from utime import sleep_ms

print('[i] setting up real time clock to trigger wake from deep sleep')
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

# check if the device woke from a deep sleep
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('[i] machine has been woken from deep sleep')
else:
    print('[i] machine has been woken by reset')

for i in range(5):
    print('[i] {0} seconds left to interrupt'.format(5 - i))
    sleep_ms(1000)

print('[i] entering deep sleep')
rtc.alarm(rtc.ALARM0, 1000 * 5)
machine.deepsleep()
