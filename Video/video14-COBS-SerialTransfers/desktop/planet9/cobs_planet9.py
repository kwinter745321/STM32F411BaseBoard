# desktop_uasyncio_cobs.py

"""
https://forum.micropython.org/viewtopic.php?t=7803
Serial binary data packets using COBS and uasyncio
Post by Planet9 » Thu Feb 20, 2020 5:54 pm
"""

import serial,os
from time import sleep
from random import randint
from datetime import datetime,timedelta


def ms_since(start_time):
    '''
    Returns the elapsed milliseconds since start_time parameter
    Usage:
             start_time = datetime.now()
             ms_since(start_time)
    '''
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms


def crc16_ccitt_bytes(crc:int, data:bytes):
    x:int=0
    for i in range(len(data)):
        x = ((crc >> 8) ^ data[i]) & 0xff
        x = x ^ (x >> 4)
        crc = (crc << 8) ^ (x << 12) ^ (x << 5) ^ x
        crc = crc & 0xffff
    return crc


def cob_encode(msg):
    '''
    COBS encoder/stuffer
    Input bytes are encoded such that there are no zero bytes in the output
    '''
    if type(msg) != bytes and type(msg) != bytearray:
        raise TypeError('Need bytes or bytearray input')
    code = i = 1
    code_idx = 0
    frame = bytearray( 5 + int(len(msg)*1.1) )
    for b in msg:
        if b == 0:
            frame[code_idx] = code  #FinishBlock
            code = 1
            code_idx = i
            i += 1
        else:
            frame[i] = b
            i += 1
            code += 1
            if code == 0xFF:
                frame[code_idx] = code  #FinishBlock
                code = 1
                code_idx = i
                i += 1
    frame[code_idx] = code  #FinishBlock
    return frame[0:i]



def cob_decode(frame):
    '''
    COBS decoder/unstuffer
    '''
    if type(frame) != bytes and type(frame) != bytearray:
        raise TypeError('Need bytes or bytearray input')
    msg = bytearray()
    i=0
    size = len(frame)
    try:
        print("cob_decode",frame)
        while i < len(frame):
            code = frame[i]
            i += 1
            for j in range(1,code):
                msg.append(frame[i])
                i += 1
            if code < 0xFF:
                msg.append(0)
    except:
        return b''
    return msg[0:-1]

def frame_is_valid(frm):
    '''
    The last four bytes of a decoded frame hold length and checksum (little endian)
    ***actually*** The last two bytes of a decoded frame hold CRC16 (High byte first)
    Thus a valid frame should be at least 5 bytes long
    '''
    if len(frm) < 5:
        return False
    # Message length field should tie up with received COBS frame length
    #hdr_msg_len = 256 * frm[-1] + frm[-2]
    #print("hdr_msg_len",hdr_msg_len)
    # if len(frm) != (hdr_msg_len + 4):
    #     return False
    # Test checksum
    ##csum = 256 * frm[-3] + frm[-4]
    csum = 256 * frm[-2] + frm[-1]
    # if crc16_ccitt_bytes(frm[0:-4]) != csum:
    #     return False
    check = frm[:-2]
    calc = crc16_ccitt_bytes(0, check)
    #print("Received CRC and calculated value: ", csum, calc)
    return True

def test_cobs_python_methods(iterations, verbose=False):
    '''
    Loopback test through COBS encoder and decoder
    '''
    for n in range(iterations):
        msg = bytes(os.urandom(randint(5,1000)))
        data_enc = cob_encode(msg)
        data_dec = cob_decode(data_enc)
        if verbose:
            print("Test ", n, ":")
            print("msg:", msg.hex())
            print("enc:", data_enc.hex())
            print("dec:", data_dec.hex())
        if data_dec != msg:
            print("FAIL")
            print(msg.hex())
            print("enc:", data_enc.hex())
            print("dec:", data_dec.hex())
            return
    print("Done")

'''
Methods which access the serial port
'''

def get_frame(serialport, timeout_ms):
    '''
    Build bytearray of uart characters until 0x00 received.
    If timeout occurs any characters received so far are returned.
    '''
    start_time = datetime.now()
    frame = bytearray()
    while ms_since(start_time) < timeout_ms:
        sleep(0.010)
        n = serialport.inWaiting()
        if n > 0:
            print("Read:",end="")
        for i in range(n):
            c = serialport.read(1)
            if len(c) != 0:
                if c[0] == 0:
                    if len(frame) > 0:
                        timeout = False
                        print()
                        return [frame, timeout]
                else:
                    frame.append(c[0])
                    print(" ",c,end="")
    timeout = True

    return [frame, timeout]


def send_msg(serialport, msg, verbose=False):
    '''
    Append csum and length fields to message, encode and send it!
    '''
    m = bytearray()
    for b in msg:
        m.append(b)

    csum = crc16_ccitt_bytes(0,msg)
    length = len(msg)

    m.append(csum >> 8)
    m.append(csum & 0x0FF) #low byte last for crc ccitt
    
    menc = cob_encode(m)
    if verbose:
        print("len:", length, "bytes, csum:", hex(csum))
        print("msg:", msg.hex())
        print("menc:", menc.hex())
    serialport.write([0])  # Frame delim character
    serialport.write(menc) # No 0x00 bytes in here
    serialport.write([0])  # Frame delim character
    #sleep(0.1)


def get_msg(serialport, timeout_ms, verbose=False):
    '''
    Get a frame, verify checksum
    '''
    [frame, timeout] = get_frame(serialport, timeout_ms)
    if len(frame) < 5 or timeout:
        return bytearray()
    fd = cob_decode(frame)

    if frame_is_valid(fd) == False:
        if verbose:
            print("FAIL Invalid Frame Received")
            print("rcv: ",frame.hex())
        return bytearray()
    return fd[0:-2]





# def test_cobs_loopback(serialport):
#     '''
#     Loopback test through microcontroller which should be programmed
#     to echo messages
#     '''
#     bytecnt = 0
#     start_time = datetime.now()
#     for n in range(50):
#         print("Test",n)
#         #msg = bytearray.fromhex('8501bebd000b131ac4163d93721a5b3176')
#         msg = os.urandom(randint(1022,1024))
#         print(len(msg))
#         #msg = os.urandom(10)
#         bytecnt += len(msg)
#         send_msg(serialport,msg)
#         [rcv, timeout] = get_frame(serialport, 1000)
#         if len(rcv) == 0:
#             print ("No response")
#             return
#         if len(rcv) < 3 or timeout:
#             print ("Bad response length = ",len(rcv))
#             return

#         resp = rcv
#         #print("Rx Msg:")
#         #print (resp.hex().upper())
#         #print("Rx Msg Decoded:")
#         data_dec = cob_decode(resp)
#         #print (data_dec.hex().upper())
#         if frame_is_valid(data_dec) == False:
#             print("FAIL")
#             print("msg: ",msg.hex())
#             print("rcv: ",rcv.hex())
#             print("rsp: ",data_dec.hex())
#             return
#     print("Success: ", bytecnt, "bytes echoed in", int( 10*ms_since(start_time)/1000 )/10.0, "secs")




'''
-----------------   Allow execution as a program or as a module  -----------------------
'''

if __name__ == '__main__':
    print("COBS Loopback Test")
    ser = serial.Serial(port='COM5', baudrate=38400, bytesize=8, parity='N', stopbits=1,timeout=1, xonxoff=False, rtscts=0, dsrdtr=False)
    total=0
    bad=0
    for i in range(100):
        msg = os.urandom(randint(100,400))
        send_msg(ser, msg, verbose=False)
        [rcv, timeout] = get_frame(ser, 5000)
        if len(rcv) < 5 or timeout:
            print ("Msg Sent= ", msg.hex().upper())
            print ("Bad Resp= ", rcv.hex().upper())
            bad += 1
            #throw
            continue
        
        resp = rcv
        #print ("RxFrm: ", resp.hex().upper())
        data_dec = cob_decode(resp)
        #print ("RxMsg: ", data_dec.hex().upper())
        
        crc = crc16_ccitt_bytes(0,data_dec)
        if crc != 0:
            bad += 1
            print("*** CRC Error ***")
        total += 1

        print("Good: ",total-bad," Bad: ",bad,"\n")
    ser.close()



__all__ = ["send_msg", "get_msg"]


