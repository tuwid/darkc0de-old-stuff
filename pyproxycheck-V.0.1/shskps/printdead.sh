#!/bin/sh

if [ ! -e "$1" ] ; then
    echo "USAGE : $0 inputfile"
    echo "Prints just DEAD proxies IP:ADDR"
fi

grep "| DEAD |" $1 | awk '{print $1}'