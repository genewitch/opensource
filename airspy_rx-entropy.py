# input to stdin signed int16 between -4096 and 4096

import sys
import numpy as np
import struct

while True:
  
  bild = []
  while len(bild) < 8:
    #get three int16s in a row
    i, = struct.unpack('h', sys.stdin.buffer.read(2))
    j, = struct.unpack('h', sys.stdin.buffer.read(2))
    k, = struct.unpack('h', sys.stdin.buffer.read(2))
    
    if i == j or i == k or k == j:
      #just drop all three if they're equal
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
  outi = int(outa,2)
  outb = outi.to_bytes(1,byteorder="little",signed=False)
  
  #this is outputting stuff like "b'n'b'F'b'N'b'\xbc'b'\x83'b'\xaa'b'\xfb'"
  #i want it to output raw bytes, no formatting or anything
  print( outb, end="")
  
