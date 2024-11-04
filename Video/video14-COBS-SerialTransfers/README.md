# README.md - testing COBS

Collected three sample of Python/MicroPython programs using
the Consistent Overhead Byte Stuffing (COBS) algorithm.  The algorithm was presented by Stuart Cheshire and Mary Baker in a paper (2).

Code in the programs
were altered slightly to accomodate the python versions being used.  The
Encode/Decode programs were used to ensure the driver produced the data results as suggested by Wikipedia (1).

Python code versions used in the testing:
- Python 3.9.20 (main, Oct  3 2024, 07:38:01) [MSC v.1929 64 bit (AMD64)] on win32
- pyserial 3.5
- keyboard 0.13.5
- MicroPython v1.20.0-326-gcfcce4b53 on 2023-07-26; WeAct Studio Core with STM32F411CE

The Desktop used the Python 3.9 and the STM32 used the MicroPython 1.20.  The repo contains the following files:

## Driver files (used by test programs)
The STM32 driver files must reside on the /flash directory.  The
Desktop driver files should be in the same directory as the test program.

| Platform  |  STM32   |  Desktop   | Source (see Endnote) |
| --------- | -------- | ---------- | ------ |
| cobs 1.2.1 |  mcobs121.py | cobs121.py  | (4),(5) |
| voltsandjolts | mcobs_volts.py | cobs_volts.py | (6) |
| planet9 | mcobs_planet9.py   | cobs_planet9.py   | (3) |

## Programs to Test Encode and Decode Functions
These files test the COBS encode/decode functions of the drivers.

| Platform  |  STM32   |  Desktop   |
| --------- | -------- | ---------- |
| cobs 1.2.1 |  test_encdec_ucobs121.py | test_encdec_cobs121.py  |
| voltsandjolts | test_encdec_ucobs_volts.py | test_encdec_cobs_volts.py |
| planet9 | test_encdec_ucobs_planet9.py   | test_encdec_cobs_planet9.py   |

## Programs to Test Send/Get Functions
Each program has both send and receive functions.  So, the programs can be individually tested using 'loopback' as described in Videos 13A/B.  Otherwise, the Bluetooth Module can be inserted into the STM32 Base Board and the programs
will operate wirelessly.

| Platform  |  STM32   |  Desktop   |
| --------- | -------- | ---------- |
| cobs 1.2.1 |  x | x  |
| voltsandjolts | test_mcobs_volts.py | test_cobs_volts.py |
| planet9 | test_mcobs_planet9.py   | test_cobs_planet9.py   |
| planet9 async| test_uasyncio_planet9.py   | y  |

- Note x: no send/get function   
- Note y: only asyncio for STM32 


## Acknowledgement Endnotes

1.  https://en.wikipedia.org/wiki/Consistent_Byte_Stuffing
2.  Paper: Stuart Cheshire and Mary Baker Consistent Overhead Byte Stuffing, IEEE/ACM Transactions on Networking, vol 7, No. 2, April 1999  http://www.stuartcheshire.org/papers/COBSforToN.pdf 
3.  Forum: https://forum.micropython.org/viewtopic.php?t=7803
4.  PyPI:  https://pypi.org/project/cobs/
5.  pythonhosted:  https://pythonhosted.org/cobs/
6.  EEVblog: https://www.eevblog.com/forum/microcontrollers/implementing-uart-data-packets-with-consistent-overhead-byte-stuffing-(cobs)/

