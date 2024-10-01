from machine import Pin, SoftI2C, RTC
from ds3231 import DS3231
import sys

##### /flash drive ################
#ds3231.py   https://github.com/pangopi/micropython-DS3231-AT24C32

##### definitions ################
I2C_PORT = 'I2C1'
I2C_SDA_PIN = 'PB7' 
I2C_SCL_PIN = 'PB6' 
I2C_FREQ = 40000

#### Setup #####################
rtc = RTC()
i2c=SoftI2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=I2C_FREQ)
ds = DS3231(i2c)

#### Init ################
dt = list()

# Per driver and MicroPython doc
# datetime "year","month","day","wkday","hour","min","sec","other"
# Example ["2024","0-12","0-31", "0-6","0-23","0-59","0-59", 0]  wkday: 6=sunday
#### Functions #####################
    
def enter_time():
    #Fields  ["year","month","day","hour","min","sec", "wkday","other"]
    dt = (2024,9,30,15,58,20,0,0)
    return dt


def set_ds3231(dt):
    print("--SET--" + 65*"-")
    val = (dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],dt[6])
    ds.datetime( val )

    
def set_rtc(dt):
    print("   Set_rtc dt",dt)
    val = (dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],dt[6],dt[7])
    rtc.datetime( val )
            
#### Main #####################

print("1. Check the DS3231.")
if ds.OSF() == 0:
    print("   DS3231 is good.")
else:
    print("***OSF is bad.")
    dt = enter_time()   # normally user input
    set_ds3231(dt)
    print("   Updated DS3231 with:{}.".format(dt) )

print("2. Checking the RTC...")
parts = rtc.datetime() 
print("   The RTC has: ",parts)

if parts[0] > 2015:
    print("   RTC is good.")
else:
    print("***RTC is bad. Updating RTC from DS3231.")
    dt = ds.datetime()
    set_rtc(dt)
    print("   Updated RTC with:{}.".format(dt) )

print("DS3231 Example finished.",)

