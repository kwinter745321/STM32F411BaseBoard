## README_UART.md
# Communicate with UART

* Platform: STM32
* Board: STM32F411CEU6 (BlackPill)
* Copyright (C) 2024 KW Services.
* MIT License
* MicroPython 1.20

## Scope.

UART Loopback Test for a MicroPython Microcontrollers with UART.

Send a message using UART1 and read it utilizing the loopback wire.

#### BlackPill for STM32F411CEU6.

Ensure the BlackPill is attached to the STM32F411 Base Board (the USB connect faces the edge).
And ensure you have MicroPython installed on the BlackPill.  See the github site for instructions
on flashing the firmware.  Make sure you have Thonny installed on your desktop.

## Send a message using UART1.

The example uses the UART1 pins that are wired to the UART1-BT Port.
For this example, we are not using an external Bluetooth board,

Follow these Steps:
1) Connect a wire between B10 and one of the buttons.
2) Connect a wire between the TXD and RXD sockets of the UART1-BT Port.
3) Plug your USB cable of the BlackPill into a desktop
4) Load the file bb_pyb_uart1_loopback.py into Thonny.
5) Click the Red STOP icon in the toolbar.
6) Click the Green Run icon in the tool bar

The application will display a few information messages and then wait.
Each time you press the user button, the program will send a message,
it will then read the messages (becuase of the loopback connection to itself.)

To exit, make sure your focus is in the shell pane, and click Control C.


Quick look:
```python
from pyb import UART

uart = UART(1, 9600)
uart.init(1, bits=8, parity=None, stop=1, timeout=50)

uart.write("hello")
```

On my BlackPill it was necessary to have the uart() command followed by the uart.init().  The write statement is all that is needed.


[Link to an example](/bb_pyb_uart1_send.py)




 



## Conclusion.

UART in MicroPython is relatively easy to setup and use.  The base board makes it easy to incorporate common user devices into your projects.

## References.

MicroPython docs 'latest' September 07, 2023: https://docs.micropython.org/en/latest/