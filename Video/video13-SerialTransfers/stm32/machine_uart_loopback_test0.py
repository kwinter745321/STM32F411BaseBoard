# machine_uart_loopback_test0.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20 
#
from pyb import Pin, LED, UART
import time

### PIN Definitions ##############
USER_BUTTON_PIN = 'PB10'

UART_PORT_NUM = 1
UART_SPEED = 38400      #use this for the classice Bluetooth device
#UART_SPEED = 9600      #use this for DT-27 (BLE5.1) device
UART_PORT = 'UART1'
UART_TX = 'PA9'
UART_RX = 'PA10'

### Setup #########################
user = Pin( USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP )

uart = UART( UART_PORT_NUM, UART_SPEED )
uart.init( UART_SPEED, bits=8, parity=None, stop=1, timeout=50 )

### Loop ##########################
done = False
try:
    print("----------------")
    print("Program started.")
    print("* User button is hardwired to {}.".format(USER_BUTTON_PIN))
    prompt = "Press User button to send data or Control-c in Shell to exit."
    print(prompt)
    while not done:
        
        user_btn = user.value()
        
        if uart.any() > 0:
            buf = uart.read(1)
            print("Reading: ",buf)
            
        if user_btn == 0:
            time.sleep(0.5)
            print("---")
            cnt = uart.write("hello")
            print("Sent message. Data: %d bytes" % cnt)
            
        time.sleep(0.2)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    uart.deinit()
    Pin(UART_TX, mode=Pin.IN )
    Pin(UART_RX, mode=Pin.IN )
    print('Finished.')