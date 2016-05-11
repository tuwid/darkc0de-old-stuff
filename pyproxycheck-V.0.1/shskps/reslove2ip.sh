#!/bin/sh

if [ ! -e "$1" ] ; then
    echo "USAGE : $0 inputfile"
    echo "Resolve Hostname To IP"
fi




##########
# i use ping over host because the output is more standard
#

for ln in `cat $1` ; do
    if [ `echo $ln | grep -c "[[:alpha:]]"` -gt 0 ] ; then
	address=`echo $ln | awk -F: '{print $1}'`
	ping -c 1 -t 1 $address > ping.out 2> /dev/null
	if [ `grep -c "PING" ping.out` -gt 0 ] ; then
	    ip=`awk '/PING/ {print $3}' ping.out | tr -d '(' | tr -d ')' | tr -d ':'`
	    if [ "$ip" != "" ]; then
		echo $ip:`echo $ln | awk -F: '{print $2}'`
	    fi
	fi
    else
	echo $ln
    fi
    
done
rm ping.out