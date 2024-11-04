# uasyncio_cobs_planet9.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.24
#

"""
https://forum.micropython.org/viewtopic.php?t=7803
Serial binary data packets using COBS and uasyncio
Post by Planet9 » Thu Feb 20, 2020 5:54 pm

"""
###################################

"""
This code will only run in MicroPython and it requires the uasyncio module.

This is a MicroPython implementation of Consistent Overhead Byte Stuffing,
an efficient method of creating binary data packets for transfer over a serial
channel. For details do an internet search for this openly available paper:
Cheshire & Baker, Consistent Overhead Byte Stuffing filetype:pdf
IEEE/ACM TRANSACTIONS ON NETWORKING, VOL.7, NO. 2, APRIL 1999

The UartCobs class provides methods for binary data packet transfer over UART with CRC protection
The code below is a simple example which just echos back any valid packet recieved.
Import to run.
"""

import uasyncio as asyncio
from machine import Pin, UART
import os, pyb
#from asyn import Event
from uasyncio import Event


class UartCobs():

    def __init__(self, uartn:int, baud:int, max_tx_len, max_rx_len):
        """Note the UART receive ring buffer (read_buf_len) should be
        appropriate for size and rate of incoming COBS frames
        """
        self._max_tx_len = max_tx_len + round(max_tx_len/5) + 7 # Allow space for two byte CRC and COBS formatting bytes
        self._max_rx_msg_len = max_rx_len + 3 # Allow space for two byte CRC and the COBS phantom byte
        self._max_frame_rx_len = max_rx_len + round(max_rx_len/5) + 5 # Received frame will have CRC and COBS formatting bytes
        
        self.uart = UART(uartn)
        #You may need to increase uart rx ringbuffer depending on demand for processor time by other tasks, default is 64 bytes
        self.uart.init(baudrate = baud, bits=8, parity=None, stop=1, timeout=0, flow=0, timeout_char=0, read_buf_len=128)
        self._swriter = asyncio.StreamWriter(self.uart, {})
        self._txfrm = bytearray(self._max_tx_len)
        self.rxmsg = bytearray(self._max_rx_msg_len)
        self.reply = bytearray(self._max_tx_len)
        self.reply_len = 0
        self.result = bytearray(self._max_rx_msg_len)

    async def send(self, txmsg:bytearray, msg_len):
        """Task for encoding and sending COBS frames over the UART
        txmsg muust have space for the two byte CRC to be appended
        """
        crc = self._crc16_ccitt(0,txmsg,msg_len)      
        txmsg[msg_len] = crc >> 8
        txmsg[msg_len+1] = crc % 256
        msg_len += 2
        frame_len = self._encode(txmsg, msg_len)
        print("*** Send Frame:",self._txfrm[0:frame_len] )
        print("*** Send CRC:",crc)
        await self._swriter.awrite(self._txfrm, 0, frame_len)


    async def _getbyte(self):
        #Using await streamreader here was very slow, so using
        #this method which will hog processor until the uart ringbuffer is emptied.
        #Shouldn't be an issue since uart comms is relatively slow.
        sreader = asyncio.StreamReader(self.uart)
        # if self.uart.any() > 0:
        #     await asyncio.sleep_ms(2) #Be careful not to overflow uart ringbuffer (2ms at 115Kbaud is about 23 bytes) but other tasks may keep processor for longer           
        #     return self.uart.read(1)
        # else:
        #     return None
        while True:
            res = await sreader.read(1)
            return res


    async def receive(self, event_rx):
        """State machine task for COBS receiver"""
        rxpkt = self.rxmsg
        while True:
            while True:   #Wait for 0x00 frame start
                c = None
                while c == None:
                    c = await self._getbyte()
                print("-----Receive2",c)
                if ord(c) == 0:
                    break
                await asyncio.sleep_ms(2)
            while True:   #Wait for non-zero byte (the first code byte of a frame)
                c = None
                while c == None:
                    c = await self._getbyte()
                
                if ord(c) != 0:
                    break
                await asyncio.sleep_ms(2)

            cnt=0 #count of bytes decoded from the frame and output to the packet
            while True:
                #Start a new COBS block because of new frame or
                #we just finished a block in the current frame
                if c == None:
                    break
                code = ord(c)
                i=1
                print("-----Receive4",c,ord(c))
                rxpkt[cnt] = code
                cnt = cnt + 1
                while i < code:
                    c = None
                    while c == None:
                        c = await self._getbyte()
                    print("-----Receive5",c,ord(c))
                    i += 1
                    rxpkt[cnt] = ord(c)
                    print("----Receive5b cnt",cnt,c,ord(c),rxpkt[cnt])
                    
                    cnt = cnt + 1
                    if ord(c) == 0:
                        #print("rxpkt",rxpkt)
                        break

                if ord(c) == 0:
                    #Finish this frame
                    if cnt > 0:
                        cnt -= 1 #remove the phantom trailing 0 that cobs produces                   
                    if self._crc16_ccitt(0,rxpkt,cnt) == 0:
                        ######val = cnt - 2
                        pass
                    ###### added #######################
                    rxpkt = self._decode(rxpkt)
                    rxpkt = trim_zeros(rxpkt)
                    size = len(rxpkt)
                    ii = 0
                    for c in range(size-2):
                        self.result[ii] = rxpkt[ii]
                        ii = ii + 1
                    #await self.send(self.reply,self.reply_len)
                    # ready for to receive another frame
                    event_rx.set()
                    break

                #Finish this block
                if code < 0xff:
                    print("Receive6 finished payload:",trim_zeros(rxpkt))
                    rxpkt[cnt]=0
                    cnt += 1


                while c == None:
                    c = await self._getbyte()
                    print("ReceiveZ",c,ord(c))

        
    def _encode(self, msg, len):
        """COBS Encoder
        Process input message bytes to create a COBS frame with CRC protection
        Output frame will have 0x00 in first and last byte and no other zero bytes
        
        Keyword arguments:
        msg -- message in bytearray. Must have space for this encoder to append 2-byte CRC.
        len -- num bytes in msg (specify length so statically allocated buffer can be used)
        frame -- pre-allocated bytearray long enough to hold the output frame
                frame length will not exceed 5 + int(len(msg)*1.1)
                output will have COBS encoded message with 0x00 frame delimiters
        """
        frame = self._txfrm       
        assert type(msg) == bytearray
        assert type(frame) == bytearray
        frame[0]=0
        n = 2
        code = 1
        code_idx = 1
        for i in range(len):
            b=msg[i]
            if b == 0:
                frame[code_idx] = code  #FinishBlock
                code = 1
                code_idx = n
                n += 1
            else:
                frame[n] = b
                n += 1
                code += 1
                if code == 0xFF:
                    frame[code_idx] = code  #FinishBlock
                    code = 1
                    code_idx = n
                    n += 1
        frame[code_idx] = code  #FinishBlock
        frame[n] = 0
        return n+1
    
    def _decode(self, frame):
        '''
        COBS decoder/unstuffer
        '''
        if type(frame) != bytes and type(frame) != bytearray:
            raise TypeError('Need bytes or bytearray input')
        msg = bytearray()
        ba = bytearray(1)
        i=0
        size = len(frame)
        code = 0
        if size < 5:
            return b''
        while i < size:
            code = frame[i]
            i += 1
            for j in range(1,code):
                if i > size - 1:
                    return msg
                ba[0] = frame[i]
                msg.extend(ba)
                i += 1
            if code < 0xFF:
                msg.append(0)
        return msg


    @micropython.viper
    def _crc16_ccitt(self, crc:int, data:ptr8, n:int)->int:
        """Update the 16-bit CRC CCITT (poly 1021) for a bytearray or bytes object
        Takes circa 8ms for 10000 bytes (pyboard v1.1 168MHz)
        Keyword arguments:
        crc -- the CRC to be updated (0 for new calculation)
        data -- byte-wide data to be CRC'd
        n -- number of data bytes to process
        """
        x=0
        for i in range(n):
            x = ((crc >> 8) ^ data[i]) & 0xff
            x = x ^ (x >> 4)
            crc = (crc << 8) ^ (x << 12) ^ (x << 5) ^ x
            crc = crc & 0xffff
        return crc

    """
    def _crc16_ccitt(self, crc:int, data:bytes, n:int)->int:
        x:int=0
        #for i in range(len(data)):
        for i in range(n):
            x = ((crc >> 8) ^ data[i]) & 0xff
            x = x ^ (x >> 4)
            crc = (crc << 8) ^ (x << 12) ^ (x << 5) ^ x
            crc = crc & 0xffff
        return crc
    """
    
    def hasresult(self):
        """
            Do something with the result
        """
        print("*** Result:",trim_zeros(self.result))
    
async def pressed(objbtn, event, cobs):
    delay = 200
    user_btn = 1
    while True:
        user_btn = user.value()
        await asyncio.sleep_ms(delay)
        if user_btn == 0:
            await cobs.send(cobs.reply,cobs.reply_len)

async def blink(objLED, event):
    global counter
    delay=10
    objLED.off()
    while True:
        #await event
        await event.wait()
        ##########delay = event.value()
        delay = 500
        event.clear()
        objLED.on()
        print("Blink turned on LED(1). Counter:",counter)
        await asyncio.sleep_ms(delay)
        objLED.off()
        print("Blink turned off LED(1):")
        counter = counter + 1
        await asyncio.sleep_ms(delay)
        
# async def msg2(event, cc):
#     while True:
#         await event.wait()
#         print("finally running")
#         cc.hasresult()

async def process_msg(rx_event, blink_event, cc):
    txmsg = bytearray(1000)
    while True:
        #await rx_event
        await rx_event.wait()
        #blink_event.set(10)  # blink LED when valid COBS frame received
        blink_event.set()
        #Echo back the very same message
        #Copy rxmsg into txmsg
        ###########msg_len = rx_event.value()
        msg_len = 100
        #print("msg_len=",msg_len)
        # for i in range(msg_len):
        #     txmsg[i]=cc.rxmsg[i]
        # print("Message4",txmsg)
        rx_event.clear() #rxpkt buffer available for use
        # await cc.send(txmsg,msg_len)
        cc.hasresult()

# Trim zeros from end of byte array
def trim_zeros(msg):
    loc = len(msg) - 1
    # Check backwards 
    while msg[loc] == 0:
        loc = loc - 1
    newmsg = bytearray(loc)
    newmsg = msg[:loc+1]
    return newmsg
