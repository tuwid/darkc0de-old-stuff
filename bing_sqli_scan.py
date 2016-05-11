#/usr/bin/env python
#
# Author: 10n1z3d <10n1z3d[at]w[dot]cn>
# Version: 1.0
# Date: 2009-10-21
#
# Uses Bing API to search given "dork" and then checks 
# every result for possible SQL injection vulnerabillity 
# by adding "'" (single quote) to the end of URL, making request 
# and searching the response's source for error messages.

import re
import sys
import time
import Queue
import urllib
import urllib2
import threading
from xml.dom import minidom

# change these if needed
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3'
BING_APP_ID = 'C2B36F733D8DCB48CE2E075CC145014122BE4724' # might get banned after a while

# do not change below
VERSION = 1.0

DORK = ''
PROXY = ''
FILE_NAME = 'vuln_to_sqli.txt'
CHAR = "'"
MYSQL_ERROR = 'error in your SQL syntax'

SCAN_AMOUNT = 50
NUM_THREADS = 5
SCANNED = 0
MAX_THREADS = 10

VERBOSE_MODE = False
USE_PROXY = False
CREATE_FILE = True

BING_URLS = []
VULN_URLS = []

HEADER =  '\t     _____ _            \n'\
          '\t    | __  |_|___ ___    \n'\
          '\t    | __ -| |   | . |   \n'\
          '\t    |_____|_|_|_|_  |   \n'\
          '\t                |___|   \n'\
          '\t   MySQL Error Scanner  \n'\
          '\t   10n1z3d[at]w[dot]cn  \n'

# Prints out the usage and options
def printHelp():
    print 'Usage: ./bing_sqli_scan.py <dork> <url amount to check> <threadcount> [options]\n'
    print 'Options: -p, --proxy    <ip:port>   |   Use proxy (http only)'
    print '         -v, --verbose              |   Verbose mode on'
    print '         -f, --file     <filename>  |   Output file'
    print '         -e, --error    <error>     |   Error for which to look for'
    print '                                        Default is: "%s"\n' % MYSQL_ERROR
    print 'Example: ./bing_mysqli_scan.py images.php?id= 500 5 -p 123.124.123.124:8080 -v -f vuln.txt\n'

# Parses the script arguments
def parseArgs():
    global DORK, PROXY, FILE_NAME, SCAN_AMOUNT, VERBOSE_MODE, NUM_THREADS, MYSQL_ERROR, CREATE_FILE, USE_PROXY
    
    DORK = sys.argv[1]
    
    if int(sys.argv[3]) <= MAX_THREADS:
        NUM_THREADS = int(sys.argv[3])
    else:
        print '[-] The maximun thread count is %s. Quitting...' % MAX_THREADS
        exit(0)
        
    if not int(sys.argv[2]) % 50:
        SCAN_AMOUNT = int(sys.argv[2])
    else:
        print '\n[-] Invalid scan amount, the step is 50, e.g. 50, 100, 150, 200... Quitting...\n'
        exit(0)
        
    for arg in sys.argv[1:]:
        if arg.lower() == '-h' or arg.lower() == '--help':
            printHelp()
            exit(0)
            
        if arg.lower() == '-p' or arg.lower() == '--proxy':
            PROXY = sys.argv[int(sys.argv[1:].index(arg))+2]
            USE_PROXY = True
            
        if arg.lower() == '-v' or arg.lower() == '--verbose':
            VERBOSE_MODE = True
            
        if arg.lower() == '-f' or arg.lower() == '--file':
            FILE_NAME = sys.argv[int(sys.argv[1:].index(arg))+2]
            CREATE_FILE = True
            
        if arg.lower() == '-e' or arg.lower() == '--error':
            MYSQL_ERROR = sys.argv[int(sys.argv[1:].index(arg))+2]

# Parses the Bing search result
def bingSearch(query, index):
    global BING_URLS
    
    url = 'http://api.search.live.net/xml.aspx?Appid='+BING_APP_ID+'&query='\
          +urllib.quote(query)+'&sources=web&market=en-us&web.count=50&web.offset='+str(index)
    xml = minidom.parse(urllib2.urlopen(url))
    
    for node in xml.getElementsByTagName('web:Url'):
        BING_URLS.append(node.childNodes[0].data)

# Checks the urls for errors
class sqliScanner(threading.Thread):
    def __init__(self, queue):
        self.__queue = queue
        threading.Thread.__init__(self)
        
    def run(self):
        global SCANNED
        while True:
            url = self.__queue.get()
            if url is None:
                break
            
            if VERBOSE_MODE:
                sys.stdout.write('[+] Scanning => %s\n' % url)
            
            try:
                if USE_PROXY:
                    proxyHandler = urllib2.ProxyHandler({'http' : 'http://' + PROXY + '/'})
                    opener = urllib2.build_opener(proxyHandler)
                    opener.addheaders = [('User-Agent', USER_AGENT)]
                    response = opener.open(url + CHAR).read()
                else:
                    req = urllib2.Request(url + CHAR)
                    req.add_header('User-Agent', USER_AGENT)
                    response = urllib2.urlopen(req).read()
                
                if re.search(MYSQL_ERROR, response):
                    if not url in VULN_URLS:
                        sys.stdout.write("[+] Found Error => %s'\n" % url)
                        VULN_URLS.append(url)
            except:
                pass
            
            SCANNED += 1

# Starts the 
def startThreads():
    queue = Queue.Queue(0)
    for i in range(NUM_THREADS):
        inst = sqliScanner(queue).start()
        
    for i in range(len(BING_URLS)):
        queue.put(BING_URLS[i])
        
    for i in range(NUM_THREADS):
        queue.put(None)

# Writes the output file
def writeResults():
    handle = open(FILE_NAME, 'a')
    handle.write(HEADER)
    handle.write('\n[+] Dork: %s\n' % DORK)
    handle.write('[+] Sites Scanned: %s\n' % len(BING_URLS))
    handle.write('[+] Vulnerable: %s\n' % len(VULN_URLS))
    handle.write('\n[+] Scan results for "%s":\n\n' % DORK)
    
    for url in VULN_URLS:
        handle.write(url+"'\n")
    handle.close()

# Main 
def main():
    print HEADER
    if len(sys.argv) not in [4,5,6,7,8,9,10]:
        printHelp()
        exit(0)
    else:
        parseArgs()
        print '\n[+] Dork: %s' % DORK
        print '[+] Sites to scan: %s' % SCAN_AMOUNT
        print '[+] Scan threads: %s' % NUM_THREADS
        print '[+] Parsing %s Bing results...' % SCAN_AMOUNT
        for i in range(0, (SCAN_AMOUNT / 50)):
            bingSearch(DORK, 1+i)
        print '[+] Parsing done.'
        print '[+] Starting %s scan threads...' % NUM_THREADS
        startThreads()
        if not VERBOSE_MODE:
            print '[+] Scanning...\n'
        while SCANNED < len(BING_URLS):
            time.sleep(1)
        print '\n[+] Scanning done.\n'
        print '[+] Scanned %s URLs' % len(BING_URLS)
        print '[+] Vulnerable: %s' % len(VULN_URLS)
        if CREATE_FILE:
            print '[+] Creating "%s"...' % FILE_NAME
            writeResults()
        print '[+] Done.'
        exit(0)
    
if __name__ == "__main__":
    main()
