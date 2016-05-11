#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""
pide.py

pide (Python Intrusion Detection Enviroment) is an intrusion detection
system for checking the integrity of files. Basically a python implemenation
of tripwire/aide. Can read AIDE/Tripwire config files, but does not
make AIDE/Tripwire compatible databases..

Implements most of the functionality of AIDE.


Copyright (C) 2004 - Lars Strand <lars strand at gnist org>
 
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

http://www.gnu.org/copyleft/gpl.html


TODO:
* xml data format
* crypt database --> problem with 3rd party modules...
  http://rogue.amk.ca/pipermail/pct/2003-July/000022.html

Changelog:
 DONE --> warn dead symlinks!
 DONE --> stats on directories as well
 DONE --> +S (ok if size is the same or growing) --> gives a small preformance
          penalty, since more cheks has to be added
 DONE --> access by name! not in tuple
          http://mail.python.org/pipermail/patches/2001-December/006887.html
 DONE --> add group of files - added globbing
 DONE --> compressed database
 DONE --> +b (add number of blocks)
 DONE --> if rules is only letters (the same as +) - REVERTED!!
 DONE --> rule-options ==> binLib-p-sha1
 DONE --> degree of summary: short, normal, detail
 DONE --> +sha1 or -sha1 also is interpreted as +a etc..
          attributes MUST have + or - in front..
 DONE --> add more template rules
 DONE --> verbose setting
 DONE --> check for save new db and old db BEFORE doing any stats!
 SHOULD BE OK NOW - done some sanity checks on =, $ and *!
 DONE --> version control (must have at least python ver. 2.3)
"""

# Package definitions.
__program__   = 'PIDE'
__version__   = '0.6'
__date__      = '2004/22/03'
__author__    = 'Lars Strand <lars at unik no>'
__licence__   = 'GPL'
__copyright__ = 'Copyright (C) 2004 Lars Strand'


import getopt, sys, os, os.path, re, glob, stat, md5, sha, tempfile, time, gzip, string

########################## makeSysDB
def makeSysDB(buildpaths, confvar):
    """We get a dictionary of 'file => att' and a list of
    attributes.
    for each file:
      - make stats according to 'att'
      - save stats to db
    return db
      """

    sysDB = {}
    # for each file
    for file in buildpaths:
        attributes = buildpaths[file]
        if verbose: print "stat:", file,

        # The stats datastructure:
        # filename => [stat1, stat2, stat3, .....], filename2 => [stat1. stat2...]
        # file = [perm, inode, lcount, uid, gid, size, blocks, atime, mtime, ctime, md5, sha1]
        sysDB[file] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        # stat the file, print warning if dead symlink
        if os.path.islink(file) and confvar['warn_dead_symlinks'] == 'yes':
            try:
                filemode = os.stat(file)
            except: # the stat will fail if dead symlink
                print "WARNING: Dead symlink? %s" % file
                
        else:
            try:
                filemode = os.stat(file)
            except:
                print "WARNING: Unable to stat file '%s'" % file
      
        # extract and put the stat in the right place
        # NB! if the rule contain both + and -, the + has presedence
        # +S (check for growing size) is not here, must do a check
        # of this size and the old one.
            
        # The rest of the stats 
        if '+p' in attributes:           # permission and file mode bits
            if verbose: print "+p",
            sysDB[file][0] = filemode.st_mode   
        if '+i' in attributes:           # inode number
            if verbose: print "+i",
            sysDB[file][1] = filemode.st_ino
        if '+n' in attributes:           # number of (hard) links
            if verbose: print "+n",
            sysDB[file][2] = filemode.st_nlink
        if '+u' in attributes:           # user id of owner
            if verbose: print "+u",
            sysDB[file][3] = filemode.st_uid
        if '+g' in attributes:           # group id of owner
            if verbose: print "+g",
            sysDB[file][4] = filemode.st_gid
        if '+s' or '+S' in attributes:   # size of file
            if verbose and '+s' in attributes: print "+s",
            if verbose and '+S' in attributes: print "+S",
            sysDB[file][5] = filemode.st_size 
        if '+b' in attributes:           # number of blocks
            if verbose: print "+b",
            sysDB[file][6] = filemode.st_blocks
        if '+a' in attributes:           # access timestamp
            if verbose: print "+a",
            sysDB[file][7] = filemode.st_atime
        if '+m' in attributes:           # modification timestamp
            if verbose: print "+m",
            sysDB[file][8] = filemode.st_mtime
        if '+c' in attributes:           # inode creation timestamp
            if verbose: print "+c",
            sysDB[file][9] = filemode.st_ctime

        if os.path.isfile(file):
            if '+md5' in attributes:         # MD5 signature
                if verbose: print "+md5",
                # open the file
                try:
                    f = open(file, 'rb')
                except:
                    print "Unable to open %s for MD5 hash" % file
                    continue
            
                hash = md5.new()
            
                # read the file in chuncks
                while 1:
                    r = f.read(8096)
                    if not r:
                        break
                    hash.update(r) # feed the hash object
                
                f.close()
            
                sysDB[file][10] = hash.hexdigest()

        if os.path.isfile(file):
            if '+sha1' in attributes:       # SHA1 signature
                if verbose: print "+sha1",
                # open the file
                try:
                    f = open(file, 'rb')
                except:
                    print "Unable to open %s for SHA-1 hash" % file
                    continue

                hash = sha.new()

                # read the file in chuncks
                while 1:
                    r = f.read(8096)
                    if not r:
                        break
                    hash.update(r) # feed the hash object
                
                f.close()
                    
                sysDB[file][11] = hash.hexdigest()

        # some space
        if verbose: print ""

    # debug
    #import pprint
    #pprint.pprint(sysDB)
    return sysDB

########################## buildPaths
def buildPaths(rcfile):
    """Read the config file:
    * read all config variables (if any)
    * read all rules (if any give) - a set of default rules listed
    * read files (os.walk)
    
    Returns a 'files' (dict) of 'files => attributs' and
    confvar (dict) of 'variablename => value'"""

    # read the config file
    try:
        ifile = open(rcfile, 'r')
    except:
        usage("Unable to open config file: %s" + ifile)
        sys.exit(1)

    # read the config file
    
    # grep '#' lines
    comment   = re.compile(r"\s*\#.*")
    # blank lines
    blanks    = re.compile(r"^$")
    
    # database
    dbfile     = r"\s*database=file:(\S+)"
    dbfilenew  = r"\s*database_out=file:(\S+)"
    dbzip      = r"\s*gzip_dbout=(\S+)"
    dbcrypt    = r"\s*crypt_dbout=(\S+)"
    dbcryptkey = r"\s*crypt_key=(\S+)"
    dbwarnsym  = r"\s*warn_dead_symlinks=(\S+)"
    
    # crypt add - public key or password?

    # length of summary
    summary   = r"\s*summary=(\S+)"
    
    # dictionary to hold optional variables
    # fill inn some default variables
    confvar   = {
        'database'           : '/var/db/pide/pide.db',
        'database_out'       : '/var/db/pide/pide.db.new',
        'gzip_dbout'         : 'yes',
        'crypt_dbout'        : 'no',
        'warn_dead_symlinks' : 'no',
        'summary'            : 'normal'
        }            #print "POP!"

    
    # all defined enviroment variables get exported (for us with cron)
    # @@define MAILTO to@address.org
    envvar    = re.compile(r"\s*@@define\s+(\S+)\s+(\S+)")

    # undef enviroment variables
    # @@undef VAR
    uenvvar   = re.compile(r"\s*@@undef\s+(\S+)")
    
    # custom rules:
    # Binlib = +p+i+n+u+g+s+b+m+c+md5+sha1
    rule      = re.compile(r"\s*(\S+)\s*=\s*(.+)")

    #    p :  permission and file mode bits      a: access timestamp
    #    i :  inode number                       m: modification timestamp
    #    n :  number of links (ref count)        c: inode creation timestamp
    #    u :  user id of owner                 md5: MD5 signature
    #    g :  group id of owner              tiger: tiger signature  (not implemented)
    #    s :  size of file                  rmd160: RMD160 signature (not implemented)
    #    b :  number of blocks (Linux)        sha1: SHA1 signature
    #    S :  check for growing size
    #
    # Predefined template rules:
    # Note!! '+' (plus) has presedence over '-' (minus), so the rule +p-p gives +p!
    # Note2! You MUST have assign +/- (plus/minus) in front attributes! If not the
    #        attribute will be ignored!
    #
    #  R         : [R]ead-only         (+p+i+n+u+g+s+b+m+md5+tiger+rmd160+sha1-a)
    #  L         : [L]og file          (+p+i+n+u+g-s-b-a-m-md5-tiger-rmd160-sha1)
    #  N         : ignore [N]othing    (+p+i+n+u+s+b+g+s+a+m+c+md5+tiger+rmd160+sha1)
    #  E         : ignore [E]verything (-p-i-n-u-s-b-g-s-a-m-c-md5-tiger-rmd160-sha1)
    #  > or Logs : growing logfile     (+p+u+g+i+n+S)
    #  Binlib    : binary files        (+p+i+n+u+g+s+b+m+c+md5+sha1)
    #  ConfFiles : config files        (+p+i+n+u+g+s+b+m+c+md5+sha1)
    #  Devices   : device files /dev   (+p+i+n+u+g+s+b+c)
    #  Databases : databases           (+p+n+u+g)
    #  StaticDir : static directories  (+p+i+n+u+g)
    #  ManPages  : manual pages        (+p+i+n+u+g+s+b+m+c+md5+sha1)
    
    # note: 
    rules     = {
        'R'         : '+p+i+n+u+g+s+b+m-a+md5+tiger+rmd160+sha1-a',
        'L'         : '+p+i+n+u+g-s-b-a-m-md5-tiger-rmd160-sha1',
        'N'         : '+p+i+n+u+s+g+s+b+a+m+c+md5+tiger+rmd160+sha1',
        'E'         : '-p-i-n-u-s-g-s-b-a-m-c-md5-tiger-rmd160-sha1',
        '>'         : '+p+u+g+i+n+S',
        'Logs'      : '+p+u+g+i+n+S',
        'Binlib'    : '+p+i+n+u+g+s+b+m+c+md5+sha1',
        'ConfFiles' : '+p+i+n+u+g+s+b+m+c+md5+sha1',
        'Devices'   : '+p+i+n+u+g+s+b+c',
        'Databases' : '+p+n+u+g',
        'StaticDir' : '+p+i+n+u+g',
        'ManPages'  : '+p+i+n+u+g+s+b+m+c+md5+sha1'
        }


    # '!' signifies the entry is to be pruned (inclusive) from
    # the list of files to be scanned.
    # !/root/.bash_history
    notfile   = re.compile(r"\s*!(\S+)")
    notfiles  = [] # files/directories which are pruned
    
    # The files/directories
    # =/boot$ Binlib
    # /bin binlib
    file      = re.compile(r"\s*(\S+)\s+(\S+)")
    files     = {}

    linenumber = 0
    
    # for each line in config file
    if verbose: print "Reading config file, line by line"
    for line in ifile:
        linenumber += 1

        # match here, so we can extract var later
        commentmatch   = re.search(comment, line)
        blankmatch     = re.search(blanks, line)
        dbfilematch    = re.search(dbfile, line)
        dbfilenewmatch = re.search(dbfilenew, line)
        dbzipmatch     = re.search(dbzip, line)
        dbwarnsymmatch = re.search(dbwarnsym, line)
        summarymatch   = re.search(summary, line)
        envvarmatch    = re.search(envvar, line)
        uenvvarmatch   = re.search(uenvvar, line) 
        rulesmatch     = re.search(rule, line)
        notfilematch   = re.search(notfile, line)
        filesmatch     = re.search(file, line)

        # skip all comments and blank lines
        if commentmatch:
            continue
        if blankmatch:
            continue
        # where should the db be read from?
        elif dbfilematch:
            database = dbfilematch.group(1)
            confvar['database'] = database
        # where should the new db be saved?
        elif dbfilenewmatch:
            databaseout = dbfilenewmatch.group(1)
            confvar['database_out'] = databaseout
        # should db be zipped?
        elif dbzipmatch:
            dbgzip = dbzipmatch.group(1)
            if dbgzip == 'no':
                confvar['gzip_dbout'] = 'no'
        # warn on dead symlinks?
        elif dbwarnsymmatch:
            if dbwarnsymmatch.group(1) == 'yes':
                confvar['warn_dead_symlinks'] = 'yes'
            
        # length of summary: valid are 'short', 'normal' and 'detail'
        elif summarymatch:
            summaryout = summarymatch.group(1)
            if summaryout == 'short' or summaryout == 'normal' or summaryout == 'detail':
                confvar['summary'] = summaryout
            else:
                print "WARNING: unrecognized summary value '%s' on line: %s" % (summaryout, linenumber)
        # any evniroment variables? (for cron)
        elif envvarmatch:
            #print "envvarmatch"
            # typcial format: MAILTO, someone@localhost
            os.putenv(envvarmatch.group(1), envvarmatch.group(2))
        # undef any enviromentvariables
        elif uenvvarmatch:
            os.unsetenv(uenvvarmatch.group(1))
        # own defined rules
        elif rulesmatch:
            #print "rulematch"
            rules[rulesmatch.group(1)] = rulesmatch.group(2)
        # files to exclude - remove these files from files{} when loop complete
        elif notfilematch:
            #print "notfilematch"
            #print "NOTFILE: " + str(notfilematch.group(1))
            
            # it the line ends with '$', remove it.
            # used to express the end of a path
            #  /tem$  == mening /tem and NOT /temm or /temp or /te ...
            # but the glob function in python does that automatic, and the
            # glob function don't like '$', so we remove it
            if notfilematch.group(1)[-1:] == "$":
                for i in glob.glob(notfilematch.group(1)[:-1]):
                    notfiles.append(i)              
            else:
                for i in glob.glob(notfilematch.group(1)):
                    notfiles.append(i)
            #print "notfiles: " + str(notfiles)

        # get files/directories
        elif filesmatch:
            
            # se comment for notfilematch - the same thing goes here
            if filesmatch.group(1)[-1:] == "$":
                file2 = filesmatch.group(1)[:-1] # do not include '$' at end
                #print file2
            else:
                file2 = filesmatch.group(1)      # has no '$' at end
                #print file2
                
            # for hver fil, sjekk om group2 = en rulesmatch
            # så legg til
            todo  = filesmatch.group(2)
            #print "file: " + file2
            #print "todo: " + todo
            #print "rules: " + str(rules)

            # if using a template (R/L/N/E/>), translate to the
            # corresponding "rules"
            if rules.has_key(todo):
                todo = rules[todo]
            # NB! Rules may also be used as
            #   BinLib-md5-sha1
            # Where 'BinLib' is a rule and we don't want md5 and sha1
            # The above test will fail, and we need to split the 'todo'
            # with '+' and/or '-' as delimiter
            else:
                # example: 'BinLib-p-a-c+md5 -s'
                # first we must get 'BinLib' - fetch that using regexp
                r = re.search(r"^(\w+)(.*$)" ,todo)  # matches (text+numbers)(the rest)
                todoo = ""                           # to hold the translated rule
                if r:                                # if match
                    if rules.has_key(r.group(1)):    # is it a know rule?
                        todoo = rules[r.group(1)]    # translate rule for later user
                    else:                            # unknow rule!
                        print "WARNING: Unknown rule on line %d! Ignoring" % linenumber
                        continue
                        
                    # ok we now have translated the rule, add the rest if any
                    #print "GROUP: ",r.group(2)
                    if r.group(2):                # more than just a rule?
                        rulessplit = string.split(str(r.group(2))) # first we split on blanks
                        for g in rulessplit:      # add the rest
                            todoo += g
                        # NB! The rule may now contain both -p and +p
                        # but when doing stats, the +p has presedence
                    # add rule:
                    todo = todoo
                        
            # '=' signifies the entry is to be added, but if it's
            # a directory, then all its contents are pruned (useful for /tmp)
            # No problem with glob.
            if verbose: print "Building pathlist: %s" % file2
            if file2[0] == '=':
                for f in glob.glob(file2[1:]):
                    files[f] = todo  # do not include '='
                    #print "FILES DIR: ", files

            # ok, add the file/directory
            else:
                for f in glob.glob(file2):
                    if os.path.isfile(f):   # if file - just add
                        files[os.path.join(f)] = todo
                    elif os.path.isdir(f) or os.path.islink(f):   # if dir - do a walk
                        for root, dirs, file3 in os.walk(f):
                            for i in file3: # for all files in dir
                                files[os.path.join(root, i)] = todo
                            if root: # add directory as well
                                files[root] = todo
        else:
            print "WARNING: unrecognized line: %s" % line

    # exclude the files from notfiles
    if verbose: print "Excluding files, if any.."
    for i in notfiles:
        if files.has_key(i):
            del files[i]
            
    #import pprint
    #print "###########"
    #pprint.pprint(files)
        
    #print "filelist: " + str(files)
    #print "rules   : " + str(rules)
    #print "END"
    # export all

    # Ok, we have dictionary of files in 'files' and a list of
    # variables in 'confvar'
    return files, confvar

########################## saveDB
def saveDB(sysDB, confvar):
    """Save the database to file, given in 'database_out'. Compress
    the database if compress is true"""

    # where should the database be saved?
    # there is always a (default) value here
    dboutfilename = confvar['database_out']

    # should we compress the database? (default = yes)
    if confvar.has_key('gzip_dbout'):
        if confvar['gzip_dbout'] == 'yes':       # We should gzip the database
            try:                                 # open the dbout file
                dbout = gzip.GzipFile(dboutfilename, 'w')
            except:
                usage("Unable to write to databasefile file: %s" % dboutfilename)
                sys.exit(1)
        else:
            # open the dbout file
            try:
                dbout = open(dboutfilename, 'w')
            except:
                usage("Unable to write to databasefile file: %s" % dboutfilename)
                sys.exit(1)

    # write to file
    dbout.write("# This file was generated by %s, version %s\n" % (__program__, __version__))
    dbout.write("# Time of generation: %s\n" % time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
    dbout.write("# @@db_spec name perm inode size blocks lcount uid gid size atime mtime ctime md5 sha1\n")

    # write all the stats to file:
    for file in sysDB:                    # for each file in dictionary
        filestats = file                  # contruct a string
        for stat in sysDB[file]:          # extract all stats..
            filestats += ' ' + str(stat)  # ..and append to string
        dbout.write(filestats+'\n')       # write to file

    # close the file
    dbout.close()

    print "Database saved in %s" % dboutfilename

########################## readSysDB
def readSysDB(confvar):
    """Read a pide database from file and put into a dictionary:
    {file : [stat1, stat2, stat3....], file2......}
    return the dictionary
    """

    dbinfilename = confvar['database']

    # if gzip_dbout == yes, we assume the db file is compressed
    if confvar['gzip_dbout'] == 'yes':  # open using gzip
        try:
            dbin = gzip.GzipFile(dbinfilename, 'r')
        except:
            usage("Unable to read database file: %s" % dbinfilename)
            sys.exit(1)
    else:
        try:
            dbin = open(dbinfilename, 'r')
        except:
            usage("Unable to read database file: %s" % dbinfilename)
            sys.exit(1)

    # This is where we put our database
    fileDB = {}
    linenumber = 0

    # grep '#' lines
    comment   = re.compile(r"\s*\#.*")
    # blank lines
    blanks    = re.compile(r"^$")

    # read file line by line
    if verbose: print "Reading database from disk, line by line"
    
    while 1:
        linenumber += 1  # in case of an error, print the line number
        line = dbin.readline()
        if not line: break

        # process line
        if re.search(comment, line):  # skip comment lines
            continue
        elif re.search(blanks, line): # skip blank lines
            continue

        # split the line
        linesplit = string.split(line)

        # read arguments into a dictionary
        if len(linesplit) != 13:           # each line has exactly 13 arguments!
            usage("Error occured reading database '%s' on line %d\nThe offending line was:\n%s\nCorrupt database?" % (dbinfilename, linenumber, line))
            sys.exit(1)
        else:
            fileDB[linesplit[0]] = linesplit[1:]
            
    #import pprint
    #pprint.pprint(fileDB)

    return fileDB

########################## compareDB
def compareDB(called, sysDB, fileDB, confvar, syspaths):
    """Should compare two databases: One (old) from disk, and the newly
    generated. The databases are two dictionaries.
    * sysDB = new generated database
    * fileDB = (old) database from disk
    """

    missing = []    # files that are in old db, but not in new
    changed = []    # files that have changed since last check
    added   = []    # new files not in old db

    #print "Compare"
    #import pprint
    #pprint.pprint(sysDB)
    
    for key in fileDB:
        try:                        # try in case there is no exceptions --> catch keyerrors
            if not sysDB[key]:      # check if we have the file in the new one
                missing.append(key) # add missing file to list
        except:                     # keyerror, just..
            continue                # ..continue with next file
        
        if sysDB[key]:              # file exists, check stats
            i = 0                   # to iterate stats
            if verbose: print "Compare: %s" % key
            # for each stat in old db
            for stat in fileDB[key]:
                # compare each stat in old DB with the corresponding stat in new DB (sysDB)
                if str(stat) != str(sysDB[key][i]): # do we have a difference?
                    # must do a exception on '+S'
                    if i == 5 and '+S' in syspaths[key]:
                        if int(fileDB[key][i]) > int(sysDB[key][i]):
                            if verbose: print "   Difference found!"
                            # add the file, it it's not added already
                            if not key in changed:
                                if verbose: print "   File added!"
                                changed.append(key) # add changed file to list
                            
                    else:
                        if verbose: print "   Difference found!"
                        # add the file, it it's not added already
                        if not key in changed:
                            if verbose: print "   File added!"
                            changed.append(key) # add changed file to list
                i += 1

    # for each file NOT old db is considered 'new' files
    for key in sysDB:
        if not fileDB.has_key(key):
            added.append(key)

    #print "REMOVED: ", missing
    #print "CHANGED: ", changed
    #print "ADDED:   ", added

    # if init and no changes - just return
    if called == "check" and not missing and not changed and not added:
        return
    else:
        # print summary - short/normal/detail get this summary
        print "\n%s found differences between database and filesystem!!" % __program__
        print "\nTimestamp: %s" % time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
        print "\nSummary:"
        print "Total number of files in database: %s" % len(fileDB)
        print "Total number of files on system  : %s" % len(sysDB)
        print "Removed files                    : %s" % len(missing)
        print "New files                        : %s" % len(added)
        print "Changed files                    : %s" % len(changed)

        # normal/detail summary level
        if confvar['summary'] == 'normal' or confvar['summary'] == 'detail':
            # viewing the files that are missing/new/changed
            if called == "update":             # When called as 'update'..
                if len(missing) != 0:
                    print "\nRemoved files:"   # ...some syntax diff
                    for file in missing:
                        print "  " + file
                if len(added) != 0:
                    print "\nAdded files:"
                    for file in added:
                        print "  " + file

            if called == "check":              # When called as 'check'..
                if len(missing) != 0:
                    print "\nMissing files:"   # .. some syntax diff
                    for file in missing:
                        print "  " + file
                if len(added) != 0:
                    print "\nNew files:"
                    for file in added:
                        print "  " + file

            # changed files
            if len(changed) != 0:
                print "\nChanged files:"
                for file in changed:
                    print "  " + file

        # detail summary level
        if confvar['summary'] == 'detail':
            print "\nDetailed information about changes:"
            
            for file in changed:              # for each changed file
                if os.path.isdir(file):
                    print "Directory:", file
                else:
                    print "File:", file

                i = 0
                for stat in fileDB[file]:     # iterate stats
                    if str(stat) != str(sysDB[file][i]):
                        # perm, inode, lcount, uid, gid, size, atime, mtime, ctime, md5, sha1
                        if i == 0:
                            print "  Perm  : %-40s , %-40s" % (str(stat), str(sysDB[file][i]))
                        elif i == 1:
                            print "  Inode : %-40s , %-40s" % (str(stat), str(sysDB[file][i]))
                        elif i == 2:
                            print "  Lcount: %-40s , %-40s" % (str(stat), str(sysDB[file][i]))
                        elif i == 3:
                            print "  Uid   : %-40s , %-40s" % (str(stat), str(sysDB[file][i]))
                        elif i == 4:
                            print "  Gid   : %-40s , %-40s" % (str(stat), str(sysDB[file][i]))

                        # must do some exceptions on +S  
                        if i == 5 and '+S' in syspaths[file] and int(fileDB[file][5]) > int(sysDB[file][5]):
                            print "  Size  : %-40s , %-40s" % (str(stat), str(sysDB[file][i]))
                        elif i == 5:
                            print "  Size  : %-40s , %-40s" % (str(stat), str(sysDB[file][i]))

                        # back to "normal" check
                        if i == 6:
                            print "  Blocks: %-40s , %-40s" % (str(stat), str(sysDB[file][i]))
                        elif i == 7:
                            print "  Atime : %-40s , %-40s" % (str(time.ctime(int(stat))), str(time.ctime(int(sysDB[file][i]))))
                        elif i == 8:
                            print "  Mtime : %-40s , %-40s" % (str(time.ctime(int(stat))), str(time.ctime(int(sysDB[file][i]))))
                        elif i == 9:
                            print "  Ctime : %-40s , %-40s" % (str(time.ctime(int(stat))), str(time.ctime(int(sysDB[file][i]))))
                        elif i == 10:
                            print "  MD5   : %-40s , %-40s" % (str(stat), str(sysDB[file][i]))
                        elif i == 11:
                            print "  SHA-1 : %-40s , %-40s" % (str(stat), str(sysDB[file][i])) 

                    i += 1

                print "" # some space between each file
    

########################## integrityCheck
def integrityCheck(init=0, check=0, update=0, rcfile="", verbose=0):
    """Starting point - call this if using as a module.
    * call 'buildPaths' which returns a list of files (with attributes)
      and a list of config variables
    * then call 'makeSysDB' to build a database of all files in 'files'
    * choice:
       - init:   save db and quit
       - check:  compare db on disk and the db generated by 'makeSysDB'
                 print changes
       - update: compare db on disk and the db generated by 'makeSysDB'
                 print updates - save new db on disk
    """

    #print "init:", init
    #print "check:", check
    #print "update:", update

    # read the config file, returns a list of files in syspaths
    # and a list of config variables in 'confvar'
    if rcfile:
        if verbose: print "Parsing config file and building paths"
        syspaths, confvar = buildPaths(rcfile)
    else:
        usage("No config file defined")
        sys.exit(1)

    # Do some sanity checks before going into some heavy processing
    if init: # can we open db out for writing? If not there is no need to process files..
        try:
            dbout =  open(str(confvar['database_out']), 'w')
            dbout.close()
        except:
            usage("Unable to write to databasefile file: %s" % confvar['database_out'])
            sys.exit(1)

    if check or update: # can we open db for reading? If not we can't compare..
        try:
            dbout = open(str(confvar['database']), 'r')
            dbout.close()
        except:
            usage("Unable to read to databasefile file: %s" % confvar['database'])
            sys.exit(1)
                       
    # build database sysDB = database of current system
    # this can be quite large (several MB)
    if verbose: print "Building database of current system"       
    sysDB = makeSysDB(syspaths, confvar)

    # init = save database as defined in 'database_out', gzip if specified
    if init:
        if verbose: print "Doing 'init' --> saving database"
        # save database to file
        saveDB(sysDB, confvar)
    
    # update = print the different between the new database (sysDB) and
    # the old one. Then save the new database in 'database'
    elif update:
        # read database from file
        if verbose: print "Reading database from file"
        fileDB = readSysDB(confvar) 
        # compare the two databases
        if verbose: print "Compare database of system with (old) database on disk"
        compareDB("update", sysDB, fileDB, confvar, syspaths)
        # save the new database sysDB
        if verbose: print "Save database to file"
        saveDB(sysDB, confvar)
        
    # check = compare the new database 'sysDB' with the old one,
    # print the differenses
    elif check:
        # read database from file
        if verbose: print "Reading database from file"
        fileDB = readSysDB(confvar) 
        # compare the two databases
        if verbose: print "Compare database of system with (old) database on disk"
        compareDB("check", sysDB, fileDB, confvar, syspaths)

    return 0
    # end

########################## printconf
def printconf():
    """Print an example config file and exit"""

    print """#
# pide.conf based on Tripwire's tw.config
#
# NOTE! the tiger and rmd160 checksum is NOT implemented! So it
# it will be ignored (but md5 and sha1 should do the job).
#
# This file contains a list of files and directories that this
# script will scan. Information collected from these files will be 
# stored in a database file.
#
# Format: [!|=] entry [attributes-flags]
#
# where:  '!' signifies the entry is to be pruned (inclusive) from
#             the list of files to be scanned.
#         '=' signifies the entry is to be added, but if it is
#             a directory, then all its contents are pruned
#             (useful for /tmp).
#
# where: 'entry' is the absolute pathname of a file or a directory
#
# where 'attributes-flags' are in the format:
#        [template][ [+|-][pinugsam...] ... ]
#
#       - :  ignore the following atributes
#       + :  do not ignore the following attributes
#
#       p :  permission and file mode bits      a: access timestamp
#       i :  inode number                       m: modification timestamp
#       n :  number of links                    c: inode creation timestamp
#       u :  user id of owner                 md5: MD5 signature
#       g :  group id of owner              tiger: tiger signature*
#       s :  size of file                  rmd160: RMD160 signature*
#       b :  number of blocks (Linux)        sha1: SHA1 signature
#       S :  check for growing size
#
#       *) not implemented, - ignored
#
# Ex:   The following entry will scan all the files in /etc, and report
#       any changes in mode bits, inode number, reference count, uid,
#       gid, modification and creation timestamp, and the signatures.
#       However, it will ignore any changes in the access timestamp.
#
#       /etc    +p+i+n+u+g+s+m+md5+tiger+rmd160+sha1-a
#
# Note! '+' (plus) has presedence over '-' (minus), so the rule +p-p gives +p!
# Note2! You MUST have assign +/- (plus/minus) for attributes! If not, the
#        attribute will be ignored!
#
# The following templates have been pre-defined to make these long ignore
# mask descriptions unecessary.
#
# Templates:
#  R         : [R]ead-only         (+p+i+n+u+g+s+b+m+md5+tiger+rmd160+sha1-a)
#  L         : [L]og file          (+p+i+n+u+g-s-b-a-m-md5-tiger-rmd160-sha1)
#  N         : ignore [N]othing    (+p+i+n+u+s+b+g+s+a+m+c+md5+tiger+rmd160+sha1)
#  E         : ignore [E]verything (-p-i-n-u-s-b-g-s-a-m-c-md5-tiger-rmd160-sha1)
#  > or Logs : growing logfile     (+p+u+g+i+n+S)
#  Binlib    : binary files        (+p+i+n+u+g+s+b+m+c+md5+sha1)
#  ConfFiles : config files        (+p+i+n+u+g+s+b+m+c+md5+sha1)
#  Devices   : device files /dev   (+p+i+n+u+g+s+b+c)
#  Databases : databases           (+p+n+u+g)
#  StaticDir : static directories  (+p+i+n+u+g)
#  ManPages  : manual pages        (+p+i+n+u+g+s+b+m+c+md5+sha1)
#
# You can use templates with modifiers, like:
#       Ex:  /etc/lp    E+u+g
#
#       Example configuration file:
#               /etc            R       # all system files
#               !/etc/lp        R       # ...but not those logs
#               =/tmp           N       # just the directory, not its files
#
# Note the difference between pruning (via '!') and ignoring everything
# (via 'E' template):  Ignoring everything in a directory still monitors
# for added and deleted files.  Pruning a directory will prevent Pide
# from even looking in the specified directory.
#
# Running slowly?  Modify the entries to ignore one of the signatures (md5
# or sha1) when this computationally-exorbitant protection is a paranoia
# setting only :^)
#

# Where is our database file?
database=file:/var/db/pide.db

# New databases (--init)
database_out=file:/var/db/pide.db.new

# Change this to 'no', or remove it to not gzip output
# (only useful on systems with few CPU cycles to spare)
gzip_dbout=yes

# Lengt of summary when doing --check or --update
#   short  = one line telling whats changed
#   normal = same as above and a list of changed files
#   detail = same as above and a detailed list of change
summary=normal

# Whether to warn about dead symlinks or not (default).
warn_dead_symlinks=no

# Custom rules may go here
# NB!! '-' (minus) has presedence over '+' (plus), so the rule +p-p gives -p!

# You may specify enviroment variables to be exported when running here.
# It's normally only usful when used by the cron script.
# Define variable VAR to value val
# @@define VAR val
@@define MAILTO root@localhost
@@define LINES 1000

# You may undefine enviroment variables with
# @@undef VAR

# Next decide what directories/files you want in the database
#  - You may do globbing here; /bin/file*
#  - You may also use '$' to define end of file/dir (ex.: '/tmp$'), but
#    is not necessary, since python's glob does the job fine without -
#    so it's stripped. It's supported for compatibility with
#    aide/tripwire only.

# Homes
=/                 L      # First, root's traditional home
/root              R      # Most likely root's  home
!/root/.bash_history
=/home             L      # Holding the users homedir

# Log files
=/var/log          StaticDir
/var/log           Logs

# Kernel, system map etc. - files that are used by the boot loader.
/boot              Binlib

# System configuration files
/etc               R
/usr/local/etc     R

# Binaries
/bin               Binlib
/sbin              Binlib
/usr/bin           Binlib
/usr/sbin          Binlib
/usr/local/bin     Binlib
/usr/local/sbin    Binlib
/usr/games         Binlib

# Libraries
/lib               Binlib
/usr/lib           Binlib
/usr/local/lib     Binlib

# Databases
/var/db            Databases

# Test only the directory when dealing with /proc and /tmp
=/proc             StaticDir
=/tmp              StaticDir

# You can look through these examples to get further ideas

# manpages can be trojaned, especially depending on *roff implementation
#/usr/man          ManPages
#/usr/share/man    ManPages
#/usr/local/man    ManPages

# docs
#/usr/doc          ManPages
#/usr/share/doc    ManPages

# check users' home directories
#/home             Binlib

# Devices - be careful to exclude terminals, sound devices, ++
#/dev              Devices

# check sources for modifications
#/usr/src          L
#/usr/local/src    L

# Check headers for same
#/usr/include       L
#/usr/local/include L

"""

########################## usage
def usage(error):
    """Print usage of program"""
    if error:
        print "%s: %s" % (os.path.basename(sys.argv[0]), str(error))
        print "Try `%s --help' for more information." % os.path.basename(sys.argv[0])
    else:
        print """usage: %s [OPTIONS]
%s (Python Intrusion Detection Enviroment) is an intrusion detection
system for checking the integrity of files. Basically a python implemenation
of Tripwire/AIDE.

Mandatory arguments to long options are mandatory for short options too.
  -i, --init         Initialize the database.
  -C, --check        Checks the database for inconsistencies. This is
                     the default option.
  -u, --update       Checks the database and updates the database
                     non-interactively.
  -c, --config=FILE  Read config options from FILE
  -p, --printconf    View an example config file. Do a '%s -p > pide.conf'
                     to pipe this to a config file.
  -v, --verbose      Level of debug messages.
  -h, --help         Display this help and exit.

Report bugs to lars [at] gnist org""" % (os.path.basename(sys.argv[0]), os.path.basename(sys.argv[0]), os.path.basename(sys.argv[0]))

########################## main
if __name__ == '__main__':
    """Main loop"""

    # version control
    version = string.split(string.split(sys.version)[0], ".")
    if map(int, version) < [2, 3]:
        usage("You need Python ver 2.3 or higher to run!")
        sys.exit(1)

    try:
        # opts = arguments recognized,
        # args = arguments NOT recognized (leftovers)
        opts, args = getopt.getopt(sys.argv[1:], "iCuhvc:p", ["init", "check", "update", "help", "verbose", "config=", "printconf"])
    except getopt.GetoptError:
        # print help information and exit:
        usage("illegal option(s) -- " + str(sys.argv[1:]))
        sys.exit(1)

    # try this as default pide.conf file, if none given
    rcfile = '/etc/pide.conf'

    # default verbose level
    verbose = 0
    
    # run through arguments and set variables
    
    # FIXFIX! - What if config file is specified AFTER the --init,
    # must get config file BEFORE init, check and update!
    for o, a in opts:
        if o == "-c" or o == "--config": # read config from this file
            try:   # check for readability later
                rcfile = str(a)
            except:
                usage("invalid config file")
                sys.exit(1)
        if o == "-v" or o == "--verbose": # verbose level
            verbose = 1
            
    #print "config file:", rcfile

    for o, a in opts:
        if o == "-h" or o == "--help":   # display help and exit
            usage("")
            sys.exit(0)
        if o == "-p" or o == "--printconf": # display example config file
            printconf()
            sys.exit(0)
        if o == "-i" or o == "--init":   # initialize the database
            integrityCheck(init=1, rcfile=rcfile, verbose=verbose)
            sys.exit(0)
        if o == "-C" or o == "--check":  # check for inconsistecies
            integrityCheck(check=1, rcfile=rcfile, verbose=verbose)
            sys.exit(0)
        if o == "-u" or o == "--update": # update the database
            integrityCheck(update=1, rcfile=rcfile, verbose=verbose)
            sys.exit(0)

    # if there is no options, do default (--check)
    if not opts:
        integrityCheck(check=1)
        sys.exit(0)
# end
