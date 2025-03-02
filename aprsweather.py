#!/usr/bin/python3
#mattermost slashcommand for aprs weather station
#weatherbot integration. use /wx <STATIONID>
# this is seemingly pointless; but it works with the
# postgres aprs mapreduce somewhere in my repo


import os
from bs4 import BeautifulSoup
from mechanize import Browser
from urllib import parse

#for mattermost/slack integration
print ("Content-type: application/json")
print ( "" )

mech = Browser()

#get the query string from the os environment and parse text
#todo token verification
qs = parse.parse_qs(os.environ['QUERY_STRING'])
aprsnodeid = qs['text']

#the [0] is needed so this is a string "foo" instead of ['foo']
url = "https://aprs.fi/weather/a/" + aprsnodeid[0]
page = mech.open(url)
html = page.read()
#bs4 complains unless this features flag is there
soup = BeautifulSoup(html,features="lxml")

#pull the only table on the page (more than one table means findall("table")
table = soup.find("table")
#get a "ResultSet" of all the <tr> in the <table>
rows = table.findAll('tr')

#Now this is the annoying bit:
#json does not like having literal "\n" in the "json SOURCE" code
#so you have to use end='' and if you want literal "\n" newlines in the 
#json DATA, you have to double escape -> "\\n"
#oof.
print ('{"response_type": "in_channel", "text": "#### Station: ' + aprsnodeid[0] + '\\n', end='')

#go through each <tr> and yank the text out. there's 2 things in the ResultSet for each row.
for c in rows[1:]:
	print (c.text + "\\n", end='')
print('[see weather charts for this station on aprs.fi](http://aprs.fi/weather/a/'+aprsnodeid[0]+')\\n',end='')
print ('", "username" : "APRSweatherbot"}')
