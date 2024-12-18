# serial_packets.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.24
#

# this is the driver file that must be loaded to the MCU

# This driver ncludes substantial portions of python code from serial_packets
# from https://github.com/zapta/serial_packets_py dated Nov 6, 2023
# Zapta's code is implemented on Desktop and uses pyserial and pyserial-asyncio
#

from enum import Enum
import sys
#from pycrc import CRCCCITT

MAX_PACKET_LEN = 64
MAX_DATA_LEN = 64
MIN_PACKET_LEN = 10 # start + cmd(4) + ep + CRC(2) + flags(2)

# Do not change the numeric tags since the will change
# the wire representation.
class PacketType(Enum):
    COMMAND = 1
    RESPONSE = 2
    MESSAGE = 3
    LOG = 4

class DecodedCommandPacket:

    def __init__(self, cmd_id: int, endpoint: int, data: PacketData):
        self.cmd_id: int = cmd_id
        self.endpoint: int = endpoint
        self.data: PacketData = data

    def __str__(self):
        return f"Command packet: {self.cmd_id}, {self.endpoint}, {self.data.size()}"


class DecodedResponsePacket:

    def __init__(self, cmd_id: int, status: int, data: PacketData):
        self.cmd_id: int = cmd_id
        self.status: int = status
        self.data: PacketData = data

    def __str__(self):
        return f"Response packet: {self.cmd_id}, {self.status}, {self.data.size()}"

class DecodedMessagePacket:

    def __init__(self, endpoint: int, data: PacketData):
        self.endpoint: int = endpoint
        self.data: PacketData = data

    def __str__(self):
        return f"Message packet: {self.endpoint}, {self.data.size()}"
      
      
class DecodedLogPacket:

    def __init__(self,  data: PacketData):
        self.data: PacketData = data

    def __str__(self):
        return f"Log packet: {self.data.size()}"

class SerialPacketsClient(object):
    PACKET_START_FLAG = 0x7C
    PACKET_ESC = 0x7D
    PACKET_END_FLAG = 0x7E

    STATE_START = 0
    STATE_TYPE  = 1
    STATE_CMD   = 2
    STATE_DEST  = 3
    STATE_DATA  = 4
    STATE_CRC   = 5
    STATE_END   = 6

    def __init__(self, uart, max_len=1024):
        self.uart = uart
        self._max_len = max_len
        self._expected_len = 0
        self._rx_crc16 = 0
        self._rx_crc16_count = 0
        self._escape_next = False
        self._state = SerialPacketsClient.STATE_START
        self._pending_payload = []
        self.__packet_bfr = bytearray()
        self.__in_packet = False
        self.__pending_escape = False
        # Used to filter warnings before first packet.
        self.__encountered_start_flag = False
        self.myflag = False
        self.recv_pkt = bytearray()
        self.seq_num = 0            # used by cmd_id in the Command packet
        self.cmd_id = None
        self.payload = None
        self.dest_ep = 0
    

    def getPacketType(self):
        if self.recv_pkt != bytearray():
            return self.recv_pkt[0]

    def crc16_ccitt(self, crc:int, data:bytes) -> int:
        x:int=0
        for i in range(len(data)):
            x = ((crc >> 8) ^ data[i]) & 0x0ffff
            x = x ^ (x >> 4)
            crc = (crc << 8) ^ (x << 12) ^ (x << 5) ^ x
            crc = crc & 0x0ffff
        return crc
    
    def buildcommand(self, endpoint, cmd_data):
        ep = PacketData().add_uint8(endpoint)
        # unique sequence number for command
        self.seq_num += 1
        cmd_id = PacketData().add_uint32(self.seq_num)
        endpt = PacketData().add_uint8(endpoint)
        #
        packet = bytearray()
        packet.append(PacketType.COMMAND)
        packet.extend(cmd_id.data_bytes() )
        packet.extend(endpt.data_bytes() )
        packet.extend(cmd_data.data_bytes() )
        crc = self.crc16_ccitt(0xFFFF, packet) 
        if crc != None:
            #packet.extend(crc.to_bytes(2, 'big'))
            ba = bytearray(1)
            ba[0] = crc >> 8
            packet.extend(ba)
            ba = bytearray(1)
            ba[0] = crc % 256
            packet.extend(ba)
        #assert (len(packet) <= MAX_PACKET_LEN)
        #print("packet w/crc:",packet)
        buf = self.byte_stuffing(packet)
        return buf
    
    def buildresponse(self, cmd_id, status, data):
        packet = bytearray()
        packet.append(PacketType.RESPONSE)
        #packet.extend(cmd_id.to_bytes(4, 'big'))
        cmd = bytearray(4)
        cmd = memoryview(cmd_id)
        packet.extend(cmd)
        packet.append(status)
        packet.extend(data)
        crc = self.crc16_ccitt(0xFFFF, packet)
        #packet.extend(crc.to_bytes(2, 'big'))
        if crc != None:
            ba = bytearray(1)
            ba[0] = crc >> 8
            packet.extend(ba)
            ba = bytearray(1)
            ba[0] = crc % 256
            packet.extend(ba)
        #assert (len(packet) <= MAX_PACKET_LEN)
        #print("packet w/crc:",packet)
        buf = self.byte_stuffing(packet)
        return buf
    
    def buildmessage(self, endpoint, msg_data):
        """Constructs a message packet, before byte stuffing"""
        packet = bytearray()
        packet.append(PacketType.MESSAGE)
        packet.append(endpoint)
        packet.extend(msg_data.data_bytes() )
        crc = self.crc16_ccitt(0xFFFF, packet)
        #packet.extend(crc.to_bytes(2, 'big'))
        if crc != None:
            ba = bytearray(1)
            ba[0] = crc >> 8
            packet.extend(ba)
            ba = bytearray(1)
            ba[0] = crc % 256
            packet.extend(ba)
        print("packet w/crc:",packet)
        #assert (len(packet) <= MAX_PACKET_LEN)
        buf = self.byte_stuffing(packet)
        return buf

    def byte_stuffing(self, packet: bytearray):
        """Byte stuff the packet using HDLC format. Also adds packet flag(s)"""
        result = bytearray()
        result.append(SerialPacketsClient.PACKET_START_FLAG)
        for byte in packet:
            if byte in [SerialPacketsClient.PACKET_START_FLAG , SerialPacketsClient.PACKET_END_FLAG, SerialPacketsClient.PACKET_ESC]:
                result.append(SerialPacketsClient.PACKET_ESC)
                result.append(byte ^ 0x20)
            else:
                result.append(byte)
        result.append(SerialPacketsClient.PACKET_END_FLAG)
        return result


#class PacketDecoder:
#
#    def __init__(self):
        # assert (decoded_packet_callback is not None)
        # self.__packet_bfr = bytearray()
        # self.__in_packet = False
        # self.__pending_escape = False
        # # Used to filter warnings before first packet.
        # self.__encountered_start_flag = False

    # def __str__(self):
    #     return f"In_packet ={self.__in_packet}, pending_escape={self.__pending_escape}, len={len(self.__packet_bytes)}"

    def __reset_packet(self, in_packet: bool):
        self.__in_packet = in_packet
        self.__pending_escape = False
        self.__packet_bfr = bytearray() # to clear buffer


    def receive_byte(self, b: int) :
        """ Returns a decoded packet or None."""
        # If not already in a packet, wait for next flag.
        if not self.__in_packet:
            if b == SerialPacketsClient.PACKET_START_FLAG:
                # Start collecting a packet.
                self.__reset_packet(True)
                self.__encountered_start_flag = True
            else:
                # Here we drop bytes until next packet start. Should not
                # happen in normal operation, except when connecting to 
                # and on going communication.
                # if self.__encountered_start_flag:
                #   logger.error(f"Dropping byte {b:02x}")
                pass
            return None

        # Here collecting packet bytes.
        assert (self.__in_packet)

        if b == SerialPacketsClient.PACKET_START_FLAG:
            # Abort current packet and start a new one.
            # logger.error(
            #     f"Dropping partial packet of size {len(self.__packet_bfr)}.")
            self.__reset_packet(True)
            return None

        if b == SerialPacketsClient.PACKET_END_FLAG:
            # Process current packet.
            if self.__pending_escape:
                #logger.error("Packet has a pending escape, dropping.")
                decoded_packet = None
            else:
                # Returns None or a packet.
                decoded_packet = self.process_packet()
                #print("\nEND_FLAG",decoded_packet)
                self.myflag = True
                try:
                    self.payload = decoded_packet.data
                except:
                    self.payload = b'Error in receive byte() line:240'
                try:
                    self.dest_ep = decoded_packet.endpoint
                except:
                    self.dest_ep = 0
                ("--Receive_byte MYFLAG:",self.myflag)
            self.__reset_packet(False)
            return decoded_packet

        # Check for size overrun. At this point, we know that the packet will
        # have at least one more additional byte, either normal or escaped.
        if len(self.__packet_bfr) >= MAX_PACKET_LEN:
            # logger.error("Packet is too long (%d), dropping",
            #              len(self.__packet_bfr))
            self.__reset_packet(False)
            return None

        # Handle escape byte.
        if b == SerialPacketsClient.PACKET_ESC:
            if self.__pending_escape:
                #logger.error("Two consecutive escape chars, dropping packet")
                self.__reset_packet(False)
            else:
                self.__pending_escape = True
            return None

        # Handle an escaped byte.
        if self.__pending_escape:
            # Flip back for 5x to 7x.
            b1 = b ^ 0x20
            if b1 not in [SerialPacketsClient.PACKET_START_FLAG, SerialPacketsClient.PACKET_END_FLAG, SerialPacketsClient.PACKET_ESC]:
                # logger.error(
                #     f"Invalid escaped byte ({b1:02x}, {b:02x}), dropping packet"
                # )
                self.__reset_packet(False)
            else:
                self.__packet_bfr.append(b1)
                self.__pending_escape = False
            return None

        # Handle a normal byte
        self.__packet_bfr.append(b)

    def process_packet(self):
        ###  Returns a packet or None. ###
        print()
        rx_bfr = self.__packet_bfr
        self.recv_pkt = rx_bfr
        # Check for minimum length. A minimum we should
        # have a type byte and two CRC bytes.
        n = len(rx_bfr)
        # logger.info(f"Packet candidate: len={n}")
        # logger.info(f"Packet: {rx_bfr.hex(sep=' ')}")
        if n < MIN_PACKET_LEN:
            #logger.error("Packet too short (%d), dropping", n)
            return None
        # Check CRC
        #packet_crc = int.from_bytes(rx_bfr[-2:], byteorder='big', signed=False)
        #print("\nprocess_packet rx_bfr:%s  \npayload: %s" % (rx_bfr, rx_bfr[6:-2]))
        foundcrc = rx_bfr[-2:]
        #print("--process_packet foundcrc:",foundcrc)
        hi = foundcrc[0]
        lo = foundcrc[1]
        #("--Found crc high-byte: %02x low byte: %02x" %(hi,lo))
        packet_crc = hi << 8
        packet_crc += lo
        computed_crc = self.crc16_ccitt(0xFFFF, bytes(rx_bfr[:-2]))
        #print("Found crc:",packet_crc,"--Computed crc:",computed_crc)
        pay_crc = self.crc16_ccitt(0xFFFF, bytes(rx_bfr))
        #print("--Payload and CRC should be zero:",pay_crc)
        if computed_crc != packet_crc:
            # logger.error("Packet CRC error, packet: %04x vs computed: %04x, dropping", packet_crc,
            #              computed_crc)
            return None
        # Construct decoded packet
        type_value = rx_bfr[0]
        if type_value == PacketType.COMMAND:
            #cmd_id = int.from_bytes(rx_bfr[1:5], byteorder='big', signed=False)
            cmd_id = rx_bfr[1:5]
            self.cmd_id = rx_bfr[1:5]
            endpoint = rx_bfr[5]
            #data = PacketData().add_bytes(rx_bfr[6:-2])
            data = PacketData().add_bytes(rx_bfr[6:-2])
            decoded_packet = DecodedCommandPacket(cmd_id, endpoint, data)
        elif type_value == PacketType.RESPONSE:
            #cmd_id = int.from_bytes(rx_bfr[1:5], byteorder='big', signed=False)
            cmd_id = rx_bfr[1:5]
            status = rx_bfr[5]
            data = PacketData().add_bytes(rx_bfr[6:-2])
            decoded_packet = DecodedResponsePacket(cmd_id, status, data)
        elif type_value == PacketType.MESSAGE:
            endpoint = rx_bfr[1]
            data = PacketData().add_bytes(rx_bfr[2:-2])
            decoded_packet = DecodedMessagePacket(endpoint, data)
        else:
            # logger.error("Invalid packet type %02x, dropping packet",
            #              type_value)
            print("process_packet decode_packet issue")
            return None
        
        # print("--decoded_packet:",decoded_packet)

        if data.size() > MAX_DATA_LEN:
            # logger.error("Packet data too long (type=%d, len=%d), dropping",
            #              type_value, data.size())
            return None

        # A new packet is available.
        # logger.info("A packet is available.")
        return decoded_packet

        # self.__packets_queue.put_nowait(decoded_packet)

class PacketStatus(Enum):
    """Defines status codes. User NAME.value to convert to int. 
    valid values are [0, 255]
    """
    OK = 0
    GENERAL_ERROR = 1
    TIMEOUT = 2
    UNHANDLED = 3
    INVALID_ARGUMENT = 4
    LENGTH_ERROR = 5
    OUT_OF_RANGE = 6
    NOT_CONNECTED = 7

    # Users can start allocating error codes from
    # here to 255.
    USER_ERRORS_BASE = 100


class PacketData:
    """Packet data buffer, with methods to serialize/deserialize the data."""

    def __init__(self):
        """ Constructs a PacketData with given initial data."""
        self.__data: bytearray = bytearray()
        self.__bytes_read: int = 0
        self.__read_error: bool = False

    def hex_str(self, max_bytes=None) -> str:
        """Returns a string with a hex dump fo the bytes. Can be long."""
        if (max_bytes is None) or (self.size() <= max_bytes):
            return self.__data.hex(sep=' ')
        prefix = self.__data[:max_bytes].hex(sep=" ")
        return f"{prefix} ... ({self.size() - max_bytes} more)"

    def data_bytes(self) -> bytearray:
        """Return a copy of the data bytes."""
        #return self.__data.copy()
        return self.__data

    def _internal_bytes_buffer(self) -> bytearray:
        """Package private. Returns a reference to the internal bytearray. Do not mutate."""
        return self.__data

    def size(self) -> int:
        """Returns the number of data bytes."""
        return len(self.__data)

    def clear(self) -> None:
        """Clear all data bytes and reset read location."""
        self.__data.clear()
        self.__bytes_read = 0
        self.__read_error = False

    def bytes_read(self) -> int:
        """The number of bytes read so far. This indicates current reading location."""
        return self.__bytes_read

    def read_error(self) -> bool:
        return self.__read_error

    def bytes_left_to_read(self) -> int:
        """Returns the number of bytes from the current reading location to the end of the data."""
        return len(self.__data) - self.__bytes_read

    def all_read(self) -> bool:
        """Returns true if read location is past the last data byte."""
        return self.__bytes_read == len(self.__data)

    def all_read_ok(self) -> bool:
        """Returns true if entire data were read with no read errors."""
        return self.all_read() and not self.read_error()

    def reset_read_location(self):
        """Reset the read location to data start and clear read error flag."""
        self.__bytes_read = 0
        self.__read_error = False

    # --- Adding data

    # TODO: Change the implementation of writing uints to a helper method 
    # similar to __read_int().
    # add_uint8(self, val: int) -> PacketData:

    def add_uint8(self, val):
        """Asserts that the value is in the range [0, 0xff] and appends it 
        to the data as a single byte."""
        assert (val >= 0 and val <= 0xff)
        self.__data.append(val)
        return self

    def add_uint16(self, val):
        """Asserts that the value is in the range [0, 0xff] and appends it 
        to the data as 2 bytes in big endian order."""
        assert (val >= 0 and val <= 0xffff)
        self.__data.extend(val.to_bytes(2, 'big'))
        return self

    def add_uint32(self, val):
        """Asserts that the value is in the range [0, 0xffff] and appends it 
        to the data as 4 bytes in big endian order."""
        assert (val >= 0 and val <= 0xffffffff)
        self.__data.extend(val.to_bytes(4, 'big'))
        return self

    def add_bytes(self, bytes: bytearray):
        """Appends the given bytes to the data."""
        self.__data.extend(bytes)
        return self

    #  --- Parsing data

    def __read_int(self, num_bytes, signed):
        """If this buffer is not in a read error condition and if it has least
        num_bytes left to read, read num_bytes bytes
        as a big endian int value and return that value. Otherwise, returns 
        None and set the read error condition.
        """
        if self.__read_error or self.__bytes_read + num_bytes > len(self.__data):
            self.__read_error = True
            return None
        result = int.from_bytes(self.__data[self.__bytes_read:self.__bytes_read + num_bytes],
                                'big',
                                signed)
        self.__bytes_read += num_bytes
        return result

    def read_uint8(self) -> int | None:
        return self.__read_int( num_bytes=1, signed=False)
       
    def read_uint16(self) -> int | None:
        return self.__read_int(num_bytes=2, signed=False)
      
    def read_uint24(self) -> int | None:
        return self.__read_int(num_bytes=3, signed=False)
      
    def read_uint32(self) -> int | None:
        return self.__read_int(num_bytes=4, signed=False)
      
    def read_int8(self) -> int | None:
        return self.__read_int(num_bytes=1, signed=True)

    def read_int16(self) -> int | None:
        return self.__read_int(num_bytes=2, signed=True)
      
    def read_int24(self) -> int | None:
        return self.__read_int(num_bytes=3, signed=True)

    def read_int32(self) -> int | None:
        return self.__read_int(num_bytes=4, signed=True)

    def read_bytes(self, n: int) -> bytearray | None:
        """Returns the next n bytes and advances the reading location,
        or None if insufficient number of bytes."""
        assert (n >= 0)
        if self.__read_error or self.__bytes_read + n > len(self.__data):
            self.__read_error = True
            return None
        result = self.__data[self.__bytes_read:self.__bytes_read + n]
        self.__bytes_read += n
        return result

    def read_str(self) -> str | None:
        """Returns the next string or null if read error."""
        if self.__read_error or self.__bytes_read + 1 > len(self.__data):
            self.__read_error = True
            return None
        # Read length byte.
        n = self.read_uint8()
        # Read characters.
        str_bytes = self.read_bytes(n)
        if self.__read_error:
            return None
        return str_bytes.decode("utf-8")

