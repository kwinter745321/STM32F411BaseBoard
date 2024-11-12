# README.md - Video 15 Serialization

November 12, 2024

Serialization

We test using this message: [ 'hello', 15, True, 1.414 ]

This set of objects, despite being simple, demonstrate several interesting situations.

- STM32: MicroPython v1.24.0-preview.276.g1897fe622 on 2024-09-02; WeAct Studio w/STM32F411CE
- Desktop: Conda Python 3.9.20 Oct 3, 2024

There are four sets of files.  Each file can be run in loopback.
Each file can send the message via a "button" and receive a message.
Otherwise, the programs are concise to highlight the serialization. 
The video demostrates them connected via a Bluetooth module on the STM32.

Serialization Technique |      STM32           |     Desktop              |
|-----------------------|----------------------|--------------------------|
| JSON                  | test_uart_json.py    | test_pyserial_json.py    |
| Pickle                | test_uart_pickle.py  | test_pyserial_pickle.py  |
| Struct                | test_uart_structpy   | test_pyserial_struct.py  |
| MsgPack               | test_uart_msgpack.py | test_pyserial_msgpack.py |


