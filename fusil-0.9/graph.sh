#!/bin/sh
DATA=$1
OUTPUT=graph.png

if [ "x$DATA" = "x" ]; then
    echo "usage: $0 graph.dat"
    exit 1
fi

if [ ! -f "$DATA" ]; then
    echo "File $DATA doesn't exit"
    exit 1
fi

cat <<EOF | gnuplot
# Output: 800x600 PNG file
set terminal png size 800, 600
set output '$OUTPUT'

# Title and labels
set title "Fusil aggressivity"
set xlabel "Session index"

# Scale axes
set autoscale
#set xrange [1:]

# Disable top and bottom borders
set border 2+8

# "linetype 3": use blue color
plot \
   '$DATA' using 1:2 title 'score' \
       with steps linewidth 2, \
   '$DATA' using 1:3 title 'aggressivity' \
       with steps linewidth 3 linetype 3
EOF

echo "Graphic generated: $OUTPUT"

display $OUTPUT

