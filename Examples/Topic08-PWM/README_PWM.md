## README_PWM.md
# Perform PWM

* Platform: STM32
* Board: STM32F411CEU6 (BlackPill)
* Copyright (C) 2024 KW Services.
* MIT License
* MicroPython 1.20

## Scope.
Perform PWM on a digital pin.  

Using a timer, one can oscillate a digital pin on/off and therefore drive the brightness of an LED.

#### BlackPill for STM32F411CEU6.
Ensure the BlackPill is attached to the STM32F411 Base Board (the USB connect faces the edge).
And ensure you have MicroPython installed on the BlackPill.  See the github site for instructions
on flashing the firmware.  Make sure you have Thonny installed on your desktop.

## Perform PWM.

The example uses a digital pin at B3 to drive the brightness of an LED indicator.
For this example, we also connect a wire between a button and B10 (to start the PWM effort).

Follow these Steps:
1) Connect a wire between B3 and one of the LED indicators.
2) Connect a wire between B10 and one of the buttons. 
4) Plug your USB cable of the BlackPill into a desktop
5) Load the file bb_pyb_timer-pwm_b3.py into Thonny.
6) Click the Red STOP icon in the toolbar.
7) Click the Green Run icon in the tool bar

[Link to an example](\bb_pyb_timer-pwm_b3.py)
You should see information messages.  When you press the button the PWM duty is changed by increments of 20% and the LED glows brighter:

Quick Look:
```
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
```

Please look at the pink box next to the PB3 pin on the BlackPill diagram. 
[Link to BlackPill pin layout](images/STM32F4x1_PinoutDiagram_RichardBalint.png)

The pink box has "T2_CH2".
This means pin PB3 is associated with Channel 2 of Timer 2.  We define these objects in the code.
When ready, the function pulse_width_percent() is then set to the desired duty ("brightness").

## Conclusion.

(Once you get it to work) the IR1838 can be very useful.  This device requires some
experimentation on your part to get the components in a working state.  Then you need to 
find the best way to use the code in your project.

The base board provides a useful port for this device.

## References.

MicroPython docs 'latest' September 07, 2023: https://docs.micropython.org/en/latest/