# servo motor control
import machine
import utime

# connect the hobby servo to pin D6 (12)
d6 = machine.Pin(12)
# servo motor frequency = 50 Hz
servo = machine.PWM(d6, freq=50)

# limit values are supposed to be in range <40, 115> but that remains to be tested
for i in range(40, 116):
    servo.duty(i)
    utime.sleep_ms(200)

for i in reversed(range(40, 116)):
    servo.duty(i)
    utime.sleep_ms(200)

