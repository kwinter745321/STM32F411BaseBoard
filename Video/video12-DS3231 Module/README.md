# README.md - Video12 - Using DS3231 Module


01 October 2024

This folder contains the code files for the video12 (Using the DS3231 Module).
Information on the driver: 
[LINK](https://github.com/pangopi/micropython-DS3231-AT24C32)

The files are:
- ds3231.py                   The driver file for the ds3231 chip
- scan_machine_i2c.py         A program utility to verify that I2C is wired correctly.
- machine_example_ds3231.py   The program to test the functionaify of the driver.

Since either the ds3231 or the RTC within the STM32 can be correct or partially correct, the program checks the state of both; and updates accordingly.  The RTC date is updated from the value in the DS3231 ( so make sure to edit
the program to change the 30-sept-2024 date/time.)

This module includes an EEPROM which will be covered in video12B.


