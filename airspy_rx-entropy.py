# take airspy_rx ype 2 (signed, 16 bit integers between -4096 and +4096)
# and output debiased raw binary (packed into bytes)

import sys
import struct


while True:
  #use a list to build a byte
  bild = []

  while len(bild) < 8:
    
    #read three int16 from stdin
    i, = struct.unpack('h', sys.stdin.buffer.read(2))
    j, = struct.unpack('h', sys.stdin.buffer.read(2))
    k, = struct.unpack('h', sys.stdin.buffer.read(2))
    
    #drop if anything all or anything is equal
    if i == j or i == k or k == j:
      continue
    
    elif (j - i) < (j - k):
      bild.append('1')
      #print("1", end="")
    
    elif (j - i) > (j - k):
      bild.append('0')
      #print("0", end="")
    
    else:
      continue
  
  outa = ''.join(bild) #this makes an 8 character string comprised of 1s and/or 0s
  
  #  debug
  #sys.stderr.write(str(outa))
  #sys.stderr.write("\n")
  
  outi = int(outa,2) # take the binary string and make it an 8 bit int
  
  #  debug
  #sys.stderr.write(str(outi))
  #sys.stderr.write("\n")
  #sys.stderr.flush()
  
  outb = outi.to_bytes(1,byteorder="little",signed=False) #take the integer and make it a raw byte
  sys.stdout.buffer.write(outb) #write raw byte to stdout
