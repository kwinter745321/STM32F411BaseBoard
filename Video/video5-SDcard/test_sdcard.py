
import pyb, sdcard, os
from pyb import LED, Pin

#CD pullup to VCC with 10K e.g. btn3
WP = None
SCK = Pin('PB13')
MISO = Pin('PB14')
MOSI = Pin('PB15')
CS = Pin('PB12')


sd = sdcard.SDCard(pyb.SPI(2), CS)
pyb.mount(sd, '/sd')
print(os.listdir('/'))
os.chdir('/sd')
#os.mkdir('test')
print(os.listdir())



                     
                     