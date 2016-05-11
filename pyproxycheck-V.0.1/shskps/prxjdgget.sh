#!/bin/sh

echo "
######################################################################
# Created by : on_a_role_again
#            : support.services.complaints@gmail.com
#            
#  
# Searches google for a inurl:prxjdg.cgi, checks results to see if 
#    they are working proxy judges
#
# USAGE : ./prxjdgfinder.sh
#
#
######################################################################
"
sleep 5

# adjust according to your patience
MAX_CHECK=100
SLEEP_TIME=3

search_string="http://www.google.se/search?q=inurl:prxjdg.cgi&num=100&hl=sv&lr=&filter=0"
echo Using URL : $search_string
lynx -dump $search_string | awk '/http:/ {print $2}' | awk '! /google/ && ! /q.cache/ {print $1}' > links
echo "done googling"
echo `wc -l links` " to check"

i=1;
> good_prxjdgs.txt
for url in `cat links` ; do
    printf "$i : checking $url  "
    lynx -dump $url > out 2> dev.null &
    the_pid=$1
    j=0
    while [ $j -lt $SLEEP_TIME ] ; do 
	if [ `grep -c REMOTE_HOST out` -gt 0 ] ; then
	    break
	fi
	sleep 1
	j=`expr $j + 1`
    done
    kill $the_pid 2> dev.null

    if [ `grep -c REMOTE_HOST out` -gt 0 ] ; then
	echo $url >> good_prxjdgs.txt
	echo "...GOOD in $j seconds" 
    else
	echo "...BAD"
    fi
    i=`expr $i + 1` 
    if [ $i -eq $MAX_CHECK ] ; then
    	break
    fi
done

echo "cleaning up"
rm links
rm out
rm dev.null
echo "... Done ..."
echo
echo "Please clean up good_prxjdgs.txt to your liking"
echo "I suggest the following commands for clean up
\$sed 's/\?.*$//' good_prxjdgs.txt > tmp
\$sort tmp | sort -u > good_prxjdgs.txt
\$rm tmp
"

echo
echo "created by on_a_role_again"
echo