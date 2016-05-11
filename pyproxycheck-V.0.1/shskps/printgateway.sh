#!/bin/sh

if [ ! -e "$1" ] ; then
    echo "USAGE : $0 inputfile"
    echo "Prints just GATEWAY proxies IP:ADDR"
fi

grep "| GATEWAY |" $1 | awk '{print $1}'