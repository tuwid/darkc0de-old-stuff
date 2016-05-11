from socket import AF_INET

def formatAddress(family, address, short=False):
    if family == AF_INET:
        host, port = address
        if not host:
            host = '(localhost)'
        if not short:
            return "(host %s, port %s)" % (host, port)
        else:
            return "%s:%s" % (host, port)
    else:
        return repr(address)

