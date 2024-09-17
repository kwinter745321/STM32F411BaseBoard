from machine import Pin, SoftI2C, lightsleep
from vl53l1x import VL53L1X
import time, sys

##### Definitions ################
I2C_PORT = 'I2C1'
I2C_SDA_PIN = 'PB7'
I2C_SCL_PIN = 'PB6'
I2C_FREQ = 5000000
#
print("System:",sys.implementation)
print("Platform:",sys.platform)
print("Version:",sys.version)
print("Byteorder:",sys.byteorder )

SCLPIN = Pin(I2C_SCL_PIN)
SDAPIN = Pin(I2C_SDA_PIN) 

##### Setup  ##################################################
#i2c = I2C(0)
i2c=SoftI2C(scl=SCLPIN, sda=SDAPIN, freq=I2C_FREQ)
print("i2c",i2c)
distance = VL53L1X(i2c)
print("Main Loop.")

try:
    for item in range(0,1):
        #print("range: mm ", distance.read())
        dat = distance.read()
        machine.lightsleep(100)
        print("{}".format(dat))
        machine.lightsleep(10)
        distance.clear()
        time.sleep_ms(50)
    i2c = None
    distance = None
except Exception:
    print("Error.")
finally:
    print("done")







    
    
    
    