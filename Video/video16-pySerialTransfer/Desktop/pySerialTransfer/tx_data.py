from time import sleep
#from pySerialTransfer import pySerialTransfer as txfer
from pySerialTransfer import SerialTransfer, STRUCT_FORMAT_LENGTHS

import keyboard
import time
import gc

##### to be sent ##########################
class struct:
    z = 15
    aa = 1   #True
    y = 1.414

arr = 'h~llo'


###### to be received #######################
class Struct:
    z = 0
    aa = 0
    y = 0.0
rarr = ''

# Choose Serial communication here #########################
#comport = "COM5"
comport = "loop://"

if __name__ == '__main__':

    link = SerialTransfer(comport) 
    link.open()

    done = False
    print("Press 's' to send, 'q' to quit.")
    try:
        while not done:

            if link.available():

                if link.bytes_read > 0:   #added
                    recSize = 0
                    testStruct = Struct
                    testStruct.z = 0
                    testStruct.aa = 0
                    testStruct.y = 0.0
                    rarr = ''
                    print(' Load to: z:{} aa:{} y:{} | rarr:[{}]'.format(testStruct.z, testStruct.aa, testStruct.y, rarr))

                    testStruct.z = link.rx_obj(obj_type='i', start_pos=recSize)
                    recSize += STRUCT_FORMAT_LENGTHS['i']
                    
                    testStruct.aa = link.rx_obj(obj_type='i', start_pos=recSize)
                    recSize += STRUCT_FORMAT_LENGTHS['i']
                    
                    testStruct.y = link.rx_obj(obj_type='f', start_pos=recSize)
                    recSize += STRUCT_FORMAT_LENGTHS['f']
                    
                    rarr = link.rx_obj(obj_type=str,
                                    start_pos=recSize,
                                    obj_byte_size=5)
                    recSize += len(rarr)
                    
                    print('Received: z:{} aa:{} y:{} | rarr:[{}]'.format(testStruct.z, testStruct.aa, testStruct.y, rarr))
            
            if keyboard.is_pressed('q'):
                done = True

            #while True:
            if keyboard.is_pressed('s'):
                time.sleep(0.2)
                testStruct = struct
               
                sendSize = 0
                
                sendSize = link.tx_obj(testStruct.z, start_pos=sendSize)
                sendSize = link.tx_obj(testStruct.aa, start_pos=sendSize)
                sendSize = link.tx_obj(testStruct.y, start_pos=sendSize)
                sendSize = link.tx_obj(arr, start_pos=sendSize)
                link.send(sendSize)
                #print("send Size:",sendSize,"msg:",link.tx_buff)

            gc.collect()  # I added this as I am running this code in a loop
        
    except KeyboardInterrupt:
        link.close()