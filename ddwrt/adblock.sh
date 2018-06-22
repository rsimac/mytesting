#!/bin/sh
#simple adblocking config script for ddwrt
#based on https://wiki.dd-wrt.com/wiki/index.php/Ad_blocking
#with whitelisting added

logger WAN up script executing
HOSTS=/tmp/hosts0
if test -s $HOSTS
then
        rm $HOSTS
fi

#blacklist uri
URI=http://www.mvps.org/winhelp2002/hosts.txt

#local whitelist, use can add hostname exceptions into it
#for example
#geo.nbcsports.com
WHITELIST=/tmp/whitelist.txt

logger Downloading $URI
wget -O - $URI | grep 0.0.0.0 |
        sed 's/[[:space:]]*#.*$//g;' |
        grep -v localhost | tr ' ' '\t' |
        tr -s '\t' | tr -d '\015' | 
        grep --invert-match --word-regexp --file=$WHITELIST |
        sort -u > $HOSTS

CONFFILE=/tmp/dnsmasq.conf
grep addn-hosts $CONFFILE || echo "addn-hosts=$HOSTS" >> $CONFFILE

logger Restarting dnsmasq
killall dnsmasq
dnsmasq --conf-file=$CONFFILE
