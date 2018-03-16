import sys
import numpy as np
import struct
#even = True
#with open("rndbits", "rb") as f:
#ar = np.empty(1, dtype="int16")

while True:
  #c = f.read(2)
  for bit in range (1,9):
    i, = struct.unpack('h', sys.stdin.buffer.read(2))
    j, = struct.unpack('h', sys.stdin.buffer.read(2))
    k, = struct.unpack('h', sys.stdin.buffer.read(2))
    if i == j or i == k or k == j:
      continue
    elif (j - i) < (j - k):
      print("1", end="")
    elif (j - i) > (j - k):
      print("0", end="")
    else:
      continue

#  print(i, end=",")
#  ar =  np.append(ar,i)
#  if ar.size % 1000 == 0:
#    sys.stderr.write(str(np.median(ar)))
#    sys.stderr.write("\n")
#    sys.stderr.write(str(np.mean(ar)))
#    sys.stderr.write("\n")
#    sys.stderr.flush()
#s = sys.stdin.read(2)
#a = np.loadtxt(s, dtype=np.int16)
#print (np.median(a))
#print (np.mean(a))
#print (np.amin(a))
#print (np.amax(a))
