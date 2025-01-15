# README.md - serial_packets

December 17, 2024

Serial-packets implements a simple Serial Transmission Protocol for Commands, Messages, and Logs.

The example "master.py" provided by the author of serial-packets only sends Commands to the slave Endpoint 20.
Since I was migrating serial-packets to MicroPython, I expanded his "master.py" example.  I liked how simple the serial-packets library made coding the master.py file.  So the MicroPython driver attempts to do the same.

Desktop
- Uses the serial-packets installed on a Python 3.11 environment.
- The master.py was enhanced to demonstrate two-way Commands/Responses and Messages.   
    - Pressing keyboard 'c' sends Commands to Endpoint 11.
    - Pressing keyboard 'm' sends Messages to Endpoint 11.

STM32
- Contains a MicroPython driver with the ability to send/receive commands and messages.
- Test program using pushbuttons and UART. 
    - Button 1 sends commands to Endpoint 2 and receives a response.
    - Button 2 sends a message to Endpoint 2.

# Files in video 17
 
|                            |                                                                                  |
| ---------------------------| -------------------------------------------------------------------------------- |
| Desktop                    |                                                                                  |
|1. pip install pyserial          | serial |
|2. pip install pyserial-asyncio  | serial asyncio  |
|3. pip install serial-packets    | utility |
|4. (copy) master.py              | Test program modified to fit our test data. |
|5. pip install keyboard          | utility for keyboard commands. |
|                            |                                                                 
| STM32                      |                                                                                  |
|1. serial_packets.py        |   put this file on the flash of the STM32                                        |
|2. test_serial_packets.py   |   File can be run on Thonny.  
|4. test_crcccitt.py         | An early program to verify the CRC16 checksum. |                                                   |
|                            |                                                                                  |

- Note: serial-packets package will install the PYPI package called "pycrc" which it uses to calculate CRC16 checksum.


# Test Data


- Desktop is endpoint 2   (Windows bluetooth on desktop)
- STM32 is endpoint 11    (UART connected to classic bluetooth-uart module)

We used the following test data:

- Integer: 15
- Boolean:  True 
- Float:   1.414
- String:  hello


# CRC16 Algorithm 

To verify the CRC16 algorithm in serial-packets, I used this website: [link](#https://www.lammertbies.nl/comm/info/crc-calculation).   This gave me same CRC's used in serial-packets.

for STM32 MicroPython, I have been using this routine:

def crc16_ccitt(crc:int, data:bytes) -> int:
    x:int=0
    for i in range(len(data)):
        x = ((crc >> 8) ^ data[i]) & 0x0ffff
        x = x ^ (x >> 4)
        crc = (crc << 8) ^ (x << 12) ^ (x << 5) ^ x
        crc = crc & 0x0ffff
    return crc

```
#msg = b'\x01\x01\x00\x00\x00\x02\x68\x65\x6c\x6c\x6f\x30\x32'
# FFFF   => val: 10:64987 hex:fddb
# xmodem => val: 10:54743 hex:d5d7 
# 1D0F   => val: 10:39700 hex:9b14 
msg = b'\x01\x01\x00\x00\x00\x02\x68\x65\x6c\x6c\x6f\x30\x32'
test = bytearray(13)
i = 0
for c in msg:
    test[i] = c
    i += 1
    
#val = crc16_ccitt(0x0, test)			#xmodem
val = crc16_ccitt(0xFFFF, test)			#0xFFFF
#val = crc16_ccitt(0x1D0F, test)			#0x1D0F
print("val: 10:%d hex:%04x "%(val,val))
# verified against an online calculator
#https://www.lammertbies.nl/comm/info/crc-calculation
```

