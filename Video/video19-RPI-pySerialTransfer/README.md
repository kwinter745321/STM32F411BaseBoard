# README.md - RPI - pySerialTransfer

January 23, 2025

Python - Serial Transfers: Deploy pySerialTransfer to Raspberry Pi OS Using Bluetooth Serial Port



Desktop
- Uses the pySerialTransfer Exxample Code displayed on the PYPI website for the pySerialTransfer 2.6.9 package.
https://pypi.org/project/pySerialTransfer/2.6.9/


RPI
- Uses the pySerialTransfer Exxample Code displayed on the PYPI website for the pySerialTransfer 2.6.9 package.
https://pypi.org/project/pySerialTransfer/2.6.9/

The Raspberry PI OS is PI4 (though any Raspberry should work.)

# Files in video 19
 
|                            |                                                                                  |
| ---------------------------| -------------------------------------------------------------------------------- |
| Desktop - Windows 11                  |                                                                                  |
|1. pip install pySerial          | serial 3.5 |
|2. pip install pySerialTransfer  | pySerialTransfer 2.6.9  |
|3. test_pst.py    | example code modified for ComPort 47 |
|                            |                                                                 
| Raspberry PI OS                     |                                                                                  |
|1. pip install pySerial          | serial 3.5 |
|2. pip install pySerialTransfer  | pySerialTransfer 2.6.9  |
|3. test_pst.py                   | example code modified for /dev/rfcomm0 |
|4. dbus-org.bluez.service        | resides in /etc/systemd/system              |
|5. rfcomm.service                | resides in /etc/systemd/system              |

