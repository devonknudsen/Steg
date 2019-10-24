import sys

SENTINEL = bytearray([0x0, 0xff, 0x0, 0x0, 0xff, 0x0])

def store(method, wrapper, hidden, offset, interval):
    if(method == 'B'):
        x = 0
        while(x < len(hidden)):
            wrapper[offset] = hidden[x]
            offset += interval
            x += 1
        
        x = 0
        while (x < len(SENTINEL)):
            wrapper[offset] = SENTINEL[x]
            offset += interval
            x += 1
    
    elif(method == 'b'):
        j = 0
        while(j < len(h)):
            for k in range(0, 8):
                
                # 254 is decimal for binary 11111110
                wrapper[offset] &= 254
                
                # 128 is decimal for binary 10000000
                # if hidden bit is a 1, add it to wrapper in LSB place
                wrapper[offset] |= ((hidden[j] & 128) >> 7)
                
                # move to the next bit in the current hiddden byte
                hidden[j] = (hidden[j] << 1) & (2 ** 8 - 1)
                offset += interval
            
            j += 1
        
        j = 0
        while(j < len(SENTINEL)):
            for k in range(0, 8):
                wrapper[offset] &= 254
                wrapper[offset] |= ((SENTINEL[j] & 128) >> 7)
                SENTINEL[j] = (SENTINEL[j] << 1) & (2 ** 8 - 1)
                offset += interval
            
            j += 1
        
    return wrapper
                

def retrieve(method, wrapper, offset, interval):
    h = bytearray()
    if(method == 'B'):
        biteArr = bytearray()
        
        for z in range(0, 6):
            biteArr.append(wrapper[offset])
            offset += interval
            
        while(offset < len(wrapper)):
            if(biteArr != SENTINEL):
                h.append(biteArr[0])
                biteArr = biteArr[1:]
                biteArr.append(wrapper[offset])
                offset += interval
            else:
                return h
    
    elif(method == 'b'):
        bitArr = bytearray()
        
        for k in range(0, 6):
            b = 0
            for j in range(0, 8):
                # if the LSB of wrapper byte is a 1 add, if not, keep 0
                b |= (wrapper[offset] & 1)
                if(j < 7):
                    # move b over to the left one bit
                    b = (b << 1) & (2 ** 8 - 1)
                    offset += interval
                
            bitArr.append(b)
            offset += interval

        while(offset < len(wrapper)):
            if(bitArr != SENTINEL):
                b = 0
                h.append(bitArr[0])
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
                return h
                        

# MAIN
sR = sys.argv[1][1]
method = sys.argv[2][1]

offset = 0
if(sys.argv[3][2:] != None):
    offset = int(sys.argv[3][2:])
    
interval = 1
if(sys.argv[4][2:] != None):
    interval = int(sys.argv[4][2:])

with open(sys.argv[5][2:], 'rb') as wImg:
    wrapper = wImg.read()
    wBytes = bytearray(wrapper)

if(sR == 's'):
    with open(sys.argv[6][2:], 'rb') as hImg:
        h = hImg.read()
        hBytes = bytearray(h)
        
    newWrap = store(method, wBytes, hBytes, offset, interval)
    sys.stdout.buffer.write(newWrap)
    
if(sR == 'r'):
    newH = retrieve(method, wBytes, offset, interval)
    sys.stdout.buffer.write(newH)