import sys

s = [0x0, 0xff, 0x0, 0x0, 0xff, 0x0]
SENTINEL = bytearray(s)

def store(method, w, h, o, i):
    if(method == 'B'):
        x = 0
        while(x < len(h)):
            w[o] = h[x]
            o += i
            x += 1
        
        x = 0
        while (x < len(SENTINEL)):
            w[o] = SENTINEL[x]
            o += i
            x += 1
            
        return w

def retrieve(method, w, o, i):
    h = bytearray()
    if(method == 'B'):
        while(o < len(w)):
            currByte = w[o]
            if(currByte == SENTINEL[0]):
                
                sentFinder = bytearray()
                for sByte in SENTINEL:
                    
                    if(currByte != sByte):
                        for b in sentFinder:
                            h.append(b)
                            
                        break
                    
                    sentFinder.append(currByte)
                    o += i
                    currByte = w[o]
                    
                if(sentFinder == SENTINEL):
                    return h
            else:
                h.append(currByte)
                o += i

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
    w = wImg.read()
    wBytes = bytearray(w)

if(sR == 's'):
    with open(sys.argv[6][2:], 'rb') as hImg:
        h = hImg.read()
        hBytes = bytearray(h)
        
    newWrap = store(method, wBytes, hBytes, offset, interval)
    sys.stdout.buffer.write(newWrap)
    
if(sR == 'r'):
    newH = retrieve(method, wBytes, offset, interval)
    sys.stdout.buffer.write(newH)