# test_keypad419_mcp23017.py
#
# Copyright (C) 2025 KW Services.
# MIT License
# MicroPython v1.24.0-preview.276.g1897fe622 on 2024-09-02
# WeAct Studio Core with STM32F411CE
#
from machine import Pin
from machine import SoftI2C
import mcp23017
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
mcp = mcp23017.MCP23017(i2c, 0x20)
mcp.gpio = 0xffff

# Setup wires on IO Expander
row_pins = [ 0,1,2,3 ]   # configure as outputs
column_pins = [ 4,5,6 ]  # configure as inputs

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
    
    def __init__( self, keys ):
        self.setup_rows()
        self.setup_cols()
        self.keys = keys
        
    def setup_rows( self ):
        for r in row_pins:
            r_item = mcp[r].output(1)
            print("setup mcp[ %d ] as out" % r)
    
    def setup_cols( self ):
        for c in column_pins:
            c_item = mcp[c].input(pull=1)    # must have pull=1
            print("setup mcp[ %d ] as in" % c)
    
    def read_keypad( self ):
        for row in range(4):
            for col in range(3):
                r = row_pins[row]
                mcp[r].output(1)
                c = column_pins[col]
                if mcp.pin(c) == 0:
                    time.sleep_ms(50)
                    key = self.keys[row][col]
                    mcp.gpio = 0x00ff        # byte 1: port B / byte 0:port a
                    return str(key)
                mcp.pin( r, mode=0, value=0)
        return None

# Setup keypad
keypad = Keypad_PID419(keys)

### main loop #############################################################

print("Reading keypad...")
while True:
    key = keypad.read_keypad()
    if key != None:
        oled.fill(0)
        oled.text("keypad:"+key,0,0)
        oled.show()
        
        
        