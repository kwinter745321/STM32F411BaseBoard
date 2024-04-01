from pyb import Pin, Timer
import time

p = Pin('B3') # has TIM2, CH2
tim2 = Timer(2, freq=1000)
ch2 = tim2.channel(2, Timer.PWM, pin=p)
for r in range(0,100,10):
    ch2.pulse_width_percent(r)
    time.sleep(0.5)
    print(r)
ch2.pulse_width_percent(0)    
