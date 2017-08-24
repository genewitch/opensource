#!/bin/bash
#
# assuming prior to first run:
# you've installed git, and jq https://stedolan.github.io/jq/
# $ mkdir twitter && cd twitter
# $ git clone https://github.com/twitter/hbc.git 
# $cd hbc && mvn install
# 
# edit this script with the twitter dev API keys in your "my apps" section
#
# then this will put twitter.text.txt in twitter/
# Which will contain all ascii-only lines - without links -
# from status messages pulled from the "samplestream" twitter endpoint.
#

mvn exec:java -pl \
hbc-example \
-Dconsumer.key=secret \
-Dconsumer.secret=secret \
-Daccess.token=secret \
-Daccess.token.secret=secret \
> twitter.json

 tail -n2008 twitter.json \
|head -n2000 \
|  jq .text  \
| sed 's/\x00//g' \
|grep -v t.co \
|grep -P -v "[^\x01-\x7F]" \
| grep -v null \
>> ../twitter.text.txt
