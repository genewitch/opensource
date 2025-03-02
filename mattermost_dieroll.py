#!/usr/bin/python
import os
import random
from urllib import parse
print ("Content-type: application/json")
print ( "" )
qs = parse.parse_qs(os.environ['QUERY_STRING'],keep_blank_values=True)
query = qs['text'][0]
rolls = [0, 0]
substring = "d"
if substring not in query.lower():
    rolls[0]=1
    rolls[1]=6
    query="1d6"
else:
    rolls = query.lower().split('d')
    if rolls[0] == '':
        rolls[0] = 1
#query="2d20"
min = 1
b = 6

print ('{"response_type": "in_channel", "text": "rolled ' + query + ':', end='')

for die in range (0,int(rolls[0])):
    print(' ' + str(random.randint(min, int(rolls[1]))), end='')

    #print(random.randint(a, int(rolls[1])))

print ('", "username" : "roller"}')
