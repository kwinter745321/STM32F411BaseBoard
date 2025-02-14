# test_mcobs_cbor.py
#
# Copyright (C) 2025 KW Services.
# MIT License
# MicroPython 1.24
#
from machine import Pin, UART, RTC
import os
import time
from mcobs_volts import send_msg, get_msg

import cbor
from cbor import Tag

### PIN Definitions ##############
USER_BUTTON_PIN =  const('PB10')
USER2_BUTTON_PIN =  const('PB2')
USER3_BUTTON_PIN =  const('PB1')

UART_PORT_NUM = const(1)
UART_SPEED = const(38400)      #use this for the classice Bluetooth device
#UART_SPEED = const(9600)      #use this for DX-BT27-A BT-27 (BLE5.1) device

# UART_TX = const('PA9')
# UART_RX = const('PA10')
#UART_PORT = const('UART1')
### Setup #########################
user = Pin( USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP )
user2 = Pin( USER2_BUTTON_PIN, Pin.IN, Pin.PULL_UP )
user3 = Pin( USER3_BUTTON_PIN, Pin.IN, Pin.PULL_UP )

uart = UART( UART_PORT_NUM, UART_SPEED )
uart.init( UART_SPEED, bits=8, parity=None, stop=1,timeout=50 )

### Main Loop ##############
if __name__ == '__main__':

#try:
    done = False
    print("CBOR Test on STM32")
    
    print("Starts waiting for data.")
    print("Press user button 1 to send hello message.")
    print("Press user button 2 to send data message.")
    print("Press user button 3 to send date message.")
    print("Press Control-c key to quit.")
    print("Hold the button for ~1 secs to send.")
    while not done:
        user_btn = user.value()
        user2_btn = user2.value()
        user3_btn = user3.value()
        
        data = get_msg(uart, 1)
        if data != b'':
            print("="*114)
            print("Received:",data,"length:",len(data) )
            obj = cbor.loads(data)
            print("CBOR (decodes) loads:",obj)
            for b in obj:
                 print("  Data: ",type(b), b)
            print("="*114)
            
            
        if user_btn == 0:
            time.sleep_ms(10)
            t = b"hello"
            msg = [t]
            print("-"*38)
            print("Sending message: ",msg)
            obj = cbor.dumps(msg)
            send_msg(uart, obj)
            print("-"*38)
            
        if user2_btn == 0:
            time.sleep_ms(10)
            t = b"hello"
            msg = (t, 1, True, 1.212)
            print("-"*84)
            s = cbor.dumps(msg)  # s is a bytes object
            print("Sending message: ",msg)
            print("CBOR (Encode) dumps:",s,"length:",len(s) )
            print("-"*84)
            send_msg(uart, s )
            print("-"*84)
            
        if user3_btn == 0:
            time.sleep_ms(10)
            t = b"hello"
            rtc = RTC()
            yr,mn,dy,wd,hr,mi,sc,ot = rtc.datetime()
            now = rtc.datetime()
            #print(now)
            # utc example: '2025-01-29T22:15:30Z'
            now_str = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}-05:00".format(yr,mn,dy,hr,mi,sc)
            #print(now_str)
            dt = Tag(0, now_str )
            msg = (t, 1, True, 1.212, dt)
            print("-"*114)
            s = cbor.dumps(msg)  # s is a bytes object
            print("Sending message: ",msg)
            print("CBOR (Encode) dumps:",s,"length:",len(s) )
            print("-"*114)
            send_msg(uart, s )
            print("-"*114)
            
        time.sleep_ms(10)

#except:
    print("Exception or Control-c pressed")
#finally:
    uart.deinit()
