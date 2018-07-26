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
#localhost
#geo.nbcsports.com
WHITELIST=/tmp/whitelist.txt

if test -s $WHITELIST
then
echo processing $WHITELIST
else
echo whitelist empty or not existing, creating $WHITELIST
touch $WHITELIST
echo localhost > $WHITELIST
fi


logger Downloading $URI
wget -O - $URI | grep 0.0.0.0 |
        sed 's/[[:space:]]*#.*$//g;' |
        grep -v -w -f $WHITELIST | tr ' ' '\t' |
        tr -s '\t' | tr -d '\015' | 
        sort -u > $HOSTS

CONFFILE=/tmp/dnsmasq.conf
grep addn-hosts $CONFFILE || echo "addn-hosts=$HOSTS" >> $CONFFILE

logger Restarting dnsmasq
killall dnsmasq
dnsmasq --conf-file=$CONFFILE
