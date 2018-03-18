import sys
import numpy as np
import struct
while True:
  
  bild = []

  while len(bild) < 8:
    i, = struct.unpack('h', sys.stdin.buffer.read(2))
    j, = struct.unpack('h', sys.stdin.buffer.read(2))
    k, = struct.unpack('h', sys.stdin.buffer.read(2))
    
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
  
  outa = ''.join(bild)
  #sys.stderr.write(str(outa))
  #sys.stderr.write("\n")
  outi = int(outa,2)
  #sys.stderr.write(str(outi))
  #sys.stderr.write("\n")
  sys.stderr.flush()
  outb = outi.to_bytes(1,byteorder="little",signed=False)
  sys.stdout.buffer.write(outb)
  sys.stdout
