# master.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# Python 3.11
#

# A program that exchanges serial_packets commands/message with endpoint 11.
# This server is Endpoint 2
# This file was modified from the distribution example master.py file at GitHub
# https://github.com/zapta/serial_packets_py

from __future__ import annotations

import sys
#pip install keyboard
import keyboard
#conda install pyserial
#conda install conda-forge::pyserial-asyncio

# For using the local version of serial_packet. Comment out if
# using serial_packets package installed by pip.
#sys.path.insert(0, "../../src")

import argparse
import asyncio
import logging
from typing import Tuple, Optional
from serial_packets.client import SerialPacketsClient
from serial_packets.packets import PacketStatus, PacketsEvent, PacketData

logging.basicConfig(level=logging.INFO,
                    format='%(relativeCreated)07d %(levelname)-7s %(filename)-10s: %(message)s')
logger = logging.getLogger("master")

logging.disable(logging.WARNING)

parser = argparse.ArgumentParser()
parser.add_argument("--port", dest="port", default=None, help="Serial port to use.")
args = parser.parse_args()

done = False
prompt = "Press 'c' to send command 'm' to send message 'q' to quit."

async def command_async_callback(endpoint: int, data: PacketData) -> Tuple[int, PacketData]:
    logger.info(f"Received command: [%d] %s", endpoint, data.hex_str())

    ###########################
    #  This endpoint is 2
    ##########################
    if (endpoint == 2):
        print("RECV","="*90)
        print("-----Command Received.       Endpoint:",endpoint)
        print("-----Command Received.        Integer:",data.read_uint32())
        print("-----Command Received.    Bool as int:",data.read_uint8())
        print("-----Command Received. float as bytes:",data.read_bytes(5))
        print("-----Command Received.   msg as bytes:",data.read_bytes(5))
        print("-----Bytes remaining:",data.bytes_left_to_read())
        print("="*94)
        status = b"0"
        response = PacketData()
        response.add_bytes(b"OK")
        print(prompt)
        if not data.all_read_ok():
                logger.info(f"Errors parsing command", status, response)
                return (PacketStatus.INVALID_ARGUMENT.value, PacketData())

        return (PacketStatus.OK.value, response)
    # In this example we don't expect incoming commands at the master side.
    assert (data.all_read_ok())
    return (PacketStatus.UNHANDLED.value, PacketData())

async def message_async_callback(endpoint: int, data: PacketData) -> Tuple[int, PacketData]:
    logger.info(f"Received message: [%d] %s", endpoint, data.hex_str())
    # Parse the message from the remote.
    if (endpoint == 2):
        msg_size = data.bytes_left_to_read()
        v1 = data.read_bytes(msg_size)
        print("RECV","="*90)
        print("-----Message Received.       Endpoint:",endpoint)
        print("-----Message received:                ",v1)
        print("-----Bytes remaining:",data.bytes_left_to_read())
        print("="*94)
        assert (data.all_read_ok())
    else:
        print("Message for a different endpoint. Endpoint:",endpoint)
    
async def event_async_callback(event: PacketsEvent) -> None:
    logger.info("%s event", event)
    print(event)

async def async_main():
    logger.info("Started.")
    done = False
    assert (args.port is not None)
    client = SerialPacketsClient(args.port, command_async_callback, message_async_callback,
                                 event_async_callback)
    print(prompt)
    while not done:
    #for r in range(0,1):
        # Connect if needed.
        if not client.is_connected():
            if not await client.connect():
                await asyncio.sleep(2.0)
                continue
        # Here connected. Send a command every 500 ms.
        await asyncio.sleep(0.5)

        if keyboard.is_pressed('q'):
            done = True

        if keyboard.is_pressed('c'):
            endpoint = 11
            cmd_data = PacketData()
            cmd_data.add_uint32(17)       # integer 17
            cmd_data.add_uint8(1)         # represents True
            cmd_data.add_bytes(b"2.414")  # float 2.414
            cmd_data.add_bytes(b"hello")
            print("SEND","="*86)
            logger.info("Sending command: [%d], %s", endpoint, cmd_data.hex_str())
            print("Sending command: EndPoint:[%d], Payload:%s" % (endpoint, cmd_data.hex_str()))
            status, response_data = await client.send_command_blocking(endpoint, cmd_data, timeout=1)
            print("="*90)
            logger.info(f"Command result: [%d], %s", status, response_data.hex_str())
            print(f"Command result: Status:[%d], Response:%s" % ( status, response_data.hex_str()))
            print("Remote Response:",response_data.read_bytes(3))
            print("-"*90)
            print(prompt)

        if keyboard.is_pressed('m'):
            endpoint = 11
            msg_data = PacketData()
            msg_data.add_bytes(b"welcome11")
            print("SEND","="*86)
            logger.info("Sending message: [%d], %s", endpoint, msg_data.hex_str())
            print("Sending message: EndPoint:[%d], Payload:%s" % (endpoint, msg_data.hex_str()))
            client.send_message(endpoint, msg_data)
            print("="*90)
            print(prompt)


asyncio.run(async_main(), debug=True)
