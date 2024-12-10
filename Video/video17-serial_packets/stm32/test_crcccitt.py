

def crc16_ccitt(crc:int, data:bytes) -> int:
    x:int=0
    for i in range(len(data)):
        x = ((crc >> 8) ^ data[i]) & 0x0ffff
        x = x ^ (x >> 4)
        crc = (crc << 8) ^ (x << 12) ^ (x << 5) ^ x
        crc = crc & 0x0ffff
    return crc


#msg = b'\x01\x01\x00\x00\x00\x02\x68\x65\x6c\x6c\x6f\x30\x32'
# FFFF   => val: 10:64987 hex:fddb
# xmodem => val: 10:54743 hex:d5d7 
# 1D0F   => val: 10:39700 hex:9b14 
msg = b'\x01\x01\x00\x00\x00\x02\x68\x65\x6c\x6c\x6f\x30\x32'
test = bytearray(13)
i = 0
for c in msg:
    test[i] = c
    i += 1
    
#val = crc16_ccitt(0x0, test)			#xmodem
val = crc16_ccitt(0xFFFF, test)			#0xFFFF
#val = crc16_ccitt(0x1D0F, test)			#0x1D0F
print("val: 10:%d hex:%04x "%(val,val))
#
#https://www.lammertbies.nl/comm/info/crc-calculation