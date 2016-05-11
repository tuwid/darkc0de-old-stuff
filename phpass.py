#!/usr/bin/env python 
import sys, md5 
 
def license(): 
    '''Print the usage license to this software, yeah, it's the same as above''' 
    print ''' 
    phpassbrute.py - phpass salted hash brute force, works against any hash 
    that use this framework to crypt and store hashed passwords, some projects that 
    use it: Wordpress, Drupal, bbPress, phpBB3 and any others. 
 
    Copyright (c) 2009  Ulisses "thebug" Castro <uss.thebug@nospam@gmail.com> 
 
    Functions encode64() and crypt_private() are from phpass module: 
    Copyright (c) 2008, Alexander Chemeris <Alexander.Chemeris@nospam@gmail.com> 
 
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
 
def encode64(input_val, count, itoa64): 
    ''' Encode binary data from input_val to ASCII string. 
 
    Every six bits of input_val are represented by corresponding 
    char from 64-char length itoa64 array. That is 0 will be 
    represented in resulting string with char itoa64[0], 1 will 
    be represented with itoa64[1], ..., 63 will be represented 
    with itoa64[63]. 
    ''' 
    output = '' 
    i = 0 
 
    while i<count: 
        value = ord(input_val[i]) 
        i = i+1 
        output = output + itoa64[value&0x3f] 
 
        if i < count: 
            value = value | (ord(input_val[i]) << 8) 
 
        output = output + itoa64[(value>>6)&0x3f] 
 
        i = i+1 
        if i >= count: 
            break 
 
        if i < count: 
            value = value | (ord(input_val[i]) << 16) 
 
        output = output + itoa64[(value>>12)&0x3f] 
 
        i = i+1 
        if i >= count: 
            break 
 
        output = output + itoa64[(value>>18)&0x3f] 
 
    return output 
 
def crypt_private(passwd, passwd_hash, hash_prefix='$P$'): 
    ''' Hash password, using same salt and number of 
        iterations as in passwd_hash. 
 
    This is useful when you want to check password match. 
    In this case you pass your raw password and password 
    hash to this function and then compare its return 
    value with password hash again: 
 
       is_valid = (crypt_private(passwd, hash) == hash) 
 
    hash_prefix is used to check that passwd_hash is of 
    supported type. It is compared with first 3 chars of 
    passwd_hash and if does not match error is returned. 
 
    NOTE: all arguments must be ASCII strings, not unicode! 
    If you want to support unicode passwords, you could 
    use any encoding you want. For compatibility with PHP 
    it is recommended to use UTF-8: 
 
       passwd_ascii = passwd.encode('utf-8') 
           is_valid = (crypt_private(passwd_ascii, hash) == hash) 
 
        Here hash is already assumed to be an ASCII string. 
 
        In case of error '*0' is usually returned. But if passwd_hash 
        begins with '*0', then '*1' is returned to prevent false 
        positive results of password check. 
    ''' 
    itoa64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' 
    output = '*0' 
    # Prevent output from being the same as passwd_hash, because 
    # this may lead to false positive password check results. 
    if passwd_hash[0:2] == output: 
        output = '*1' 
 
    # Check for correct hash type 
    if passwd_hash[0:3] != hash_prefix: 
        return output 
 
    count_log2 = itoa64.index(passwd_hash[3]) 
    if count_log2<7 or count_log2>30: 
        return output 
    count = 1<<count_log2 
 
    salt = passwd_hash[4:12] 
    if len(salt) != 8: 
        return output 
 
    m = md5.new(salt) 
    m.update(passwd) 
    tmp_hash = m.digest() 
    for i in xrange(count): 
        m = md5.new(tmp_hash) 
        m.update(passwd) 
        tmp_hash = m.digest() 
 
    output = passwd_hash[0:12]+encode64(tmp_hash, 16, itoa64) 
    return output 
 
def makelist(file): 
    ''' 
    Make lists 
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
 
 
if __name__ == '__main__': 
    from optparse import OptionError 
    from optparse import OptionParser 
 
    version = '''---------------------------------------------------------------------- 
 phpass hash brute force 
 version 0.1                                  uss.thebug[at]gmail.com 
----------------------------------------------------------------------''' 
 
    usage = '%s [-w wordlist] [-t threads] [-v]' % sys.argv[0] 
 
    parser = OptionParser(version=version, usage=usage) 
 
    parser.add_option('-w', dest='wordlist', help='wordlist to run against hash') 
    parser.add_option('-p', dest='prefix', default='$P$', help='hash prefix (default: %default)') 
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', help='verbose') 
    parser.add_option('-l', '--license', action='store_true', dest='license', help='license') 
 
    (options, args) = parser.parse_args() 
 
    if options.license: 
        license() 
        sys.exit(0) 
 
    if not options.wordlist: 
        parser.print_help() 
        sys.exit(1) 
 
    prefix   = options.prefix 
    wordlist = options.wordlist 
 
    results = [] 
 
    words = makelist(wordlist) 
 
    print "[*] phpass hash brute force tool (by thebug)" 
    print "[*] hash prefix: %s" % prefix 
    hash = raw_input("[*] paste hash here: ") 
    print "[*] %s word(s) loaded." % str(len(words)) 
    print "[*] brute force started." 
 
    for word in words: 
        if options.verbose: 
            print "[+] word: %s" % word 
 
        is_valid = (crypt_private(word, hash, prefix) == hash) 
 
        if is_valid: 
            print "\n[*] got it!" 
            print "[*] password is: %s\n" % word 
            sys.exit(0) 
        else: 
            pass 
 
    print "[*] Done.\n" 
    sys.exit(0)
