# README.md - serial_packets

December 08, 2024


# Serial-Packets Endpoints
Desktop is endpoint 2   (Windows bluetooth on desktop)
stm32 is enspoint 11    (UART connected to classic bluetooth-uart module)


# Files in video 17
 
|                            |                                                                                  |
| ---------------------------| -------------------------------------------------------------------------------- |
| Desktop                    |                                                                                  |
|1. master.py                |    This is the desktop endpoint #2 program that uses the serial-packets utility. |
|2. pip install serial-packets    | utility |
|3. pip install pyserial          | serial |
|4. pip install pyserial-asyncio  | serial asyncio  |
|5.  pycrc                        |  PyCRC should be installed by serial-packets otherwise pip install pycrc   |
|                            |                                                                                  |
| STM32                      |                                                                                  |
|1. serial_packets.py        |   put this file on the flash of the STM32                                        |
|2. test_serial_packets.py   |   File can be run on Thonny.                                                     |
|                            |                                                                                  |





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

