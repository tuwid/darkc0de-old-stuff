Network client
==============

Method:
 * __init__(project, host, port, timeout=10.0): constructor
 * sendBytes(bytes): send bytes on socket. Return value: False on error, True
   on success

Attribute:
 * host: host name/IP address
 * port: port number
 * timeout: socket timeout (in second)
 * tx_bytes: number of bytes sent to host
 * socket: socket object (set to None on error)

