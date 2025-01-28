# smalltest2.py
#
# Modified 28 January 2025
# By 2025 KW Services to support SSD1963 800X480 LCD Display.
# MIT License
# MicroPython v1.20.0 on 2023-04-26; Raspberry Pi Pico with RP2040
#
from color_setup import ssd
import time


width, height = ssd.getScreensize()
print("Screensize width,height:",width,height)

print("Constant for Red, Green, and Blue.")
red = bytearray(    (255, 0, 0)  )
green = bytearray(  (0, 255, 0)  )
blue = bytearray(   (0, 0, 255)  )
white = bytearray((255, 255, 255))

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHTRED = (140, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
LIGHTGREEN = (0, 100, 0)
DARKGREEN = (0, 80, 0)
DARKBLUE = (0, 0, 90)
WHITE = (255, 255, 255)

colors = [BLACK,GREY,MAGENTA,DARKBLUE,BLUE,CYAN,DARKGREEN,GREEN, \
          LIGHTGREEN,YELLOW,RED,LIGHTRED,WHITE ]



#####
for i in range(0,100,2):
    ssd.pixel(i, 44, red)
    ssd.pixel(i, 45, red)
    ssd.pixel(i, 46, red)
    ssd.pixel(i, 48, white)
    ssd.pixel(i, 50, blue)
    ssd.pixel(i, 51, blue)
    ssd.pixel(i, 52, blue)
    ssd.pixel(i, 53, blue)


######
ssd.hline(100, 100, 50, green)
ssd.vline(200, 100, 50, red)


filled = True
print('Draw rect and rect filled')
ssd.rect(100, 200, 50, 50, blue)
ssd.rect(200, 200, 50, 50, green, filled)

######

filled = True
m = 1
print('Draw circles but called ellipse and ellipse filled')
ssd.ellipse(100, 300, 40, 40, blue)
ssd.ellipse(200, 300, 40, 40, green, filled)
ssd.ellipse(300, 300, 40, 40, green, filled, m)


str = "hello"
ssd.text(str, 100, 400, green)

str = "hello, this is a very long sentence hopefully"
ssd.text(str, 100, 450, red)

time.sleep_ms(6000)
ssd.fill( 0)

print("Perform fill entire frame")
for color in colors:
    ssd.fill(color)
    time.sleep_ms(1000)
ssd.fill( 0)
