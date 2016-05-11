"""
Functions to parse a Python function prototype in its documentation.
"""

import re

PROTOTYPE_REGEX = re.compile(r"[A-Za-z]+[A-Za-z_0-9]*\(([^)]*)\)", re.MULTILINE)

def parseArguments(arguments, defaults):
    for arg in arguments.split(","):
        arg = arg.strip(" \n[]")
        if not arg:
            continue
        if "=" in arg:
            arg, value = arg.split("=", 1)
            defaults[arg] = value
        yield arg

def parsePrototype(doc):
    r"""
    >>> parsePrototype("test([x])")
    ((), None, ('x',), {})
    >>> parsePrototype('dump(obj, file, protocol=0)')
    (('obj', 'file'), None, ('protocol',), {'protocol': '0'})
    >>> parsePrototype('setitimer(which, seconds[, interval])')
    (('which', 'seconds'), None, ('interval',), {})
    >>> parsePrototype("decompress(string[, wbits[, bufsize]])")
    (('string',), None, ('wbits', 'bufsize'), {})
    >>> parsePrototype("decompress(string,\nwbits)")
    (('string', 'wbits'), None, (), {})
    >>> parsePrototype("get_referents(*objs)")
    ((), '*objs', (), {})
    >>> parsePrototype("nothing")
    """
    if not doc:
        return None
    doc = doc.strip()
    match = PROTOTYPE_REGEX.match(doc)
    if not match:
        return None
    arguments = match.group(1)
    if arguments == '...':
        return None
    defaults = {}
    vararg = None
    varkw = tuple()
    if "[" in arguments:
        arguments, varkw = arguments.split("[", 1)
        arguments = tuple(parseArguments(arguments, defaults))
        varkw = tuple(parseArguments(varkw, defaults))
    else:
        arguments = tuple(parseArguments(arguments, defaults))

    # Argument with default value? => varkw
    move = None
    for index in xrange(len(arguments)-1, -1, -1):
        arg = arguments[index]
        if arg not in defaults:
            break
        move = index
    if move is not None:
        varkw = arguments[move:] + varkw
        arguments = arguments[:move]

    if arguments and arguments[-1].startswith("*"):
        vararg = arguments[-1]
        arguments = arguments[:-1]
    return (arguments, vararg, varkw, defaults)

def parseDocumentation(doc, max_var_arg):
    """
    doc: documentation string
    max_var_arg: maximum number of arguments for variable argument,
                 eg. test(*args).
    """
    prototype = parsePrototype(doc)
    if not prototype:
        return None

    args, varargs, varkw, defaults = prototype
    min_arg = len(args)
    max_arg = min_arg + len(varkw)
    if varargs:
        max_arg += max_var_arg
    return min_arg, max_arg

