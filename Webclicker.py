## v1.0a
## sannes

import urllib2, httplib, socket, sys, threading
from re import search
from time import sleep
from random import randint
from optparse import OptionParser

url = urllib2
parser = OptionParser()

Hello = """
   _____                                    
  / ___/____ _____  ____  ___  _____        
  \__ \/ __ `/ __ \/ __ \/ _ \/ ___/  ______
 ___/ / /_/ / / / / / / /  __(__  )  /_____/
/____/\__,_/_/ /_/_/ /_/\___/____/          
                                            
 _       __     __         ___      __                     ___  ____       
| |     / /__  / /_  _____/ (_)____/ /_____  _____   _   _<  / / __ \____ _
| | /| / / _ \/ __ \/ ___/ / / ___/ //_/ _ \/ ___/  | | / / / / / / / __ `/
| |/ |/ /  __/ /_/ / /__/ / / /__/ ,< /  __/ /      | |/ / /_/ /_/ / /_/ / 
|__/|__/\___/_.___/\___/_/_/\___/_/|_|\___/_/       |___/_/(_)____/\__,_/  
                                                                           
"""

print Hello

## Option's
parser.add_option("-p", dest="proxylist", help="Path to your proxylist", metavar="<Proxy.txt>", type="string")
parser.add_option("-t", dest="timeout", help="Timeout in seconds", metavar="<3>", type="int")
parser.add_option("-b", dest="threads", help="The count of the bots working at same time", metavar="<25>", type="int")
parser.add_option("-n", dest="loggoodp", help="Log good proxies (optional)", metavar="<Checked.txt>", type="string")
parser.add_option("-v", dest="visitlink", help="Visit a link (optional)", metavar="<http://web.de>", type="string")
parser.add_option("-q", dest="quiet", action="store_false", default=True, help="Don't print status messages to stdout (optional)")
parser.add_option("-g", dest="showgoodhits", action="store_false", default=True, help="Only print good status messages to stdout (optimal)")
parser.add_option("-r", dest="goodhit", help="Good hit must contain <STRING> (optional)", metavar="<STRING>", type="string")


try:
    (options, args) = parser.parse_args()
    
    #Open
    if options.proxylist:
        f = open(options.proxylist, 'r')
        proxyl = f.readlines()
    else:
        parser.print_help()
        sys.exit(1)
    
    #Timeout
    if options.timeout:
        timeout = options.timeout
        socket.setdefaulttimeout(timeout)
    else:
        parser.print_help()
        sys.exit(1)
        
    #Threads
    if options.threads:
        threadscount = options.threads+1
    else:
        parser.print_help()
        sys.exit(1)
    
    #New File
    if options.loggoodp:
        n = open(options.loggoodp, 'w')
    
    #Visitlink
    if options.visitlink:
        if "http" not in options.visitlink:
            print "==\t\tPlease insert a complete link (plus http)"
            sys.exit(1)
            
    if options.goodhit:
        if not options.visitlink:
            print "==\t\tPlease use -v <link> if u want to search a String"
            sys.exit(1)
    
    
except IOError, e:
    if "directory" in str(e[1]):
        print "==\t\tCan't open " + options.proxylist
        sys.exit(1)
    else:
        print "==\t\t" + e[1]
        sys.exit(1)
    
## Errorcode's

Errorcode = {
    1: "\t\t== Timed out!",
    111: "\t\t== Connection refused!",
    113: "\t\t== No route to host!",
    503: "\t\t== Service unavailable!",
    404: "\t\t== Not found!",
    400: "\t\t== Bad request!",
    50: "\t\t== Proxy error!",
    403: "\t\t== Forbidden!",
    401: "\t\t== Authorization required!",
    502: "\t\t== Bad Gateway!"
}

## User Agent's

user_agents = [
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506; InfoPath.2)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; de; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.1 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.4; ch; rv:1.9.0.8) Gecko/2009032608 [www.VIS-Network.de]",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6",
    "Opera/9.25(Ubuntu 8.04; U; en)",
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.9) Gecko/2009042115 Fedora/3.0.9-1.fc10 Firefox/3.0.9",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; BrowserVer)",
    "SiteBar/3.3.9 (Bookmark Server; http://sitebar.org/)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.0.9) Gecko/2009040821 Firefox/3.0.8 (de) (TL-FF) (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.9) Gecko/2009040821 Firefox/3.0.9",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.59 Safari/525.19",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.0.9) Gecko/2009040821 Firefox/3.0.4 (de) (TL-FF)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; GTB5; FunWebProducts; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; InfoPath.2)",
    "Opera/9.64 (Windows NT 6.1; U; de) Presto/2.1.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.9) Gecko/2009040820 Firefox/3.0.9"
]

## Thread

class SocketThread(threading.Thread):
    def __init__ (self, proxy):
        self.proxy = proxy
        threading.Thread.__init__ (self)
        
    def run(self):
        self.proxy = self.proxy.lstrip()
        proxy_number = a+1
    
        proxysupport = urllib2.ProxyHandler({"http" : self.proxy})
        opener = urllib2.build_opener(proxysupport)
        urllib2.install_opener(opener)
            
        if options.visitlink:
            Request = urllib2.Request(options.visitlink)
        else:
            Request = urllib2.Request("http://www.google.de")
            
        Request.add_header('User-Agent', user_agents[randint(0,len(user_agents)-1)])
        
        try:
            open = urllib2.urlopen(Request)
            if options.goodhit:
                open_read = open.read()
            
            if options.quiet:
                if options.visitlink:
                    if options.goodhit:
                        if options.goodhit in open_read:
                            print "== Proxy " + str(proxy_number) +" ==\t" + self.proxy + "\t\t== OK! Link visited! \'" + options.goodhit + "\' found!"
                            if options.loggoodp:
                                n.write(self.proxy + "\n")
                        else:
                            if options.showgoodhits:
                                print "== Proxy " + str(proxy_number) +" ==\t" + self.proxy + "\t\t== Proxy is online but didn't found \'" + options.goodhit + "\'"
                    else:
                        print "== Proxy " + str(proxy_number) +" ==\t" + self.proxy + "\t\t== OK! Link visited!"
                        if options.loggoodp:
                            n.write(self.proxy + "\n")
                else:
                    print "== Proxy " + str(proxy_number) +" ==\t" + self.proxy + "\t\t== Online!"
                    if options.loggoodp:
                        n.write(self.proxy + "\n")
            else:
                if options.loggoodp:
                    n.write(self.proxy + "\n")
                    
            open.close()
                
        except (url.URLError, socket.error, httplib.CannotSendRequest, httplib.ResponseNotReady, httplib.BadStatusLine, httplib.InvalidURL), e:
            if options.quiet:
                ErrorString = str(e)
                error_code = search('[0-9]{2,3}', ErrorString) 

                if options.showgoodhits:
                    if "timed out" in ErrorString:
                        print "== Proxy " + str(proxy_number) +" ==\t" + self.proxy + Errorcode[1]
                    else:
                        try:
                            try:
                                l = int(error_code.group(0))
                                print "== Proxy " + str(proxy_number) +" ==\t" + self.proxy + Errorcode[l]
                            except AttributeError:
                                pass
                        except KeyError:
                            print "== Proxy " + str(proxy_number) +" ==\t" + self.proxy + "\t\t== Can't request (Invalid Proxy?)"
            
## Main

if __name__ == "__main__":
    print "\n==\t\tChecking " +str(len(proxyl)) + " proxies with " + str(threadscount-1) + " Bots.\n"
    sleep(2)

    if options.quiet is False:
        print "==\t\tWorking... Please wait\n"

    a = 0
    while a != len(proxyl):
        if threading.activeCount() != threadscount:
            try:
                SocketThread(proxyl[a].rstrip()).start()
                a += 1
            except IndexError:
                pass
            