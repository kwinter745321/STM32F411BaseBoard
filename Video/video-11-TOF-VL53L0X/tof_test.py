# import time
from machine import Pin, I2C
from vl53l0x import VL53L0X

print("setting up i2c")
I2C_PORT = 'I2C1'
I2C_SCL_PIN = 'PB6'
I2C_SDA_PIN = 'PB7'
I2C_FREQ = 400000

sda = Pin(I2C_SDA_PIN)   #Pin(0)
scl = Pin(I2C_SCL_PIN)   #Pin(1)
id = 0

#i2c = I2C(id=id, sda=sda, scl=scl)
i2c = I2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=I2C_FREQ)

print(i2c.scan())

# print("creating vl53lox object")
# Create a VL53L0X object
tof = VL53L0X(i2c)

# Pre: 12 to 18 (initialized to 14 by default)
# Final: 8 to 14 (initialized to 10 by default)

# the measuting_timing_budget is a value in ms, the longer the budget, the more accurate the reading. 
budget = tof.measurement_timing_budget_us
print("Budget was:", budget)
tof.set_measurement_timing_budget(40000)

# Sets the VCSEL (vertical cavity surface emitting laser) pulse period for the 
# given period type (VL53L0X::VcselPeriodPreRange or VL53L0X::VcselPeriodFinalRange) 
# to the given value (in PCLKs). Longer periods increase the potential range of the sensor. 
# Valid values are (even numbers only):

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)
#tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)
#tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)

#while True:
for t in range(1,12):
# Start ranging
    print(tof.ping()-50, "mm")