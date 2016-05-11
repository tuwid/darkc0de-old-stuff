from itertools import izip
from ptrace.tools import minmax

def listDiff(old, new):
    """
    Difference of two lists item by item.

    >>> listDiff([4, 0, 3], [10, 0, 50])
    [6, 0, 47]
    """
    return [ item[1]-item[0] for item in izip(old, new) ]

def timedeltaSeconds(delta):
    """
    Convert a datetime.timedelta() objet to a number of second
    (floatting point number).

    >>> from datetime import timedelta
    >>> timedeltaSeconds(timedelta(seconds=2, microseconds=40000))
    2.04
    >>> timedeltaSeconds(timedelta(minutes=1, milliseconds=250))
    60.25
    """
    return delta.microseconds / 1000000.0 + delta.seconds \
        + delta.days * 3600 * 24

