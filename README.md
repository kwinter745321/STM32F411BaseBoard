# STM32F411BaseBoard
 STM32F411 Base Board

* Platform: STM32
* Board: STM32F411CEU6 (BlackPill)
* Copyright (C) 2024 KW Services.
* MIT License
* MicroPython 1.20

## Scope.

Jump start your project with the <B>STM32F411 Base Board</B>.  The board provides a patch-wire friendly (flexible) base for the low-cost WeAct Studios' BlackPill v3.1 USB Stick board. The BlackPill is not included, however this low-cost board is available from popular retailers.  The board includes common user interface devices and ports for external devices.  

![](Board_image.jpg)

The board is compatible with popular Integrated Development Environments (IDE).  The board is well suited to creating projects in MicroPython.

## Acquiring the STM32F411 Base Board

[Please visit my store at Tindie](https://www.tindie.com/products/aiy745321/stm32f411-base-board/)

## Acquiring the STM32F411 *BlackPill) from WeAct Studios.

[Link to github web site](https://github.com/WeActStudio/WeActStudio.MiniSTM32F4x1)

1. Make sure you are getting BlackPill v3.1.
2. You should get the optional 8 MB or 16 MB Flash chip pre-soldered to the bottom of the board.
 for the BlackPill

On a Linux computer:

Follow the directions from WeAct Studios: [Link](https://github.com/WeActStudio/WeAct_F411CE-MicroPython)

This includes the first step to get the basic MicroPython software from MicroPython org.  [Link](https://micropython.org/download/)

After getting the setup, make sure to edit the file mpconfigboard.h:

```
/* BOARD Ver 2.0 set 1 ，other set 0 ex.V1.3,V2.1 V3.0 */
#define VERSION_V20 (0)

/* Use the built-in flash to change to 1 , use the external flash to change to 0 */
#define MICROPY_HW_ENABLE_INTERNAL_FLASH_STORAGE (0)

// Flash Size:
// 4MB Flash 32Mbit
// 8MB Flash 64Mbit
// 16MB Flash 128Mbit
#define MICROPY_HW_SPIFLASH_SIZE_BITS (64 * 1024 * 1024)
```

>Note: I changed all three above values:
1) I changed 1->0 because board is v3.1.
2) I changed 1->0 because my board includes flash chip.
3) I changed 32->64 because flash chip is 8MB.

The SPI_Flash area is correctly using A4, A5, A6, and A7.

## Flashing MicroPython Firmware to a BlackPill

You should register at the ST Microelectronics site and get their STM32Cube Programmer software (its free to registered users).

There are several ways to flash the BlackPill.

1. Via the USB-C port
2. Via a ST-LINK-V2 dongle that connects to the four SWD pins.
