#!/bin/sh

if [ ! -e "$1" ] ; then
    echo "USAGE : $0 inputfile"
    echo "Prints just NOT ANON proxies IP:ADDR"
fi

grep "| NOT ANON |" $1 | awk '{print $1}'