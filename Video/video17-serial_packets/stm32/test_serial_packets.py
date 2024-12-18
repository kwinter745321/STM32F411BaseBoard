# test_serial_packets.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.24
#
from machine import Pin, UART
import time
import utime

from serial_packets import PacketType, PacketData, PacketStatus
from serial_packets import SerialPacketsClient

### PIN Definitions ##############
USER_BUTTON_PIN =  "PB10"

UART_PORT_NUM = 1
SERIAL_PORT_NUM = 1
SERIAL_SPEED = 38400      #use this for the classice Bluetooth device
#SERIAL_SPEED = 9600      #use this for DT-27 (BLE5.1) device
SERIAL_PORT = "UART1"
#UART_TX = const('PA9')
#UART_RX = const('PA10')

### Setup #########################
user = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
user2 = Pin("PB2", Pin.IN, Pin.PULL_UP)
user3 = Pin("PB1", Pin.IN, Pin.PULL_UP)
uart = UART(UART_PORT_NUM, baudrate=SERIAL_SPEED)
uart.init(SERIAL_SPEED, bits=8, parity=None, stop=1,timeout=150)
buffer_size = 64
##############

### Loop ##########################
done = False

#try:
print("----------------")
print("Program started (to exchange Serial data).")
prompt = "Press User button to send data or Control-c in Shell to exit."
print(prompt)
sp = SerialPacketsClient(uart, buffer_size)

timeout_period = 200
temp = timeout_period
start = 0             # start timer
while not done:
    user_btn = user.value()
    user2_btn = user2.value()
    user3_btn = user3.value()
    
    #######################################################
    #  (1) Recieve bytes,
    #      sp.myflag is True if received a proper packet
    #      else a timeout occurred and the uart is flushed
    #######################################################   
    if uart.any() > 0:
        # read a byte
        c = uart.read(1)
        dat = ord(c)
        # Set 'start' timer. 
        if dat == sp.PACKET_START_FLAG and start == 0:   
            start = utime.ticks_ms()
            print("Set Start timer")
        diff = utime.ticks_ms() - start
        # if reached time limit, flush uart, and reset sp.myflag
        if diff > temp:
            #timeout occurred, flush
            print("TIMEOUT OCCURRED.",diff)
            temp = timeout_period
            while c:
                c = uart.read(1)
            sp.myflag = False
        ### Decode incoming bytes ##############
        print("%02x " % dat, end="")
        buf = sp.receive_byte(dat)
        
    #==========================================
    # Press 3rd button to test timeout
    #==========================================
    if user3_btn == 0:
        print("Change timeout setting to 20 ms.")
        time.sleep(0.5)
        # For fun, lwt's force a timeout
        temp = 20
    
    
    ###############################################
    # (2) Handle (sp.myflag), received data packet 
    ###############################################   
    if sp.myflag ==  True:
        start = 0
        sp.myflag = False
        #======================================
        #  Received a RESPONSE
        #======================================
        if sp.getPacketType() == PacketType.RESPONSE:
            data = sp.payload
            if isinstance(data, PacketData):
                response_size = data.bytes_left_to_read()
                msg = data.read_bytes(response_size)
                print("RECV","="*76)
                print("-----Remote Response:",msg,"time:%d ms"%(diff))
                print("----------Timer (ms):",diff)
                print("="*80)
            else:
                print("RECV","="*76)
                print("Response data",data)
                print("="*80)
        #======================================
        #  Received a COMMAND 
        #======================================
        if sp.getPacketType() == PacketType.COMMAND:
            #---------------------------------------
            # Make sure Command is for endpoint: 11
            #---------------------------------------
            if sp.dest_ep == 11:
                data = sp.payload
                if data != None:
                    #msg = data.read_bytes(7)
                    print("="*80)
                    print("-----Command Received.       Endpoint:",sp.dest_ep)
                    cmd_id = sp.cmd_id
                    print("-----Command Received.         Cmd-ID:",int.from_bytes(cmd_id,'big') )
                    print("-----Command Received.        Integer:",data.read_uint32())
                    print("-----Command Received.    Bool as int:",data.read_uint8())
                    print("-----Command Received. float as bytes:",data.read_bytes(5))
                    print("-----Command Received.   msg as bytes:",data.read_bytes(5))
                    print("-----Bytes remaining:",data.bytes_left_to_read())
                    print("----------Timer (ms):",diff)
                    print("="*80)
                else:
                    msg = "Error payload is None"
                    print("Error:",msg)
                print("-")
                #------------------------------------------------
                # After reading a COMMAND we must send a RESPONSE
                #------------------------------------------------
                sp.myflag = False
                buf = sp.buildresponse(sp.cmd_id,status=PacketStatus.OK,data=b'ACK')
                # buf = sp.byte_stuffing(pkt)
                print("--Main: Size:",len(buf),"Command response packet:",buf)
                uart.write(buf)
                #print("--Main: Packet sent:",buf)
                print("-"*80)
            else:
                print("Command sent to endpoint:",sp.dest_ep)
                print("----------Timer (ms):",diff)
        #======================================
        #  Received a MESSAGE
        #======================================
        if sp.getPacketType() == PacketType.MESSAGE:
            #---------------------------------------
            # Make sure Message is for endpoint: 11
            #---------------------------------------
            if sp.dest_ep == 11:
                data = sp.payload
                if data != None:
                    msg_size = data.bytes_left_to_read()
                    print("="*80)
                    print("-----Message Received.       Endpoint:",sp.dest_ep)
                    print("-----Message Received.   msg as bytes:",data.read_bytes(msg_size))
                    print("-----Bytes remaining:",data.bytes_left_to_read())
                    print("----------Timer (ms):",diff)
                    print("="*80)
                else:
                    msg = "Error payload is None"
                    print("Error:",msg)

    ###############################################
    # (3) Send a Command
    ###############################################   
    if user_btn == 0:
        print("Building command and data...")
        time.sleep(0.5)
        endpoint = 2
        cmd_data = PacketData()
        cmd_data.add_uint32(15)
        cmd_data.add_uint8(1)  # represents True
        cmd_data.add_bytes(b"1.414")  # float 1.414
        cmd_data.add_bytes(b"hello")
        #------------------------------------------
        # Send command
        #------------------------------------------
        buf = sp.buildcommand( endpoint, cmd_data)
        #
        print("Sending","-"*76)
        print("Size:",len(buf))
        print("Packet sent:",buf)
        print("-"*80)
        uart.write(buf)
        print("Receiving...")
        if buf[1] == PacketType.COMMAND:
            # Start a timer for Response
            start = utime.ticks_ms()
            
    #==========================================
    # Press 2nd button to send a message
    #==========================================
    if user2_btn == 0:
        print("Building message data...")
        time.sleep(0.5)
        endpoint = 2
        msg_data = PacketData()
        msg_data.add_bytes(b"welcome02")
        #------------------------------------------
        # Send message
        #------------------------------------------
        buf = sp.buildmessage(endpoint, msg_data)
        #
        print("Sending","-"*76)
        print("Size:",len(buf))
        print("Packet sent:",buf)
        print("-"*80)
        uart.write(buf)


# except KeyboardInterrupt:
#     done = True
#     print('Interrupted by Control-c.')
# finally:
#     print('Finished.')
uart.deinit()

