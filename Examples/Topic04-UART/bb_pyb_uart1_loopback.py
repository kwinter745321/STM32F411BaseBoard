# bb_pyb_uart1_loopback.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20 
#
from pyb import Pin, LED, UART
import time

USER_BUTTON_PIN = 'PB10'

UART_PORT_NUM = 1
UART_SPEED = 38400
UART_PORT = 'UART1'
UART_TX = 'PA9'
UART_RX = 'PA10'

# (1) Wire a connection between B10 and a button.

# (2) Go to the UART1-BT POrt
# Connect a wire from the TXD socket to the RXD sockets.

user = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)

uart = UART(UART_PORT_NUM, UART_SPEED)
# Timeout per a suggestion on MicroPython Forum site.
uart.init(UART_SPEED, bits=8, parity=None, stop=1,timeout=50)

done = False
try:
    print("----------------")
    print("Program started (to send UART data).")
    print("* Please wire Host port {} to Remote.".format(UART_PORT))
    print("* - %s (TX) at %s wire to Remote-RX." % (UART_PORT, UART_TX) )
    print("* - %s (RX) at %s wire to Remote-TX." % (UART_PORT, UART_RX) )
    print("* User button is hardwired to {}.".format(USER_BUTTON_PIN))
    prompt = "Press User button to send data or Control-c in Shell to exit."
    print(prompt)
    while not done:
        user_btn = user.value()
        if uart.any() > 0:
            buf = uart.read(13)
            print("reading: ",buf)
        if user_btn == 0:
            print("Sending data.")
            time.sleep(0.5)
            b = uart.write("hello")
        time.sleep(0.2)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    uart.deinit()
    Pin(UART_TX, mode=Pin.IN )
    Pin(UART_RX, mode=Pin.IN )
    print('Finished.')