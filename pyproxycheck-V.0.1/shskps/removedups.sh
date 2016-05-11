#!/bin/sh

if [ ! -e "$1" ] ; then
    echo "USAGE : $0 inputfile"
    echo "Removes Duplicates From Proxy List"
fi

sort $1 | sort -u > unique.$1