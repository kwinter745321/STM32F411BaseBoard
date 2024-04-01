## README_I2C.md
# Communicate with I2C

* Platform: STM32
* Board: STM32F411CEU6 (BlackPill)
* Copyright (C) 2024 KW Services.
* MIT License
* MicroPython 1.20

## Scope.

Display short messages on an OLED with I2C.

#### Acquiring the OLED
The example uses an inexpenseive OLED available from Amazon or Ali Express.
The OLEDs are hard coded to certain colors: (e.g. always white) But I like the device in which the top portion displays fonts in Yellow and the remaining area is in blue.

[Amazon 0.96 Yellow-Blue OLED](https://www.amazon.com/UCTRONICS-SSD1306-Self-Luminous-Display-Raspberry/dp/B072Q2X2LL/ref=sr_1_7?dib=eyJ2IjoiMSJ9.Av2lkLGBWPhH2qBAbn1mSPGKyQ_hVDqN0Om-UmYJrf66AKnS5ghnYLkISDHrowoVn3JVtTT_Uo-hErXM6t9OzJcPG2Qacl_p_UZH-B8G4lkxPxAXDiR8kLyEIffCPGqrLFmfqdZqydjQi-KF8i1q5_vDRzNBVLpCG8OV1FGXFY8Lymoi52qLgiCuzfjJp9IbrraFa7xp8nuWlPK8Ks0Ws3UTBIvT5c_tzrK99PAb4no.4Q8j3JX8r905cfQi57P-mMBIwlXPeo4LZ0CDPdsw_gg&dib_tag=se&keywords=SSD1306&qid=1711466280&sr=8-7)
[Amazon 0.96 Blue OLED](https://www.amazon.com/HiLetgo-Serial-128X64-Display-Color/dp/B06XRBYJR8/ref=sr_1_1_sspa?dib=eyJ2IjoiMSJ9.Av2lkLGBWPhH2qBAbn1mSPGKyQ_hVDqN0Om-UmYJrf66AKnS5ghnYLkISDHrowoVn3JVtTT_Uo-hErXM6t9OzJcPG2Qacl_p_UZH-B8G4lkxPxAXDiR8kLyEIffCPGqrLFmfqdZqydjQi-KF8i1q5_vDRzNBVLpCG8OV1FGXFY8Lymoi52qLgiCuzfjJp9IbrraFa7xp8nuWlPK8Ks0Ws3UTBIvT5c_tzrK99PAb4no.4Q8j3JX8r905cfQi57P-mMBIwlXPeo4LZ0CDPdsw_gg&dib_tag=se&keywords=SSD1306&qid=1711466280&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1)

This display is 128 pixels by 64 pixels and uses Blue or Yellow/Blue.  And it states it uses SSD1306 driver.
The default font uses a 8x8 pixel font.  Therefore you can displa a maximum of 16 characters on a row.  There are upto eight rows.

#### BlackPill for STM32F411CEU6.

Ensure the BlackPill is attached to the STM32F411 Base Board (the USB connect faces the edge).
And ensure you have MicroPython installed on the BlackPill.  See the github site for instructions
on flashing the firmware.  Make sure you have Thonny installed on your desktop.

## Verify the I2C Address.

Load the program: "Test_scan_i2c.py" into Thonny. Connect your device to the I2C1 ports and run the program.
It will search the I2C bus and determine the device address. Make sure this address is used in the "ssd1306.py" driver file.

My OLED returned the value 0x3c

Here are lines 113 and 114 in the driver file:
```
class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
```

>Note: Change the value in the file ssd1306.py as needed.

## Display messages on a small OLED.

The example uses the I2C1 pins (SDA and SCL) that are wired to the I2C1 Port.
It expects a OLED display to be plugged into the 4 socket header.

Follow these Steps:
1) Connect a wire between B10 and one of the buttons.
2) Load the ssd1306.py file onto the BlackPill.
3) Plug your OLED display into the four-socket port.
4) Load the file bb_small_096_oled_pyb_i2c1.py into Thonny.
5) Click the Red STOP icon in the toolbar.
6) Click the Green Run icon in the tool bar

The application wil display a few information messages and then wait.
Each time you press the user button, the program will display a message
To exit, make sure your focus is in the shell pane, and click Control C.
This will also blank the OLED.


Quick look:
```python
from pyb import I2C
import ssd1306

i2c = I2C(scl=Pin('PB6'), sda=Pin('PB7'), freq = 100000)
oled = ssd1306.SSD1306_I2C (128,64, i2c)

oled.text("hello")
```

> The oled text does not display until you invoke the show() function.

[Link to an example](./bb_small_096_oled_pyb_i2c1.py)



## Conclusion.

OLED in MicroPython is relatively easy to setup and use once you save the driver file "ssd1306.py" onto the BlackPill.
 The base board makes it easy to incorporate common user devices into your projects.

## References.

MicroPython docs 'latest' September 07, 2023: https://docs.micropython.org/en/latest/