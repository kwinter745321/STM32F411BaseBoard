# tof_test_3devices.py
# Modified test file for three devices.

from machine import Pin, I2C
from vl53l0x import VL53L0X

import time

print("setting up i2c")
I2C_SCL1_PIN = 'PB8'
I2C_SDA1_PIN = 'PB9'

I2C_SCL2_PIN = 'PB4'
I2C_SDA2_PIN = 'PB5'

I2C_SCL3_PIN = 'PA15'
I2C_SDA3_PIN = 'PB3'
I2C_FREQ = 400000
TIMING = 40000
DELAY = 0
PERIOD0 = 18
PERIOD1 = 14

sda1 = Pin(I2C_SDA1_PIN)   #Pin(0)
scl1 = Pin(I2C_SCL1_PIN)   #Pin(1)

sda2 = Pin(I2C_SDA2_PIN)   #Pin(0)
scl2 = Pin(I2C_SCL2_PIN)   #Pin(1)

sda3 = Pin(I2C_SDA3_PIN)   #Pin(0)
scl3 = Pin(I2C_SCL3_PIN)   #Pin(1)
id = 0

#i2c = I2C(id=id, sda=sda, scl=scl)
i2c1 = I2C(scl=scl1, sda=sda1, freq=I2C_FREQ)
i2c2 = I2C(scl=scl2, sda=sda2, freq=I2C_FREQ)
i2c3 = I2C(scl=scl3, sda=sda3, freq=I2C_FREQ)

devices = i2c1.scan() 
print('Scan finished.')
device_count = len(devices)

if device_count == 0:
    print('No I2C device found.')
else:
    print('I2C devices found:',device_count)
    print("| Decimal Address | Hex Address |")
    print("| --------------- | ----------- |")
    for device in devices:
        xdevice = str(hex(device))
        print("| %15s " % device,end="")
        print("| %9s " % xdevice," |")
        
devices = i2c2.scan() 
print('Scan finished.')
device_count = len(devices)

if device_count == 0:
    print('No I2C device found.')
else:
    print('I2C devices found:',device_count)
    print("| Decimal Address | Hex Address |")
    print("| --------------- | ----------- |")
    for device in devices:
        xdevice = str(hex(device))
        print("| %15s " % device,end="")
        print("| %9s " % xdevice," |")

devices = i2c3.scan() 
print('Scan finished.')
device_count = len(devices)

if device_count == 0:
    print('No I2C device found.')
else:
    print('I2C devices found:',device_count)
    print("| Decimal Address | Hex Address |")
    print("| --------------- | ----------- |")
    for device in devices:
        xdevice = str(hex(device))
        print("| %15s " % device,end="")
        print("| %9s " % xdevice," |")

#print(i2c2.scan())
#print(i2c3.scan())
# print("creating vl53lox object")
# Create a VL53L0X object
tof1 = VL53L0X(i2c1)
budget1 = tof1.measurement_timing_budget_us
print("Budget1 was:", budget1)
tof1.set_measurement_timing_budget( TIMING )
tof1.set_Vcsel_pulse_period(tof1.vcsel_period_type[0], PERIOD0)
tof1.set_Vcsel_pulse_period(tof1.vcsel_period_type[1], PERIOD1)

for t in range(1,12):
    print(tof1.ping()-50)
    time.sleep(DELAY)

tof2 = VL53L0X(i2c2)
budget2 = tof2.measurement_timing_budget_us
print("Budget2 was:", budget2)
tof2.set_measurement_timing_budget( TIMING )
tof2.set_Vcsel_pulse_period(tof2.vcsel_period_type[0], PERIOD0)
tof2.set_Vcsel_pulse_period(tof2.vcsel_period_type[1], PERIOD1)


for t in range(1,12):
    print(tof2.ping()-50)
    time.sleep(DELAY)
    
tof3 = VL53L0X(i2c3)
budget3 = tof3.measurement_timing_budget_us
print("Budget3 was:", budget3)
tof3.set_measurement_timing_budget( TIMING )
tof3.set_Vcsel_pulse_period(tof3.vcsel_period_type[0], PERIOD0)
tof3.set_Vcsel_pulse_period(tof3.vcsel_period_type[1], PERIOD1)
    
for t in range(1,12):
    print(tof3.ping()-50)
    time.sleep(DELAY)
    
