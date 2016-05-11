#!/bin/sh
ROOTDIR=$(dirname $0)
if test "x$PYTHON" = "x"; then
	PYTHON="env python"
fi
PYTHONPATH=$ROOTDIR:$PYTHONPATH $PYTHON $ROOTDIR/scripts/fusil "$@"
