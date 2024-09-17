# README.md - VL53L1X Video 11B

16 August 2024

This video is a continuation of the Video 11.  Though the driver is from a different author.  The hardware is an upgrade (VL53L1X) over the previous VL53L0X device.

The test file and driver used in today's video is from drakxtwo's GitHub site.  (https://github.com/drakxtwo/vl53l1x_pico).  The author is Lee Halls.  He implemented this software three years ago for MicroPython on a Raspberry Pi Pico.

I also tested the Arduino code for VL53L1X on an ESP32-WROOM device and it worked well.

The program TOF400Ftest.py is the main client-side program.  This is run in Thonny.  I feel the driver is getting hung in the MicroPython code.  Which is why the MP Forum suggested i needed pull-up resistors.  Though I feel the board already had the resistors (and anyway it worked for Arduino.) Despite this i tried adding 10K resistors pulled up to 3.3volts, and the connection crashed.

There could be an issue with the MP driver on STM32 as one of the driver init bytes was indeed different from how Arduino init the device. (Alas I tried this change as well and there was no difference.)  Probably I missed the obvious.

So that is why I posted the code as it might just work.

17 September 2024

I tried using a different vendor's VL53L1X board (this time from Amazon).
The board is twice the cost of the Chinese-supplied device.  Its well made.
Unfortunately it responded exactly the same as the other device.

I did a lot of testing and did not want to clutter this site.  As the results ultimately were the same.


Files for the video 11B:
1. vl53l1x.py                                   (put on MCU's drive.)
2. TOF400Ftest.py                               (can be run from Thonny).
3. scan_machine_I2c.py                          My test program to verify I2C address.


Test-data
1. run1.csv                                     One of the first runs.  it shows the initialization and several reads()

DataSheet
1. vl53l1x.pdf                                  Datasheet on the device.

