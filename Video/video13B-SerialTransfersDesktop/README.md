# README.md - video 13B - Serial Transfers (Desktop)


25 October 2024

This video is the start of a mini-series on Serial Transfers. Is there a better approach?  I explore the Internet and find
several promising software (python) class libraries.  We find an approach called Framing (in which we transmit a stream of bytes that are organized into a Frame.

In this video, we write the Frame and byte-stuffing code routines for the STM32.
The files are:

1. serial_loopback_test1.py             Desktop code with a pyserial loopback template 
2. desktop_serial_test1.py              Desktop code (above plus similar code from stm32)

Please make sure you have TeraTerm application deployed.

Also the Windows Bluetooth setup may require you to change another setting
Under Settings > Bluetooth & devices > Devices > Advanced

[Link to picture of Settings](Settings.jpg)