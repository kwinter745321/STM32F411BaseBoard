## README_SDCARD.md
# Communicate with SD Card Socket

* Platform: STM32
* Board: STM32F411CEU6 (BlackPill)
* Copyright (C) 2024 KW Services.
* MIT License
* MicroPython 1.20

## Scope.

Use MicroPython Microcontrollers to read a SD Card.

>This example requires a SD Card formated as FAT32.


#### BlackPill for STM32F411CEU6.

Ensure the BlackPill is attached to the STM32F411 Base Board (the USB connect faces the edge).
And ensure you have MicroPython installed on the BlackPill.  See the github site for instructions
on flashing the firmware.  Make sure you have Thonny installed on your desktop.

## Directory listing of a SD Card.

The example uses the SPI-2 pins that are wired (using jumpers) to the SPI-2/SD Card Port.
For this example, make sure you insert a MicroSD card formated as FAT32 into the card socket.
Ideally the SD Card has one or more text files to read.

Follow these Steps:
1) Connect a wire between B10 and one of the buttons.
2) Ensure the jumpers are inserted for the SPI-2 / SD Card Port.
3) Insert a FAT32-formated MicroSD card into the Base Board card socket.
4) Plug your USB cable of the BlackPill into a desktop
5) Upload the sdcard.py file to the /flash directory on the BlackPill.
   Note:  When the BlackPill is first powered on, it displays the flash directory.
   You can simply drag-and-drop the sdcard.py file to the directory.
6) Load the file bb_pyb_test_sdcard.py into Thonny.
7) Click the Red STOP icon in the toolbar.
8) Click the Green Run icon in the tool bar

This application has several Try-Except clauses that attempt to verify the above steps occurred.
(a) Verify the sdcard library is imported
(b) Verify that a SD card is available.  

The application displays information about the configuration and awaits the press of the User Button.
Each time you press the user button, the program will perform a directory listing.

To exit, make sure your focus is in the shell pane, and click Control C.


Quick look:
```python
import pyb, sdcard, os
from pyb import LED, Pin

#CD pullup to VCC with 10K e.g. btn3
WP = None
SCK = Pin('PB13')
MISO = Pin('PB14')
MOSI = Pin('PB15')
CS = Pin('PB12')


sd = sdcard.SDCard(pyb.SPI(2), CS)
pyb.mount(sd, '/sd')
print(os.listdir('/'))
```

This exacmple performs a read.  Follow the MicroPython web site's exaplanation on how to read/write to files.

[Link to an example](/bb_pyb_uart1_send.py)



## Conclusion.

A MicroSD Card in MicroPython is relatively easy to setup and use.  The base board makes it easy to incorporate common user devices into your projects.

## References.

MicroPython docs 'latest' September 07, 2023: https://docs.micropython.org/en/latest/