from at24c32n import AT24C32N
#from at24c02n import AT24C02N
from machine import SoftI2C, Pin

#https://github.com/mcauser/micropython-tinyrtc-i2c
##### definitions ################
I2C_PORT = 'I2C1'
I2C_SDA_PIN = 'PB7' 
I2C_SCL_PIN = 'PB6' 
I2C_FREQ = 40000

I2C_ADDR = 0x57   
EEPROM_SIZE = 4    

##### setup ################
#i2c = I2C(0, scl=Pin(13), sda=Pin(12), freq=800000)
i2c=SoftI2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=I2C_FREQ)
eeprom = AT24C32N(i2c_addr=I2C_ADDR, pages=128, bpp=32, i2c=i2c)
#eeprom = AT24C02N(i2c_addr=I2C_ADDR, pages=256, bpp=8, i2c=i2c)
print("EEPROM memory example using AT24C32N driver")

##### main################
# write 12 bytes
eeprom.write(0, '202409301234')
# read 12 bytes
result = eeprom.read(0, 12)
print("result:",result)

word = "abcdefghijklmnopqrstuvwxyz123456"
for i in range(0,128):
    eeprom.write(i*32, word)
    
result = eeprom.read(3*32, 12)
print("result:",result)
    


