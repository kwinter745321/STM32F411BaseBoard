## README_UART.md
# Communicate with IR1838

* Platform: STM32
* Board: STM32F411CEU6 (BlackPill)
* Copyright (C) 2024 KW Services.
* MIT License
* MicroPython 1.20

## Scope.
Communicate with IR1838 receiver sensor.  

The IR1838 sensor is useful for receiving simple single-byte commands from a remote device.

>Note:  This port can be used for numerous other sensors, since the Port is generic and
 the signal can be configured for any BlackPill pin

#### Keyes KY-022 Sensor
Compatiable with NEC and Samsung Remotes. 
The nice thing about a Keyes sensor is that its LED blinks each time a remote sends data
(giving you visual feedback that the sensor is working.)

[Link to Keyes KY-022 Web Site](https://arduinomodules.info/ky-022-infrared-receiver-module/)

![KY-022 Image](https://arduinomodules.info/wp-content/uploads/KY-022_infrared_receiver_module-240x240.jpg)

<i>Image from Keyes web site.</i>

#### OSEPP
IR Receiver and Transmitter found in the "OSEPP IR Receiver with Remote kit".
This is nice because both devices are ready to use.  Though the IR Receiver did not have the LED that blinks.

#### Amazon
One can search Amazon for "1838 sensors" and look for kits that sell the IR Receiver and Remote.

#### Getting the Software

Get the MicroPython code from Peter Hinch's web site. His README file describes the various
IR protocols.

[Link to Peter Hinch's Github Web Site](https://github.com/peterhinch/micropython_ir)

Download both directories: "ir_rx" and "ir_tx" and place them on the BlackPill. Copy the "test.py" 
script found in the ir_rx folder. and load the test.py in Thonny.  Run the program and follow 
these instructions:

Using the Remote, a HEX code is sent to the receiver. Different Remotes send different codes.
So load the Micropython program and slowly click on each remote button to learn its hex code.
Later use this lookup list of the codes for your Project.

#### BlackPill for STM32F411CEU6.

Ensure the BlackPill is attached to the STM32F411 Base Board (the USB connect faces the edge).
And ensure you have MicroPython installed on the BlackPill.  See the github site for instructions
on flashing the firmware.  Make sure you have Thonny installed on your desktop.

## Send data.

The example uses the UART1 pins that are wired to the UART1-BT Port.
For this example, we connect a wire between the TXD and the RXD sockets.
In otherwords the signal goes out then back into the MCU (a "loopback").

Follow these Steps:
1) Connect a wire between B1 and the IR Signals pin of the "SIGNALS PORT".
2) Connect a 3-wire (white-red-black) cable between IR1838 Port and the IR Device. 
3a) Make sure the black wire connects GND on the board to the "-" (minus) on thhe device.
3b) Make sure the red wire connects the 3.3 on the board to the "+" (plus) on the device.
3c) Make sure the white wire connects  the "Sig" on the board to the "S" on the device.
4) Plug your USB cable of the BlackPill into a desktop
5) Load the file bb_test_ir1838.py into Thonny.
6) Click the Red STOP icon in the toolbar.
7) Click the Green Run icon in the tool bar

You should see information messages like so:

```
Test for IR receiver. Run:
from ir_rx.test import test
test() for NEC 8 bit protocol,
test(1) for NEC 16 bit,
test(2) for Sony SIRC 12 bit,
test(3) for Sony SIRC 15 bit,
test(4) for Sony SIRC 20 bit,
test(5) for Philips RC-5 protocol,
test(6) for RC6 mode 0.
test(7) for Microsoft Vista MCE.
test(8) for Samsung.

Hit ctrl-c to stop, then ctrl-d to soft reset.
running
running
running
```

Press a button on the remote.  You should see a reading like this:

```
Data 0x18 Addr 0x0000 Ctrl 0x00
Repeat code.
```


[Link to an example](/bb_test_ir1838.py)

Ideally there are two devices each using its own UART to communicate with the other.
For example, one can setup two BlackPills to communicate with each other.

The port on the base board can hold a bluetooth-uart dongle.  In this manner you can interact
with the bluetooth of your smart phone or your desktop computer.

## Conclusion.

(Once you get it to work) the IR1838 can be very useful.  This device requires some
experimentation on your part to get the components in a working state.  Then you need to 
find the best way to use the code in your project.

The base board provides a useful port for this device.

## References.

MicroPython docs 'latest' September 07, 2023: https://docs.micropython.org/en/latest/