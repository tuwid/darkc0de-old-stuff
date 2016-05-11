#!/usr/bin/env python 
import sys 
 
try: 
    import hashlib 
except ImportError: 
    print ''' 
    You need hashlib. 
    Update your python to version 2.5\n''' 
    sys.exit(1) 
 
def license(): 
    '''Print the usage license to this software, yeah, it's the same as above''' 
    print ''' 
    %s - MySQL double SHA1 hash wordlist brute forcer. This cracker works against 
    hash created by MySQL to store passwords. 
 
    Copyright (c) 2009  Ulisses "thebug" Castro <uss.thebug@nospam@gmail.com> 
 
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
    ''' % sys.argv[0] 
 
def makelist(file): 
    ''' 
    Make word list 
    ''' 
    items = [] 
 
    try: 
        fd = open(file, 'r') 
 
        for line in fd.readlines(): 
            item = line.replace('\n', '').replace('\r', '') 
            items.append(item) 
 
        return items 
 
    except IOError: 
        print 'unable to read file \'%s\'' % file 
        pass 
 
    except Exception, e: 
        print 'unknown error' 
        pass 
 
def testword(text): 
    """ 
    Hash string twice with SHA1 (double SHA1), make UPPER and add an asterix. 
    """ 
    pazz = hashlib.sha1(text).digest() 
    pazz2 = hashlib.sha1(pazz).hexdigest() 
    return "*" + pazz2.upper() 
 
if __name__ == '__main__': 
    from optparse import OptionError 
    from optparse import OptionParser 
 
    version = '''---------------------------------------------------------------------- 
 MySQL double SHA1 hash brute force 
 version 0.1                                  uss.thebug[at]gmail.com 
----------------------------------------------------------------------''' 
 
    usage = '%s [-H hash] [-w wordlist] [-t word-to-hash] [-v]' % sys.argv[0] 
 
    parser = OptionParser(version=version, usage=usage) 
 
    parser.add_option('-H', dest='hash', help='hash. (format: *6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9)') 
    parser.add_option('-w', dest='wordlist', help='wordlist to run against hash') 
    parser.add_option('-t', dest='wordtohash', help='transform word to hash') 
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', help='verbose') 
    parser.add_option('-l', '--license', action='store_true', dest='license', help='license') 
 
    (options, args) = parser.parse_args() 
 
    hash       = options.hash 
    wordlist   = options.wordlist 
    wordtohash = options.wordtohash 
 
    if options.license: 
        license() 
        sys.exit(0) 
 
    if options.wordtohash: 
        print "[*] MySQL double SHA1 hasher (by thebug)" 
        print "[*] word: %s" % wordtohash 
        print "[*] hash: %s" % testword(wordtohash) 
        sys.exit(0) 
 
    if not options.wordlist: 
        parser.print_help() 
        sys.exit(1) 
 
    if int(len(hash)) != 41 or hash[:1] != "*": 
        print "Improper hash format. Format: *6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9\n" 
        sys.exit(1) 
 
    words = makelist(wordlist) 
 
    print "[*] MySQL double SHA1 hash brute force (by thebug)" 
    print "[*] hash: %s" % hash 
    print "[*] %s word(s) loaded." % str(len(words)) 
    print "[*] brute force started." 
 
    for word in words: 
        if options.verbose: 
            print "[+] word: %s" % word 
 
        if hash == testword(word): 
            print "\n[*] got it!" 
            print "[*] password is: %s\n" % word 
            sys.exit(0) 
        else: 
            pass 
 
    print "[*] Done.\n" 
    sys.exit(0)
