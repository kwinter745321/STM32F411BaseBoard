# master.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# Python 3.11
#

# based on master.py found at
# https://github.com/zapta/serial_packets_py/tree/main/src/examples
#

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

parser = argparse.ArgumentParser()
parser.add_argument("--port", dest="port", default=None, help="Serial port to use.")
args = parser.parse_args()

done = False

async def command_async_callback(endpoint: int, data: PacketData) -> Tuple[int, PacketData]:
    logger.info(f"Received command: [%d] %s", endpoint, data.hex_str())
    #################################################
    #  The master.py on the Desktop is endpoint is 2
    #################################################
    if (endpoint == 2):
        print("RECV","="*56)
        print("-----Command Received. endpoint:",endpoint,"data:",data.read_bytes(7))
        print("-----Bytes remaining:",data.bytes_left_to_read())
        print("="*60)
        status = b"0"
        response = PacketData()
        response.add_bytes(b"OK")

        if not data.all_read_ok():
                logger.info(f"Errors parsing command", status, response)
                return (PacketStatus.INVALID_ARGUMENT.value, PacketData())

        return (PacketStatus.OK.value, response)
    # In this example we don't expect incoming commands at the master side.
    assert (data.all_read_ok())
    return (PacketStatus.UNHANDLED.value, PacketData())


async def message_async_callback(endpoint: int, data: PacketData) -> Tuple[int, PacketData]:
    logger.info(f"Received message: [%d] %s", endpoint, data.hex_str())
    # Parse the message from the slave.
    v1 = data.read_bytes(7)
    print("Message received:",v1)
    #v1 = data.read_uint32()
    #assert (v1 == 12345678)
    assert (data.all_read_ok())
    


async def event_async_callback(event: PacketsEvent) -> None:
    logger.info("%s event", event)



async def async_main():
    logger.info("Started.")
    done = False
    assert (args.port is not None)
    client = SerialPacketsClient(args.port, command_async_callback, message_async_callback,
                                 event_async_callback)
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

        if keyboard.is_pressed('s'):
            #endpoint = 20
            endpoint = 11
            #cmd_data = PacketData().add_uint8(200).add_uint32(1234)
            #cmd_data = PacketData().add_uint32(1234)
            hello = b"hello11"
            cmd_data = PacketData().add_bytes(hello)
            logger.info("Sending command: [%d], %s", endpoint, cmd_data.hex_str())
            print("SEND","="*56)
            status, response_data = await client.send_command_blocking(endpoint, cmd_data, timeout=0.2)
            print("="*60)
            logger.info(f"Command result: [%d], %s", status, response_data.hex_str())
            print("Remote Response:",response_data.read_bytes(3))
            print("-"*60)


asyncio.run(async_main(), debug=True)
