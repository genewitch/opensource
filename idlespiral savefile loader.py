from Crypto.Cipher import AES
from hashlib import pbkdf2_hmac
import base64
import json

def decryptAES (ciphertext):
    o = pbkdf2_hmac('sha1',b'kkyyhka',b'stkttnsstkttns',1000,32)
    key = o[0:16]
    iv = o[16:]
    AESobj = AES.new(key, AES.MODE_CBC, iv)
    return AESobj.decrypt(ciphertext)

with open("is.txt",'r') as file:
    for line in file:
        input = line.split('#')
        for i in range( 0,len(input)):
            input[i] = base64.b64decode(input[i])
            input[i] = decryptAES(input[i])
            input[i] = str(input[i], 'utf-8')
#            input[i] = json.dumps(input[i])
#            input[i] = json.loads(input[i])
            print(input[i])
