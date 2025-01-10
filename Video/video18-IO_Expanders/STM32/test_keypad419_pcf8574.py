# test_keypad419_pcf8574.py
#
# Copyright (C) 2025 KW Services.
# MIT License
# MicroPython v1.24.0-preview.276.g1897fe622 on 2024-09-02
# WeAct Studio Core with STM32F411CE
#
from machine import Pin
from machine import SoftI2C
import pcf8574
import time
import ssd1306

# Define the Pins for the 4-socket hearder label I2C1 Port.
SCL_PIN = 'PB6'
SDA_PIN = 'PB7'

# Initialization of the I2C1 device
i2c = SoftI2C (scl = Pin (SCL_PIN), sda = Pin (SDA_PIN), freq = 100000)

# Setup the OLED 
oled_width = 128
oled_height = 32  # (double height) normally this is 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Define IO expander
pcf = pcf8574.PCF8574(i2c, 0x20)

# Setup wires on IO Expander
row_pins = [ 0, 1, 2, 3 ]
column_pins = [ 4, 5, 6 ]

# Define keypad matrix layout
keys = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']]

# Wiring
# keypad has 3-pin (yellow wire is first)
#           4-pin cable (white wire is first) 
# expander has 3pin cable at 0,1,2 (yellow wire first) and 4pin cable at 3,4,5,6 (white wire first)

class Keypad_PID419():
    
    #keypad PID419 pins: nc R1 R2 R3 R4 C1 C2 C3 nc
    
    def __init__( self, rows, columns, keys ):
        self.rows = rows
        self.cols = columns
        self.keys = keys

    def read_keypad( self ):
        for row in range(4):
            for col in range(3):
                pcf.port = 0x7F
                pcf.pin(self.cols[col], 0)
                readrow = pcf.pin(self.rows[row])
                readcol = pcf.pin(self.cols[col])
                if  readrow == 0:
                    time.sleep_ms(150)
                    key = self.keys[row][col]
                    return str(key)
                pcf.pin(self.cols[col], 1)
	return None

# Setup keypad
keypad = Keypad_PID419(row_pins, column_pins, keys)

### main loop #############################################################

print("Reading keypad...")
while True:
    key = keypad.read_keypad()
    if key != None:
        oled.fill(0)
        oled.text("keypad:"+key,0,0)
        oled.show()
        

