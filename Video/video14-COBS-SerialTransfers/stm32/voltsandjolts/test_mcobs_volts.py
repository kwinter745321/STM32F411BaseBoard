# test_ucobs_volts.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.24
#
from machine import Pin, UART
import os
import time
from mcobs_volts import send_msg, get_msg


### PIN Definitions ##############
USER_BUTTON_PIN =  const('PB10')
USER2_BUTTON_PIN =  const('PB2')
USER3_BUTTON_PIN =  const('PB3')

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
    print("Volts UCOBS Test from STM32")
    print("Starts waiting for data. Press User button to send message.")
    print("Press Control-c key to quit.")
    print("Hold the button for 1-2 secs to send.")
    while not done:
        user_btn = user.value()
        user2_btn = user2.value()
        user3_btn = user3.value()
        #print(user3_btn)
        
        data = get_msg(uart, 1)
        if data != b'':
            print("Received:",data)
                    
        if user_btn == 0:
            time.sleep_ms(50)
            msgtx = b"hello"
            print("Sending message: ",msgtx)
            send_msg(uart, msgtx)
            
        if user2_btn == 0:
            time.sleep_ms(50)
            #msgtx = bytearray.fromhex('0102030405060708090A0B0C0D0E0F')
            msgtx = bytearray.fromhex('0102030405')
            print("Sending message: ",msgtx)
            uart.write(msgtx)
            
                    
        if user3_btn == 0:
            time.sleep_ms(50)
            #msgtx = bytearray.fromhex('0102030405060708090A0B0C0D0E0F')
            msgtx = bytearray.fromhex('0011121100')
            print("Sending message: ",msgtx)
            uart.write(msgtx)
                
        time.sleep_ms(50)

#except:
    print("Exception or Control-c pressed")
#finally:
    uart.deinit()
