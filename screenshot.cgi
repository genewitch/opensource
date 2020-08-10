#!/bin/bash
USER=nginx   #nginx tries to run this with "root" env for some reason
HOME=/var/www/fcgi-data #so give it a chdir the same as in /etc/conf.d/spawn-fcgi.nginx
echo "Content-Type: application/json"
echo ""
#echo "ephemeral"

if [ "$REQUEST_METHOD" = "GET" ]; then


    UrlReq=$(echo "$QUERY_STRING" | sed -n 's/^.*text=\([^&]*\).*$/\1/p')
    UrlReq_Dec=$(echo -e $(echo "$UrlReq" | sed 's/+/ /g;s/%\(..\)/\\x\1/g;'))

    Tokenz=$(echo "$QUERY_STRING" | sed -n 's/^.*token=\([^&]*\).*$/\1/p')
    Tokenz_Dec=$(echo -e $(echo "$Tokenz" | sed 's/+/ /g;s/%\(..\)/\\x\1/g;'))

    if [ "$Tokenz_Dec" = "TOKENTOKENTOKENTOKEN" ]; then #this has to have your mattermost slash command token in it

        finaluri=`openssl rand -hex 3`
        finaluri=$finaluri.png
        #touch /tmp/$finaluri    #make sure nginx is writing files as nginx.nginx
        #env >> /tmp/firefox.log #to debug environment
        firefox-bin --screenshot /var/www/fileserv.projectftm.com/$finaluri "$UrlReq_Dec" &>>/tmp/firefox.log
#        firefox-bin --headless --first-startup &>>/tmp/firefox.log  #this is needed ONCE after your HOME and USER are set correctly
        chmod a+r /var/www/fileserv.projectftm.com/$finaluri  #firefox-bin --screenshot writes 0500 by default or something

        echo "{\"response_type\": \"in_channel\", \"text\": "
        echo "\"\n#### Hello. I got $UrlReq_Dec as the url.\n http://fileserv.projectftm.com/$finaluri is your link\", \"username\": \"screenshotter\"}"

#       cat jsonfooter
    fi
fi

exit 0
