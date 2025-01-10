# test_keypad419_mcu.py
#
# Copyright (C) 2025 KW Services.
# MIT License
# MicroPython v1.24.0-preview.276.g1897fe622 on 2024-09-02
# WeAct Studio Core with STM32F411CE
#

from machine import Pin
from machine import SoftI2C
import ssd1306
import time

# Define the I2C1 Pins.
SCL_PIN = 'PB6'
SDA_PIN = 'PB7'

# Setup I2C
i2c = SoftI2C (scl = Pin (SCL_PIN), sda = Pin (SDA_PIN), freq = 100000)

# Setup the OLED (double height)
oled_width = 128
oled_height = 32  # normally this is 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Setup wires on MCU
row_pins = [ "B12", "B13", "B14", "B15" ]  # configure as digital outputs 
column_pins = [ "B3","B4", "B5" ]       # configure as digital inputs using pull-down

# Define keypad matrix layout
keys = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']]


# Wiring
# keypad has 3-pin (yellow wire is first)
#           4-pin cable (white wire is first) 
# mcu has 3pin cable at b3-b5 (yellow at b3) and 4pin cable at b12-b15 (white at b12)

class Keypad_PID419():
    
    def __init__( self, rows, columns, keys ):
        self.rows = self.setup_rows(rows)
        self.cols = self.setup_cols(columns)
        self.keys = keys
        
    def setup_rows( self, rows):
        arr  = []
        for r in rows:
            row = Pin(r, Pin.OUT)
            arr.append(row)
            row.value(1)
        return arr
    
    def setup_cols( self, cols):
        arr = []
        for c in cols:
            col = Pin(c, Pin.IN, Pin.PULL_DOWN)
            arr.append(col)
        return arr
    
    def read_keypad( self ):
        done = False
        key = -1
        while not done:
            for row in range(4):
                for col in range(3):
                    self.rows[row].value(1)
                    if self.cols[col].value() == 1:
                        time.sleep_ms(150)
                        done = True
                        key = self.keys[row][col]
                        self.rows[row].value(1)
                    self.rows[row].value(0)
        return str(key)

# Setup keypad
keypad = Keypad_PID419(row_pins, column_pins, keys)

### Main ######################################################

print("Reading keypad...")
while True:
    key = keypad.read_keypad()
    if key != None :
        #print(key)
        oled.fill(0)                    # clear OLED
        oled.text("keypad:"+key, 0, 0)
        oled.show()
        
