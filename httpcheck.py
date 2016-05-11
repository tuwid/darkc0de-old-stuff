#!/usr/bin/python 
 
# Name: httpcheck 
# Version: 0.1 
# Author: intense2k 
# Description: scans a range of ips and checks results with a regular expression 
 
import sys 
import socket 
import httplib 
import re 
import Queue 
import thread 
import threading 
 
def convert_to_num(ip): 
    data = ip.split(".") 
    if len(data) != 4: 
        return -1 
 
    addr = 0 
    prod = 256 * 256 * 256 
    for i in range(0, 4): 
        data[i] = int(data[i]) 
        if data[i] < 0 or data[i] > 255: 
            return 
        addr = addr + prod * data[i] 
        prod = prod / 256 
 
    return addr 
 
def convert_to_ip(num): 
    tmp = num 
    quot = 256 * 256 * 256 
    ip = [] 
    for i in range(0, 4): 
        a = tmp % quot 
        b = (tmp - a) / quot 
        ip.append(str(b)) 
        quot = quot / 256 
        tmp = a 
    return '.'.join(ip) 
 
def httpcheck(host, filename, regex, timeout): 
    global log 
    socket.setdefaulttimeout(timeout) 
    try: 
        sockfd = httplib.HTTPConnection(host) 
        sockfd.request('GET', filename) 
        response = sockfd.getresponse() 
        data = response.read() 
        if re.compile(regex).search(data): 
            log.acquire() 
            print 'http://' + host + filename 
            log.release() 
    except: 
        pass 
    sockfd.close() 
 
def worker(): 
    global iplist 
    global filename 
    global regex 
 
    while True: 
        host = iplist.get() 
        httpcheck(host, filename, regex, 3) 
        iplist.task_done() 
 
def main(argv): 
    global iplist 
    global regex 
    global filename 
 
    print '\n httpcheck v0.1 - coded by intense2k' 
 
    if len(argv) < 6: 
        print ' Usage: ./httpcheck <start> <end> <threads> <filename> <regex>' 
        print ' e.g. : ./httpcheck 192.168.1.1 192.168.1.255 10 /bla.php (a|b)' 
        return 
 
    start = convert_to_num(argv[1]) 
    end = convert_to_num(argv[2]) 
    threads = int(argv[3]) 
    filename = argv[4] 
    regex = argv[5] 
 
    if threads < 1: 
        print ' Invalid value entered for <threads>' 
        return 
 
    if start == -1 or end == -1: 
        print ' Invalid IP range given, check your input!' 
        return 
 
    if start > end: 
        tmp = start 
        start = end 
        end = tmp 
 
    for i in range(0, threads): 
        t = threading.Thread(target = worker) 
        t.setDaemon(True) 
        t.start() 
 
    end = end + 1 
    for i in range(start, end): 
        ip = convert_to_ip(i) 
        iplist.put(ip) 
 
    iplist.join() 
 
log = thread.allocate_lock() 
iplist = Queue.Queue() 
filename = '' 
regex = '' 
 
if __name__ == '__main__': 
    main(sys.argv) 
