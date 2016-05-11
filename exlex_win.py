#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# exlex_win.py
# 
# Version: 1.0
# 
# Copyright (C) 2009  novacane novacane[at]dandies[dot]org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# TODO
# () linux compatibility
# () switch output mode

import os
import sys
import socket
import datetime
import re
from operator import itemgetter
from optparse import OptionParser

def main(logfile, importips=False):
    
    matches = {}
    cachedips = []
    count_cached = 0
    count_iips = 0
    
    ip_pattern = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
    
    #http://docs.python.org/library/socket.html
    HOST = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    s.bind((HOST, 0))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    if os.path.exists(logfile):
        try:
            f_src = open(logfile)
        except IOError:
            print "!> Error reading from logfile!"
            print "!> " + logfile
            sys.exit(1)
        print ">> Reading logfile: %s" % logfile
        for line in f_src:
            try:
                ip = line.replace("\n", "").split()[2]
            except IndexError:
                print "!> Error while reading IPs from logfile!"
                print "!> " + logfile
                sys.exit(1)
            # check input for valid ip address
            if ip_pattern.match(ip):
                cachedips.append(ip)
            else:
                print "!> Invalid IP address in line:"
                print "!>> " + line
                sys.exit(1)
        f_src.close()
        count_cached = len(cachedips)
        print ">> Existing IP Addresses: " + str(count_cached)
        
    if importips:
        if os.path.exists(importips):
            try:
                f_iips = open(importips)
            except IOError:
                print "!> Error reading from import file!"
                print "!> " + importips
                sys.exit(1)
            print ">> Caching IP Addresses from import file: %s" % importips
            for line in f_iips:
                try:
                    iip = line.replace("\n", "")
                except IndexError:
                    print "!> Error while reading IPs from import file!"
                    print "!> " + importips
                    sys.exit(1)
                # check input for valid ip address
                if not ip_pattern.match(iip):
                    print "!> Invalid IP address in line:"
                    print "!>> " + line
                    sys.exit(1)
                if iip not in cachedips:
                    matches[iip] = str(datetime.datetime.now())
                else:
                    print "!> " + iip + " already imported!"
            f_iips.close()
            count_iips = len(matches)
            print ">> Imported IP Addresses: " + str(count_iips)
        else:
            print "!> Could not find import file!"
            print "!> " + importips
            sys.exit(1)
    try:
        f_dst = open(logfile, "a")
    except IOError:
        print "!> Error writing to logfile!"
        print "!> " + logfile
        sys.exit(1)
    print ">> Sniffing for Hosts..."
    while 1:
        try:
            sniffedstr,addr = s.recvfrom(65536)
            host,port = addr
            if not addr[0] in cachedips and addr[0] not in matches:
                matches[addr[0]] = str(datetime.datetime.now())
                print addr[0]
        except KeyboardInterrupt:
            break
    
    if count_iips == 0:
        count_new = len(matches)
    else:
        count_new = len(matches) - count_iips
    
    count_total = count_new + count_cached + count_iips

    # performance optimized method to sort dictionary
    # thanks to writeonly.wordpress.com
    for addr, time in sorted(matches.iteritems(), key=itemgetter(1)):
        f_dst.write(time + " " + addr + "\n")
    print ">> ...\n>> FINISHED!\n>> New IP Addresses: " + str(count_new)
    print ">> Total: " + str(count_total)
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    f_dst.close()

if __name__ == '__main__':
    
    usage = "usage: %prog [options] outfile"
    parser = OptionParser(usage=usage, version="%prog 1.0")
    parser.add_option("-i", "--import", action="store", type="string",
                      metavar="FILE", dest="importips",
                      help="Import IP Adresses form file")
    (options, args) = parser.parse_args()
    
    if len(args) != 1:
        print "\n\t[*] exlex_win 1.0 [*]"
        print "\n\tTry: exlex_win.py  --help\n"
        sys.exit(2)
        
    if options.importips:
        main(args[0], options.importips)
    else:
        main(args[0])
