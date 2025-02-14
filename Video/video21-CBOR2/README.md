# README.md  - video21 - Concise Binary Object Representation - CBOR2

February 14, 2025

# Serialization using Concise Binary Object Representation - CBOR2

The objective of this video was to learn more about serialization using CBOR.

Objects can sometimes be different on the desktop and a microcontroller. While doing
video 15 I learned of the issues with the Python module pickle, and that it handled data
differently on a desktop and a microcontroller. The biggest data difference is how datetime is handled on a desktop vs microcontroller.  

 So could I use CBOR2 instead. 

 I used the CBOR TAG method on the microntroller to encode datetime (with timezone).  This is
 the third "test" in the Desktop and the STM32 programs.

# Files

 | Platform | File Names        | Purpose                                                |
 | ---------| ------------------| ----------------------------------------------------------------------- |
 | desktop | cobs_volts.py      | Desktop pyserial methods to Get and Send messages based on COBS Frames. |
 |         | test_cobs_cbor2.py | Test program on desktop using CBOR2. |
 |         |                    |                                                                         |
 | STM32   | cbor               | Directory containg the downloaded micropython library for CBOR. |
 |         | mcobs_volts.py     | Microcontroller methods to Get and Send messages based on COBS Frames. |
 |         | test_mcobs_cbor.py | Test program on microcontroller using CBOR. |
 |         |                    |                                              |