# bb_pyb_uart1_ble.py
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
UART_SPEED = 38400        #use this for the classice Bluetooth device  
#UART_SPEED = 9600        #use this for DT-27 (BLE5.1) device
UART_PORT = 'UART1'
UART_TX = 'PA9'
UART_RX = 'PA10'

# (1) Wire a connection between B10 and a button.
# (2) Go to the UART1-BT Port and insert the BLE UART device.
# (3) Download a Serial Bluetooth Terminal app on your phone.
# (4) Load this program into Thonny, Set the UART Speed, and run it.
# (5) At your phone enable Bluetooth and scan
# (6) On my phone, H-C-2010-06-01 (was the BT-UART name.)
# (7) Start the Serial Terminal, click on Devices and select the name.
# (8) Press the button on the PCB to send "hello" to the phone.
# (9) Likewise, you can enter a word on the phone and click send.

### Setup #########################
user = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
uart = UART(UART_PORT_NUM, UART_SPEED)
# Timeout per a suggestion on MicroPython Forum site.
uart.init(UART_SPEED, bits=8, parity=None, stop=1,timeout=50)

### Loop ##########################
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