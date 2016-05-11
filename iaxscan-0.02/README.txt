Use scan_hosts.py and scan_users.py to discover live IAX2 hosts and user accounts. The only
dependency is that you have Python installed. I tested using 2.4 and 2.5.

The interfaces are quite minimal at the moment and the host and user scanners support a variety of 
options not available through the UIs at the moment (e.g padding of usernames with zeroes). To
access these either change the respective scanner in scanner.py or add the code to the interface
to accept these options on the command line.

That said, most things you would want are available through the interfaces and everything appears
to work quite well. If you have any trouble then send on the crash details or problem to 
nnp@unprotectedhex.com

-nnp, 9th October 2008