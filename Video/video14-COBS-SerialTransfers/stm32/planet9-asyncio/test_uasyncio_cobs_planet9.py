# test_uasyncio_cobs_planet9.py
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

#import os
import pyb
from machine import Pin, UART
import uasyncio as asyncio

#from asyn import Event
from uasyncio import Event

from uasyncio_cobs_planet9 import UartCobs

### PIN Definitions ##############
USER_BUTTON_PIN =  const('PB10')

### Setup #########################
user = Pin( USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP )

# Frame sizes
max_rx_pkt_len = 500
max_tx_pkt_len = 500
#cc = UartCobs(1, 115200, max_rx_pkt_len, max_tx_pkt_len)
cc = UartCobs(1, 38400, max_rx_pkt_len, max_tx_pkt_len)  #for my Bluetooth module

### Functions #####################

# User Button
async def pressed(objbtn, event, cobs):
    delay = 300
    user_btn = 1  
    while True:
        user_btn = user.value()
        await asyncio.sleep_ms(delay)
        if user_btn == 0:  # becomes zero when button is pressed (to GND)
            await cobs.send(cobs.reply,cobs.reply_len)

# LED(1)
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

# Upon receipt of message, trigger the blink
async def process_msg(rx_event, blink_event, cc):
    #txmsg = bytearray(1000)
    txmsg = bytearray(max_tx_pkt_len)   #using above global
    while True:
        #await rx_event
        await rx_event.wait()
        #blink_event.set(10)  # blink LED when valid COBS frame received
        blink_event.set()
        #Echo back the very same message
        #Copy rxmsg into txmsg
        ###########msg_len = rx_event.value()
        #msg_len = 100
        #print("msg_len=",msg_len)
        # for i in range(msg_len):
        #     txmsg[i]=cc.rxmsg[i]
        # print("Message4",txmsg)
        rx_event.clear() #rxpkt buffer available for use
        # await cc.send(txmsg,msg_len)
        cc.hasresult()

### Initialize ##############################################

print("Starts waiting for other system to send a message.  Or...")
print("You can send the 'hello' message by pressing the User button.")

# the send message
msg = "hello"
message = msg.encode("utf-8")
# count blinks
counter = 1
# save message in a buffer within UartCobs
for i,c in enumerate(message):
    cc.reply[i] = c
cc.reply_len = len(msg)

### Define Tasks ######################################
loop = asyncio.get_event_loop()

# LED(1)
event_blink = Event()
loop.create_task(blink(pyb.LED(1), event_blink))

# Wait for the Push button(1) press to SEND bytes
event_pressed = Event()
loop.create_task(pressed(user, event_pressed, cc))

# Receive bytes
event_rx_cobs_pkt = Event()
loop.create_task(cc.receive(event_rx_cobs_pkt))

# Trigger LED upon receipt of message
loop.create_task(process_msg(event_rx_cobs_pkt, event_blink, cc))

loop.run_forever()
