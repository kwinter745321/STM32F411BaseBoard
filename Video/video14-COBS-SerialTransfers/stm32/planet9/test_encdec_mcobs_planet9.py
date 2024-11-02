# test_encdec_mcobs_planet9.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from mcobs_planet9 import cob_encode, cob_decode

def test1(msg):

    message = bytearray(len(msg))
    for i,c in enumerate(msg):
        message[i] = c
    encoded = cob_encode(message)
    decoded = cob_decode(encoded)
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
    print("COBS Encode Test")
    for i in range(1):

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