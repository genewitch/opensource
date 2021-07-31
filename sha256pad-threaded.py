'''
in python you can put filepath on the command line:
        python sha256pad.py somefile.txt
TODO: fix stdin for threaded?

once this has given you output,
echo the output and append to your file:
        echo "whatever the nonce is" >> somefile.txt
then:
        sha256sum somefile.txt
the output of that should start with however many zeros
specified in "difficulty" variable.

#warning: difficulty > 5 will take a while
#todo: threads, hopefully
#todo: scryptpad
#todo: command line switches like -d[iff[iculty]]
'''

import fileinput
import hashlib
import random
from joblib import Parallel, delayed

file = fileinput.input(mode='rb') # inputs from stdin or file argument

nonce = ''          
noncelength = 64                         #64 hex characters is 256bits
noncemagic = '%0' +str(noncelength) +'x' #found this online to make hex numbers in python

difficulty = 9                           #how many zeros on left
leftpad =''
for x in range(1,difficulty+1):
        leftpad += "0"

def shasum(q):
	precursor = hashlib.sha256()
	for line in q:
	    #print(line)
	    precursor.update(line)
	summer = precursor.copy()
	while not (summer.hexdigest().startswith(leftpad)):
		summer = precursor.copy()
		nonce = noncemagic % random.randrange(16**noncelength)
		nonce += "\n"
		summer.update(nonce.encode('utf-8'))
	print(nonce,end='')
	
    
	
Parallel(n_jobs=40, verbose=0)(delayed(shasum)(file) for _ in range(41))
