# bb_small_096_oled_pyb_i2c1.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20 
#
from machine import Pin, I2C
import ssd1306
from time import sleep

# (1) Make sure ssd1306.py file is placed on BlackPill flash.
# (2) Define the User Button
USER_PIN = 'PB10'
user = Pin(USER_PIN, Pin.IN)
# (3) Define the Pins for the 4-socket hearder label I2C1 Port.
SCL_PIN = 'PB6'
SDA_PIN = 'PB7'

# (4) Place the OLED 4-pins into the I2C1 Port. 
# Initialization of the I2C1 device
i2c = I2C (scl = Pin (SCL_PIN), sda = Pin (SDA_PIN), freq = 100000)

# Parameter setting of screen characteristics in Pixels
oled_screen_width = 128
oled_screen_length = 64
oled = ssd1306.SSD1306_I2C (oled_screen_width, oled_screen_length, i2c)
done = False

try:
    prompt = "Press User button or Control-c in Shell to exit."
    print(prompt)
    while not done:
        oled.text ('(Press User Btn)', 0, 0)
        oled.text ('or click Cntl-C', 0, 8)
        oled.show()
        user_btn = user.value()
        if user_btn == 0: 
            #Send text to display on the OLED screen
            #Font is 8x8
            oled.fill(0)
            oled.show()
            oled.text ('MicroPython OLED', 0, 0)
            oled.text ('Using I2C', 0, 8)
            oled.text ('L3', 0, 16)
            oled.text ('Cntl-c to exit', 0, 24)
            oled.text ('L5', 0, 32)
            oled.text ('L6', 0, 40)
            oled.text ('L7', 0, 48)
            oled.text ('L8', 0, 56)
            oled.show ()
            sleep(4)
            oled.fill(0)
            oled.show()
        sleep(0.5)
except:
    oled.fill(0)
    oled.show()
    done = True
    print('Interrupted by Control-c.')
finally:
    print('Finished.')