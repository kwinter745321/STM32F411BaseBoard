# test_stm32_mp_cobs_planet9.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.24
#
from machine import Pin, UART
import os
from time import sleep
import time

from mcobs_planet9 import send_msg, get_msg, get_frame, cob_decode, crc16_ccitt_bytes

### PIN Definitions ##############
USER_BUTTON_PIN =  const('PB10')

UART_PORT_NUM = const(1)
UART_SPEED = const(38400)      #use this for the classice Bluetooth device
#UART_SPEED = const(9600)      #use this for DX-BT27-A BT-27 (BLE5.1) device

# UART_TX = const('PA9')
# UART_RX = const('PA10')
#UART_PORT = const('UART1')
### Setup #########################
user = Pin( USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP )
uart = UART( UART_PORT_NUM, UART_SPEED )
uart.init( UART_SPEED, bits=8, parity=None, stop=1,timeout=50 )


if __name__ == '__main__':

    try:
        done = False
        print("Planet9 UCOBS Test from STM32")
        print("Starts waiting for data. Press User button to send message.")
        print("Press Control-c key to quit.")
        print("Press the button for 1-2 secs.")
        while not done:
            user_btn = user.value()
            
            data = get_msg(uart, 1)
            if data != b'':
                print("Received:",data)
                
            if user_btn == 0:
                time.sleep_ms(200)
                for i in range(1):
                    #msgtx = bytearray.fromhex('0102030405060708090A0B0C0D0E0F')
                    msgtx = b"hello"
                    print("Sending message: ",msgtx)
                    send_msg(uart, msgtx)
    except:
        print("Exception or Control-c pressed")
    finally:
        uart.deinit()