# test_ucobs_volts.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.24
#
from mcobs_volts import cobs_encode,cobs_decode

def test1(msg):
    message = bytearray(len(msg))
    for i,c in enumerate(msg):
        message[i] = c
    encoded = cobs_encode(message)
    decoded = cobs_decode(encoded)
    print("--------")
    print("Msg:", end="")
    for c in msg:
        print("%02x " % c, end="")
    print("\nEnc:", end="")
    for c in encoded:
        print("%02x " % c, end="")
    print("\nDec:", end="")
    for c in decoded:
        print("%02x " % c, end="")
    print()

if __name__ == '__main__':
    
    msg = [0x00]
    test1(msg)

    msg = [0x00, 0x00]
    test1(msg)

    msg = [0x00, 0x11, 0x00]
    test1(msg)

    msg = [0x11, 0x22, 0x00, 0x33]
    test1(msg)
    
    msg = [0x11, 0x22, 0x33, 0x44]
    test1(msg)
    
    # print(10*"-")
    # size = 256
    # ba = bytearray(size)
    # for x in range(0,size):
    #     ba[x] = x
    # test1(ba)

    # print(10*"-")
    # size = 256
    # loopsize = 2
    # cnt = 0
    # ba = bytearray(size*loopsize)
    # for y in range(0,loopsize):
    #     cnt = 256 * y
    #     for x in range(0,256):
    #         ba[x + cnt] = x
    # test1(ba)

    # msg = "hello"
    # message = bytearray(msg.encode("utf-8"))
    # test1(message)
    
    # msg = [0x68, 0x65, 0x6c, 0x6c, 0x6f]
    # test1(msg)