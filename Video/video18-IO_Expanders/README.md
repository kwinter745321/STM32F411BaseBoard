# README.md - using IO Expanders

January 10, 2025

Copies of Mike Causer's IO Expander drivers are available from his github site:

- https://github.com/mcauser/micropython-pcf8574
- https://github.com/mcauser/micropython-pcf8575
- https://github.com/mcauser/micropython-mcp23017

We benefit becuase he uses a common approach in the driver code.
I recommend visiting his GitHub site as he provides a lot of additional information.

Typically these devices are used to interface LED indicators. I thought interfacing a keypad would be more interesting.

I obtained the keypad from Adafruit.  It is model PID419.
its ribbon cable (as wired to its switches) has seven wires:
starting from the left: they are Row 1-4 and Column 1-3.
Note: In the code they are zero-indexed.

At my GitHub site I provide the following MicroPython files:

| File Names                  |                   Function                              |
| ----------------------------| ------------------------------------------------------- |
| scan_machine_i2c.py         |  Verify address of any I2C devices on the MCU.          |
| test_keypad419_mcu.py       |  Code to test the keypad directly connected to the MCU. |
| test_keypad419_pcf8574.py   |  Code to test the keypad using PCF8574 module.          |
| test_keypad419_pcf8575.py   |  Code to test the keypad using PCF8575 module.          |
| test_keypad419_mcp23017.py  |  Code to test the keypad using MCP23017 module.         |

In the video I only demonstrate and explain the MCU-only and PCF8575 module connected to the keypad.  This is because the coding approach for them is very similar.

In summary:

The least expensive module PCF8574 looks promising.  However, when testing
the modules with other keypads I found that MCP23017 modules' ability to define pull-ups
helped. Another consideration is the ability to daisy-chain modules.  The PCF 8574 module had soldered headers and made connections to other modules easy.  The PCF8575 module included an onboard LDO regulator (regulating 5 volts to 3.3 volts.)

Any module might be the best choice for your project.


