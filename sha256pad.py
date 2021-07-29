import fileinput
import hashlib
import random

file = fileinput.input(mode='rb')
precursor = hashlib.sha256()

for line in file:
        precursor.update(line)
summer = precursor.copy()

nonce =''
noncelength = 8
noncemagic = '%0' +str(noncelength) +'x'

difficulty = 6
leftpad =''
for x in range(1,difficulty+1):
        leftpad += "0"

while not (summer.hexdigest().startswith(leftpad)):
        summer = precursor.copy()
        nonce = noncemagic % random.randrange(16**noncelength)
        nonce += "\n"
        summer.update(nonce.encode('utf-8'))

print(nonce +" | "+ summer.hexdigest())
