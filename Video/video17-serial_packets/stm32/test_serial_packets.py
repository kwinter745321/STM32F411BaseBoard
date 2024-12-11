from machine import Pin, UART
import time
import utime

from serial_packets import PacketHDLC, PacketData, PacketStatus

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

# Algorithm for CRC16 calculation confirmed by
# https://www.lammertbies.nl/comm/info/crc-calculation
### Loop ##########################
done = False

#try:
print("----------------")
print("Program started (to exchange Serial data).")
prompt = "Press User button to send data or Control-c in Shell to exit."
print(prompt)
sp = PacketHDLC(uart, buffer_size)

timeout_period = 200
temp = timeout_period
start = 0             # start timer
while not done:
    user_btn = user.value()
    user2_btn = user2.value()
    
    #######################################################
    #  (1) Recieve bytes,
    #      sp.myflag is True if received a proper packet
    #      else a timeout occurred and the uart is flushed
    #######################################################   
    if uart.any() > 0:
        # read a byte
        c = uart.read(1)
        dat = ord(c)
        # Reset 'start' timer. if first action is Command
        if start == 0:   
            start = utime.ticks_ms()
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
    # Press 2nd button on STM32 to test timeout
    #==========================================
    if user2_btn == 0:
        # For fun, lwt's force a timeout
        temp = 20
    
    
    ###############################################
    # (2) Handle (sp.myflag), received data packet 
    ###############################################   
    if sp.myflag ==  True:
        start = 0
        sp.myflag = False
        #======================================
        #  STM32 received a RESPONSE
        #======================================
        if sp.recv_pkt[0] == sp.RESPONSE:
            data = sp.payload
            msg = data.read_bytes(2)
            print("RECV","="*56)
            print("Remote Response:",msg,"time:%d ms"%(diff))
            print("="*60)
        #======================================
        #  STM32 received a COMMAND 
        #======================================
        if sp.recv_pkt[0] == sp.COMMAND:
            #---------------------------------------
            # Make sure Command is for endpoint: 11
            #---------------------------------------
            if sp.dest_ep == 11:
                data = sp.payload
                if data != None:
                    msg = data.read_bytes(7)
                else:
                    msg = "Error"
                print("="*40)
                print("Command received",msg,"time:",diff)
                print("="*40)
                print("-")
                #------------------------------------------------
                # After reading a COMMAND we must send a RESPONSE
                #------------------------------------------------
                sp.myflag = False
                pkt = sp.buildresponse(sp.cmd_id,status=PacketStatus.OK,data=b'ACK')
                buf = sp.byte_stuffing(pkt)
                print("--Main: Size:",len(buf),"Command response packet:",buf)
                print("-"*60)
                uart.write(buf)
                print("--Main: Packet sent:",buf)
                print("-"*60)
            else:
                print("Command sent to endpoint:",sp.dest_ep)

    ###############################################
    # (3) Send a data packet 
    ###############################################   
    if user_btn == 0:
        print("Sending data...")
        time.sleep(0.5)
        cmd = bytearray(4)
        cmd[0] = 0x01
        cmd[1] = 0x00
        cmd[2] = 0x00
        cmd[3] = 0x00
        endpoint = 2
        msg = "hello02"
        message = msg.encode("utf-8")
        #------------------------------------------
        # Send command
        #------------------------------------------
        pkt = sp.buildcommand(cmd,endpoint,message)
        #------------------------------------------
        # or, Send a Message
        #------------------------------------------
        #pkt = sp.buildmessage(endpoint, message)
        #
        buf = sp.byte_stuffing(pkt)
        print("Size:",len(buf),"Data packet:",buf)
        print("Sending","-"*56)
        print("Packet sent:",buf)
        print("-"*60)
        uart.write(buf)
        if buf[1] == sp.COMMAND:
            # Start a timer for Response
            start = utime.ticks_ms()


# except KeyboardInterrupt:
#     done = True
#     print('Interrupted by Control-c.')
# finally:
#     print('Finished.')
uart.deinit()

