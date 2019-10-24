import sys

s = [0x0, 0xff, 0x0, 0x0, 0xff, 0x0]
SENTINEL = bytearray(s)

def store(method, wrapper, h, offset, interval):
    if(method == 'B'):
        x = 0
        while(x < len(h)):
            wrapper[offset] = h[x]
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
                wrapper[offset] |= ((h[j] & 128) >> 7)
                
                # move to the next bit in the current hiddden byte
                h[j] = (h[j] << 1) & (2 ** 8 - 1)
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
        while(offset < len(wrapper)):
            currByte = wrapper[offset]
            if(currByte == SENTINEL[0]):
                sentFinder = bytearray()
                
                for sByte in SENTINEL:
                    
                    if(currByte != sByte):
                        for b in sentFinder:
                            h.append(b)
                            
                        break
                    
                    sentFinder.append(currByte)
                    offset += interval
                    currByte = wrapper[offset]
                    
                if(sentFinder == SENTINEL):
                    return h
            else:
                h.append(currByte)
                offset += interval
    
    elif(method == 'b'):
        while(offset < len(wrapper)):
            b = 0
            for j in range(0, 8):
                # if the LSB of wrapper byte is a 1 add, if not, keep 0
                b |= (wrapper[offset] & 1)
                if(j < 7):
                    # move b over to the left one bit
                    b = (b << 1) & (2 ** 8 - 1)
                    offset += interval
            
            if(b == SENTINEL[0]):
                print('{} == {}'.format(b, SENTINEL[0]))
                # print(bin(SENTINEL[0]))
                sF = bytearray()
                sF.append(b)
                offset += interval
                
                for m in range(1, len(SENTINEL)):
                    b = 0
                    for k in range(0, 8):
                        # if the LSB of wrapper byte is a 1 add, if not, keep 0
                        b |= (wrapper[offset] & 1)
                        if(k < 7):
                            # move b over to the left one bit
                            b = (b << 1) & (2 ** 8 - 1)
                            offset += interval
                    
                    if(b != SENTINEL[m]):
                        h.append(b)
                        for byte in sF:
                            h.append(byte)
                        
                        break
                    else:
                        sF.append(b)
                        offset += interval
                
                if(sF == SENTINEL):
                    return h
            else:
                h.append(b)
                offset += interval
                        

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