# README.md - video13-SerialTransfers

24 October 2024

This video is the start of a mini-series on Serial Transfers. Is there a better approach?  I explore the Internet and find
several promising software (python) class libraries.  We find an approach called Framing (in which we transmit a stream of bytes that are organized into a Frame.

In this video, we write the Frame and byte-stuffing code routines for the STM32.
The files are:

1. machine_uart_loopback_test0.py   A slightly modified file from Video4 UART
2. stm32_uart_test1.py              A demonstration program that creates a Frame for a simple message.
3. enum.py                          Place this file on the STM32 /flash folder
