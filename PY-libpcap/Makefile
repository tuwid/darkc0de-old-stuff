CC         = gcc
SWIG       = swig
LIBDIRS    = -L/usr/local/lib
LIBS       = -lpcap
INCLUDES   = -I/usr/include/python1.5

all:	Pcapmodule.so 

Pcapmodule.so: Pcap_wrap.c
	$(CC) -shared Pcap_wrap.c $(INCLUDES) -o Pcapmodule.so $(LIBDIRS) $(LIBS)

Pcap_wrap.c: Pcap.i 
	$(SWIG) -python Pcap.i

clean:
	rm -f *_wrap* *.o *~ *.so 

