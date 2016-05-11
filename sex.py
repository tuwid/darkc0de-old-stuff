#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# 
# sex.py 
# 
# Version: 2.0 
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
# Thanks to regular-expressions.info for your regex pattern! 
# DO NOT FORGET TO INSTALL DNSPYTHON - http://www.dnspython.org/ 
# 
 
import os 
import sys 
import re 
import smtplib 
import dns.resolver 
from optparse import OptionParser 
 
def main(source, destination, verbose, sort, remove_duplicates, exclude_ext): 
 
    #email_pattern = re.compile( 
    #r"""[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z 
    #0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?""") 
    email_pattern = re.compile( 
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b", re.I) 
    matches = [] 
 
    try: 
        file_dst = open(destination, "w") 
    except IOError: 
        print "!> ERROR: %s" % destination 
        sys.exit(1) 
 
    if os.path.isfile(source): 
        try: 
            file_src = open(source) 
            if verbose == 2: print ">> FILE: %s" % source 
        except IOError: 
            print "!> ERROR: %s" % source 
            sys.exit(1) 
        for line in file_src: 
            for match in email_pattern.findall(line): 
                matches.append(match) 
                if verbose == 1: 
                    print match 
                elif verbose == 2: 
                    print ">> FOUND: %s" % match 
    elif os.path.isdir(source): 
        for root, dirs, files in os.walk(source, topdown=False): 
            for name in files: 
                fpath = os.path.join(root, name) 
                if name.find(".") != -1: 
                    if name.split(".")[1] in exclude_ext: 
                        if verbose == 2: 
                            print "!> EXCLUDE: %s" % fpath 
                        continue 
                try: 
                    file_src = open(fpath) 
                    if verbose == 2: print ">> FILE: %s" % fpath 
                except IOError: 
                    print "!> ERROR: %s" % fpath 
                    continue 
                for line in file_src: 
                    for match in email_pattern.findall(line): 
                        matches.append(match) 
                        if verbose == 1: 
                            print match 
                        elif verbose == 2: 
                            print ">> FOUND: %s" % match 
                file_src.close() 
    else: 
        print "!> ERROR: %s" % source 
        sys.exit(1) 
 
    if remove_duplicates == 1: matches = list(set(matches)) 
    if verbose == 2: print ">> Extraced email addresses: " + str(len(matches)) 
    if sort == 1: matches.sort() 
    for i in matches: 
        file_dst.write(i + "\n") 
 
    file_src.close() 
    file_dst.close() 
 
def verify_email_address(email_addresses): 
 
    """ Get SMTP return code 
 
    Verify emails by checking the "RCPT TO" return code from the SMTP server. 
    NOTE: dropped vrfy command because provider disabled it to prevent attacks 
 
    """ 
 
    failed_domains = [] 
 
    try: 
        # Open the Source-File. 
        file_emails = open(email_addresses) 
    except IOError: 
        print "!> ERROR: %s" % email_addresses 
        sys.exit(1) 
 
    # Loop through addresses. Each line represents an email-address. 
    for line in file_emails: 
        # Remove Linefeed. 
        line = line.replace("\n", "") 
        # The actual domain. 
        domain = line.split("@")[1] 
 
        # Do nothing if domain is already in the failed_domain list. 
        if not domain in failed_domains: 
            try: 
                # Make a MX DNS query. 
                answers = dns.resolver.query(domain, "MX") 
                # OR: mx = str(answers[1].exchange)[:-1] 
                for rdata in answers: 
                    # Remove the dot from rdata.exchange. 
                    mx = str(rdata.exchange)[:-1] 
                    try: 
                        # Connect to SMTP server. 
                        smtp = smtplib.SMTP(mx) 
                        # Polite people say hello first. 
                        smtp.docmd("HELO microsoft.com") 
                        # Indicates who is sending the mail. 
                        smtp.docmd("MAIL FROM:", "<asdf@microsoft.com>") 
                        # Indicates who is recieving the mail. 
                        rcpt = smtp.docmd("RCPT TO:", "<" + line + ">") 
                        # Print output. 
                        print line + "," + mx + "," + \ 
                        str(rcpt[0]) + "," + str(rcpt[1]) 
                        # Close SMTP connection. 
                        smtp.quit() 
                    except smtplib.SMTPServerDisconnected: 
                        # Add domain to list. 
                        failed_domains.append(domain) 
                    # Use only the first server-address. 
                    break 
 
            # Raise exception. 
            except dns.resolver.NXDOMAIN: 
                # Add domain to list. 
                failed_domains.append(domain) 
            except dns.resolver.NoAnswer: 
                # Add domain to list. 
                failed_domains.append(domain) 
            except: 
                pass 
 
    # Close the Source-File. 
    file_emails.close() 
 
    # Output failed domains. 
    if failed_domains: 
        for item in failed_domains: print "!> FAILED: %s" % item 
 
    sys.exit() 
 
if __name__ == '__main__': 
 
    help_message = "\n\t[*] Smashing Email eXtractor 2.0 [*] \ 
                   \n\t[*] by dandies.org [*] \ 
                   \n\n\tTry: sex.py  --help\n" 
    usage = "\n  %prog [options] <source> <destination> \ 
            \n  %prog [-lqsr] [-e ext1,ext2] <source> <destination> \ 
            \n  %prog -y <file>" 
    parser = OptionParser(usage=usage, version="%prog 2.0") 
    parser.add_option("-l", "--list", 
                  action="store_true", dest="list", 
                  help="display email addresses only") 
    parser.add_option("-q", "--quiet", 
                  action="store_true", dest="quiet", 
                  help="silent output mode") 
    parser.add_option("-s", "--sort", 
                  action="store_true", dest="sort", 
                  help="sort addresses in alphabetical order") 
    parser.add_option("-r", "--remove-duplicates", 
                  action="store_true", dest="remove_duplicates", 
                  help="remove duplicated emails") 
    parser.add_option("-e", "--exclude-extension", 
                  metavar="EXTENSION", dest="exclude_ext", 
                  help="exclude files by extension") 
    parser.add_option("-y", metavar="FILE", dest="email_addresses", 
                  help="verify emails from file") 
 
    (options, args) = parser.parse_args() 
 
    if options.email_addresses and len(args) == 0: 
        verify_email_address(options.email_addresses) 
    elif options.email_addresses and len(args) != 0: 
        print help_message 
        sys.exit(2) 
    elif len(args) != 2: 
        print help_message 
        sys.exit(2) 
 
    if options.list and options.quiet: 
        parser.error("options -l and -q are mutually exclusive") 
 
    # Set default values here. 
    verbose = 2 
    sort = 0 
    remove_duplicates = 0 
    exclude_ext = [] 
 
    if options.exclude_ext: 
        exclude_ext = options.exclude_ext.split(",") 
    if options.list: 
        verbose = 1 
    if options.quiet: 
        verbose = 0 
    if options.sort: 
        sort = 1 
    if options.remove_duplicates: 
        remove_duplicates = 1 
 
    main(args[0], args[1], verbose, sort, remove_duplicates, exclude_ext)
