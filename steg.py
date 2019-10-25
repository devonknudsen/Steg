# Persians: Sydney Anderson, Tram Doan, Devon Knudsen, Zackary Phillips, Promyse Ward, James Wilson
# GitHub Repo URL: https://github.com/devonknudsen/Steg
# Written in Python 3.7

import sys

# used to tell any retrieval method that they have found the end of the hidden image/message
SENTINEL = bytearray([0x0, 0xff, 0x0, 0x0, 0xff, 0x0])

# method to store a defined file's data within a wrapper file
def store(method, wrapper, hidden, offset, interval):
    # byte method of storing
    if(method == 'B'):
        
        # add file to be hidden's bytes
        x = 0
        while(x < len(hidden)):
            wrapper[offset] = hidden[x]
            offset += interval
            x += 1
        
        # add sentinel bytes
        x = 0
        while (x < len(SENTINEL)):
            wrapper[offset] = SENTINEL[x]
            offset += interval
            x += 1
    
    # bit method of storing
    elif(method == 'b'):
        
        # add file to be hidden's bytes, bit by bit
        j = 0
        while(j < len(hidden)):
            for k in range(0, 8):
                
                # 254 is decimal for binary 11111110
                wrapper[offset] &= 254
                
                # 128 is decimal for binary 10000000
                # if hidden bit is a 1, add it to wrapper in LSB place
                wrapper[offset] |= ((hidden[j] & 128) >> 7)
                
                # bit shift left once in the current byte to be hidden
                hidden[j] = (hidden[j] << 1) & (2 ** 8 - 1)
                offset += interval
            
            j += 1
        
        # add sentinel bytes, bit by bit
        j = 0
        while(j < len(SENTINEL)):
            for k in range(0, 8):
                wrapper[offset] &= 254
                wrapper[offset] |= ((SENTINEL[j] & 128) >> 7)
                SENTINEL[j] = (SENTINEL[j] << 1) & (2 ** 8 - 1)
                offset += interval
            
            j += 1
        
    return wrapper
                
# method to retreive hidden data from a defined wrapper file 
def retrieve(method, wrapper, offset, interval):
    # byte array to contain data from the retreived hidden file
    hidden = bytearray()
    
    # byte method for retrieving
    if(method == 'B'):
        biteArr = bytearray()
        
        for z in range(0, 6):
            biteArr.append(wrapper[offset])
            offset += interval
            
        while(offset < len(wrapper)):
            if(biteArr != SENTINEL):
                hidden.append(biteArr[0])
                biteArr = biteArr[1:]
                biteArr.append(wrapper[offset])
                offset += interval
            else:
                return hidden
    
    # bit method for retrieving
    elif(method == 'b'):
        bitArr = bytearray()
        
        for k in range(0, 6):
            b = 0
            for j in range(0, 8):
                # if the LSB of wrapper byte is a 1 add, if not, keep 0
                b |= (wrapper[offset] & 1)
                if(j < 7):
                    # bit shift left once
                    b = (b << 1) & (2 ** 8 - 1)
                    offset += interval
                
            bitArr.append(b)
            offset += interval

        while(offset < len(wrapper)):
            if(bitArr != SENTINEL):
                b = 0
                hidden.append(bitArr[0])
                bitArr = bitArr[1:]
                for j in range(0, 8):
                    # if the LSB of wrapper byte is a 1 add, if not, keep 0
                    b |= (wrapper[offset] & 1)
                    if(j < 7):
                        # move b over to the left one bit
                        b = (b << 1) & (2 ** 8 - 1)
                        offset += interval
                
                bitArr.append(b)
                offset += interval
                
            else:
                return hidden
                        

# MAIN
sR = sys.argv[1][1]
method = sys.argv[2][1]

interval = 1

offset = int(sys.argv[3][2:])
    
if(method == 'b'):
    if(sys.argv[4][:2] == '-i'):
        interval = int(sys.argv[4][2:])
        with open(sys.argv[5][2:], 'rb') as wImg:
            wrapper = wImg.read()
            wBytes = bytearray(wrapper)
        if(sR == 's'):
            with open(sys.argv[6][2:], 'rb') as hImg:
                hidden = hImg.read()
                hBytes = bytearray(hidden)        
    else:
        with open(sys.argv[4][2:], 'rb') as wImg:
            wrapper = wImg.read()
            wBytes = bytearray(wrapper)
        if(sR == 's'):
            with open(sys.argv[5][2:], 'rb') as hImg:
                hidden = hImg.read()
                hBytes = bytearray(hidden)  
elif(method == 'B'):
    interval = int(sys.argv[4][2:])
    with open(sys.argv[5][2:], 'rb') as wImg:
            wrapper = wImg.read()
            wBytes = bytearray(wrapper)
    if(sR == 's'):
            with open(sys.argv[6][2:], 'rb') as hImg:
                hidden = hImg.read()
                hBytes = bytearray(hidden)
    
if(sR == 's'):
    newWrap = store(method, wBytes, hBytes, offset, interval)
    sys.stdout.buffer.write(newWrap)
    
if(sR == 'r'):
    newH = retrieve(method, wBytes, offset, interval)
    sys.stdout.buffer.write(newH)