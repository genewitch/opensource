#!/bin/bash
USER=nginx
HOME=/var/www/fcgi-data
echo "Content-Type: application/json"
echo ""
#echo "ephemeral"

if [ "$REQUEST_METHOD" = "GET" ]; then


    UrlReq=$(echo "$QUERY_STRING" | sed -n 's/^.*text=\([^&]*\).*$/\1/p')
    UrlReq_Dec=$(echo -e $(echo "$UrlReq" | sed 's/+/ /g;s/%\(..\)/\\x\1/g;'))

    Tokenz=$(echo "$QUERY_STRING" | sed -n 's/^.*token=\([^&]*\).*$/\1/p')
    Tokenz_Dec=$(echo -e $(echo "$Tokenz" | sed 's/+/ /g;s/%\(..\)/\\x\1/g;'))

    if [ "$Tokenz_Dec" = "TOKENTOKENTOKENTOKEN" ]; then

        finaluri=`openssl rand -hex 3`
        finaluri=$finaluri.png
        #touch /tmp/$finaluri
        #env >> /tmp/firefox.log
        firefox-bin --screenshot /var/www/fileserv.projectftm.com/$finaluri "$UrlReq_Dec" &>>/tmp/firefox.log
#        firefox-bin --headless --first-startup &>>/tmp/firefox.log
        chmod a+r /var/www/fileserv.projectftm.com/$finaluri

        echo "{\"response_type\": \"in_channel\", \"text\": "
        echo "\"\n#### Hello. I got $UrlReq_Dec as the url.\n http://fileserv.projectftm.com/$finaluri is your link\", \"username\": \"screenshotter\"}"

#       cat jsonfooter
    fi
else

    echo "<title>456 Wrong Request Method</title>"
    echo "</head><body>"
    echo "<h1>456</h1>"
    echo "<p>Requesting data went wrong.<br>The Request method has to be \"GET\" only!</p>"

fi

exit 0
