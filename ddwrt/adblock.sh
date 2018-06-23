#!/bin/sh
logger WAN up script executing
if test -s /tmp/hosts0
then
        rm /tmp/hosts0
fi

logger Downloading http://www.mvps.org/winhelp2002/hosts.txt
wget -O - http://www.mvps.org/winhelp2002/hosts.txt | grep 0.0.0.0 |
	sed 's/[[:space:]]*#.*$//g;' |
	grep -v localhost | tr ' ' '\t' |
	tr -s '\t' | tr -d '\015' | sort -u >/tmp/hosts0
grep addn-hosts /tmp/dnsmasq.conf ||
	echo "addn-hosts=/tmp/hosts0" >>/tmp/dnsmasq.conf
logger Restarting dnsmasq
killall dnsmasq
dnsmasq --conf-file=/tmp/dnsmasq.conf
