import fileinput
import hashlib
import random

''' 
in python you can put filepath on the command line:
        python sha256pad.py somefile.txt
or you can pipe / use stdin:
        echo "foobar" | python sha256pad.py

either way works. once this has given you output,
echo the output and append to your file:
        echo "whatever the nonce is" >> somefile.txt
or:
python sha256pad.py somefile.txt >> somefile.txt
then:
        sha256sum somefile.txt
the output of that should start with however many zeros
specified in "difficulty" variable.

#warning: difficulty > 5 will take a while
#todo: threads, hopefully
#todo: scryptpad
#todo: command line switches like -d[iff[iculty]]
'''
        
file = fileinput.input(mode='rb')
precursor = hashlib.sha256()

for line in file:
        precursor.update(line)
summer = precursor.copy()

nonce =''
noncelength = 8
noncemagic = '%0' +str(noncelength) +'x'

difficulty = 5
leftpad =''
for x in range(1,difficulty+1):
        leftpad += "0"

while not (summer.hexdigest().startswith(leftpad)):
        summer = precursor.copy()
        nonce = noncemagic % random.randrange(16**noncelength)
        nonce += "\n"
        summer.update(nonce.encode('utf-8'))

print(nonce,end='')
