# bb_demo_oled.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
#########################
##
## 1. Upload the ssd1306.py and sdcard.py programs to the BlackPill.
## 2. Plug an external 0.96 OLED into the I2C1 Port.
## 3. Load bb_demo.py program into Thonny and click the Run ICON.
## 4. Click in the Shell (pane) to ensure the keystrokes are focused.
##
##########################
from pyb import Pin, ADC
from machine import I2C
import time

import ssd1306
from time import sleep
import sdcard
import os

# Global Variables.
choice = 0
onetime = 0
mydir = "/sd"
line1 = ""
line2 = ""
# LEDs on the SBB.
USER_LED1_PIN = 'PB4'
USER_LED2_PIN = 'PB3'
USER_LED3_PIN = 'PA15'
# Define the leds.
led1 =  Pin(USER_LED1_PIN, Pin.OUT)
led2 =  Pin(USER_LED2_PIN, Pin.OUT)
led3 =  Pin(USER_LED3_PIN, Pin.OUT)
# Make sure they are off.
led1.off()
led2.off()
led3.off()
# Connect wires between PB1,PB2,PB10 and the SBB buttons.
USER_BTN1_PIN = 'PB1'
USER_BTN2_PIN = 'PB2'
USER_BTN3_PIN = 'PB10'
# Define the user buttons.
user1 = Pin(USER_BTN1_PIN, Pin.IN, Pin.PULL_UP)
user2 = Pin(USER_BTN2_PIN, Pin.IN, Pin.PULL_UP)
user3 = Pin(USER_BTN3_PIN, Pin.IN, Pin.PULL_UP)
# Connect wires between PA1, PA2, and PA3 to the potentiometers.
POT1_PIN = 'PA1'
POT2_PIN = 'PA2'
POT3_PIN = 'PA3'
# Define the analog input for the potentiometers.
pot1 = ADC(POT1_PIN)
pot2 = ADC(POT2_PIN)
pot3 = ADC(POT3_PIN)
# Define the Pins for the 4-socket hearder label I2C1 Port.
SCL_PIN = 'PB6'
SDA_PIN = 'PB7'
# Initialization of the I2C1 device
i2c = I2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=100000)
# Parameter setting of screen characteristics in Pixels
oled_screen_width = 128
oled_screen_length = 64
# oled object
oled = None
#
# Jumpers must be on board between SPI-2 and SD Port.
# Note: CD is already pulled up to VCC with 10K 
#WP = None
SCK = Pin('PB13')
MISO = Pin('PB14')
MOSI = Pin('PB15')
CS = Pin('PB12')
SPI_PORT = 2
# microsd object
sd = None
    
def menu():
    global choice
    print("Menu.")
    print("1. Button and LEDs demo.")
    print("2. Potentiometers (ADC) demo.")
    print("3. OLED (I2C1) demo.")
    print("4. SD Card (SPI2) demo.")
    print("Click in the Shell and ", end="")
    print("type a menu choice and press 'Enter' key.")
    choice = input()
    if len(choice) > 1:
        choice = choice[0]

def prompt():
    print("\n")
    print("Press a User button or Control-c in Shell to exit.")

def button_setup():
    print("SETUP STM32F411 Base Board as follows:")
    print("* LED1 at {}.".format(led1))
    print("* LED2 at {}.".format(led2))
    print("* LED3 at {}.".format(led3))
    print("* User BTN1 defined at {}.".format(user1))
    print("* User BTN2 defined at {}.".format(user2))
    print("* User BTN3 defined at {}.".format(user3))

def button_demo():
    user1_btn = user1.value()   # returns one or zero.
    user2_btn = user2.value()   # returns one or zero.
    user3_btn = user3.value()   # returns one or zero.
    #print("user1_btn:",user1_btn)
    if user1_btn == 0:
        led1.on()
    if user2_btn == 0:
        led2.on()
    if user3_btn == 0:
        led3.on()
    time.sleep(0.7)
    led1.off()
    led2.off()
    led3.off()

def pot_setup():
    global onetime, oled
    onetime = 0
    print("SETUP STM32F411 Base Board as follows:")
    print("* POT1 at {}.".format(pot1))
    print("* POT2 at {}.".format(pot2))
    print("* POT3 at {}.".format(pot3))
    print("* User BTN1 defined at {}.".format(user1))
    oled_setup()

def pot_headers():
    global onetime, oled
    if onetime == 0:
        print()
        print("NOTE: Readings are updated every 5 seconds.\n")
        print("     POT1     ", end="")
        print("       POT2     ", end="")
        print("       POT3     ", end="\n")
        print(" -------------- ", end="")
        print(" -------------- ", end="")
        print(" -------------- ", end="\n")
        oled.fill(0)
        oled.show()
    onetime = 1

def pot_demo():
    global oled, line1, line2
    pot_headers()
    oled.text (line1, 0, 16, 0)
    oled.text (line2, 0, 24, 0)
    #oled.fill(0)
    oled.show()
    reading1 = pot1.read()
    value1 = (reading1 * 3.3) / 4095
    time.sleep(.1)
    reading2 = pot2.read()
    value2 = (reading2 * 3.3) / 4095
    time.sleep(.1)
    reading3 = pot3.read()
    value3 = (reading3 * 3.3) / 4095
    time.sleep(.1)
    print(" %d cnt %.2fv " % (reading1,value1),end="")
    print(" %d cnt %.2fv " % (reading2,value2),end="")
    print(" %d cnt %.2fv " % (reading3,value3),end="\n")
    line1 = "%4d %4d %4d" % (reading1, reading2, reading3)
    line2 = "%.2f %.2f %.2f" % (value1, value2, value3)
    oled.text ('Potentiometers', 0, 0)
    oled.text ('POT1 POT2 POT3', 0, 8)
    oled.text (line1, 0, 16)
    oled.text (line2, 0, 24)
    oled.show ()
    time.sleep(5)

def oled_setup():
    global oled
    print("SETUP STM32F411 Base Board as follows:")
    print("* Note: I2C1 port is ready. OLED must be plugged in.")
    # this will error if oled is not plugged in.
    oled = ssd1306.SSD1306_I2C(oled_screen_width, oled_screen_length, i2c)
    print("* I2C1 is {}.".format(i2c))
    print("* User BTN1 defined at {}.".format(user1))
    oled.text ('(Press User Btn)', 0, 0)
    oled.text ('or click Cntl-C', 0, 8)
    oled.show()

def oled_demo():
    global done, oled
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
    sleep(3)
    oled.fill(0)
    oled.show()
    sleep(1)
    oled.text ('App exited.', 0, 0)
    oled.show()
    sleep(1)
    oled.fill(0)
    oled.show()
    done= True
    
def sdcard_setup():
    global sd, oled
    print("SETUP STM32F411 Base Board as follows:")
    print("Place a MicroSD card into the SD card socket.")
    print("Note: Place the jumpers on the SPI-2/SD-card Port.")
    print("* The SPI interface is using SPI-{} pins.".format(SPI_PORT))
    print("* - CS   is %s." % (CS) )
    print("* - SCK  is %s." % (SCK) )
    print("* - MISO is %s." % (MISO) )
    print("* - MOSI is %s." % (MOSI) )
    print("")
    print("* User BTN1 defined at {}.".format(user1))
    sd = sdcard.SDCard(pyb.SPI(SPI_PORT), CS)
    pyb.mount(sd, mydir)
    print("SD card mounted as {}.".format(mydir))
    oled_setup()

def sdcard_demo():
    global mydir, done, sd, oled
    print("Listing for {}.".format(mydir))
    oled.fill(0)
    oled.show()
    time.sleep(0.5)
    files = os.listdir(mydir)
    for file in files:
        print(" --",file)
    oled.text ('Micro SD Card', 0, 0)
    oled.text ('DIR:'+mydir, 0, 8)
    row = 16
    for file in files:
        print(" --",file)
        oled.text(file, 0, row)
        row = row + 8
    oled.show()
    sleep(10)
    done=True
    
try:
    print("----------------")
    print("Program started.")
    menu()
    print("Performing choice '{}'.\n".format(choice))
    if choice == '1':
        button_setup()
    if choice == '2':
        pot_setup()
    if choice == '3':
        oled_setup()
    if choice == '4':
        sdcard_setup()
    print("----------------")
    print("Press User button (BTN1) when ready.")
    # waiting for user to be ready with the board setup.
    user1_btn = 1
    while user1_btn == 1:
        user1_btn = user1.value()
    prompt()
    done = False
    while not done:
        if choice == '1':
            button_demo()
        if choice == '2':
            pot_demo()
        if choice == '3':
            oled_demo()
        if choice == '4':
            sdcard_demo()
        time.sleep(0.1)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
except:
    print("\n")
    print("General exception error.")
    print("** NOTE: Did you plug in the OLED?")
    print("\n")
finally:
    led1.off()
    led2.off()
    led3.off()
    if choice != '1':
        oled.fill(0)
        oled.show()
    print('Finished.')
