#! /usr/bin/python --

"""
usage: %(progname)s [domain...]

Version: %(version)s

Contacts the apropriate whois database for each domain and displays
the result.

class WhoisRecord:
    self.domain             -- Domain Name
    self.whoisserver        -- Whoisserver associated with domain
    self.page               -- raw whois record data

    public methods:

        def WhoisRecord(domain=None)
            Whois object constructor

        def whois(domainname=None, server=None, cache=0)
            Fetches whoisrecord and places result in self.page
            Raises NoSuchDomain if the domain doesn't exist.


class DomainRecord(WhoisRecord):
    self.domainid           -- domainid for this domain
    self.created            -- date in which the domain was created
    self.lastupdated        -- date in which the domain was last updated.
    self.expires            -- date in which the domain expires
    self.databaseupdated    -- date in which the database was last updated.
    self.servers            -- list of (hostname, ip) pairs of the nameservers. 
    self.registrant         -- ContactRecord of domain owner. 
    self.contacts           -- dictionary of contacts (ContactRecord objects)

    public methods:

    def DomainRecord(domain=None)
        Constructor for DomainRecord

    def Parse()
        Creates a parsed version of the information contained in 
        the whois record for domain from self.page
        raises NoParser if a parser does not exist for a registry.



class Contact:
    self.type               -- Type of contact
    self.organization       -- Organization associated with contact.
    self.person             -- Person associated with contact.
    self.handle             -- NIC Handle
    self.address            -- Street address of contact
    self.address2           --
    self.address3           --
    self.city               -- city of addr
    self.state              -- address state
    self.zip                -- zipcode
    self.country            -- country
    self.email              -- Email address of contact
    self.phone              -- Phone Number
    self.fax                -- Fax Number
    self.lastupdated        -- Last update of contact record
"""

_version = "1.5"

import os, sys, string, time, getopt, socket, select, re, errno, copy, signal

timeout=5

try:
    signal.SIGALRM
    HAS_ALARM = 1
except:
    HAS_ALARM = 0


class WhoisRecord:      

    defaultserver='whois.verisign-grs.net'#'whois.networksolutions.com'
    whoismap={ 'com' : 'whois.internic.net' , \
               'org' : 'whois.pir.org' , \
               'net' : 'whois.internic.net' , \
               'edu' : 'whois.networksolutions.com' , \
               'biz' : 'whois.biz' , \
               'info': 'whois.afilias.info' , \
               'us'  : 'whois.nic.us', \
               'de'  : 'whois.denic.de' , \
               'gov' : 'whois.nic.gov' , \
               'name': 'whois.nic.name' , \
#???	       'pro': 'whois.nic.name' , \
               'museum': 'whois.museum' , \
               'int':  'whois.iana.org' , \
               'aero': 'whois.information.aero' , \
               'coop': 'whois.nic.coop' , \
               # See http://www.nic.gov/cgi-bin/whois 
               'mil' : 'whois.nic.mil' , \
               # See http://www.nic.mil/cgi-bin/whois
               'ca'  : 'whois.cdnnet.ca' , \
               'uk'  : 'whois.nic.uk' , \
               'au'  : 'whois.aunic.net' , \
               'hu'  : 'whois.nic.hu' , \

               # All the following are unverified/checked. 
               'be'  : 'whois.ripe.net',
               'it'  : 'whois.ripe.net' , \
               # also whois.nic.it
               'at'  : 'whois.ripe.net' , \
               # also www.nic.at, whois.aco.net
               'dk'  : 'whois.ripe.net' , \
               'fo'  : 'whois.ripe.net' , \
               'lt'  : 'whois.ripe.net' , \
               'no'  : 'whois.ripe.net' , \
               'sj'  : 'whois.ripe.net' , \
               'sk'  : 'whois.ripe.net' , \
               'tr'  : 'whois.ripe.net' , \
               # also whois.metu.edu.tr
               'il'  : 'whois.ripe.net' , \
               'bv'  : 'whois.ripe.net' , \
               'se'  : 'whois.nic-se.se' , \
               'br'  : 'whois.nic.br' , \
               # a.k.a. whois.fapesp.br?
               'fr'  : 'whois.nic.fr' , \
               'sg'  : 'whois.nic.net.sg' , \
               'hm'  : 'whois.registry.hm' , \
               # see also whois.nic.hm
               'nz'  : 'domainz.waikato.ac.nz' , \
               'nl'  : 'whois.domain-registry.nl' , \
               # RIPE also handles other countries
               # See  http://www.ripe.net/info/ncc/rir-areas.html
               'ru'  : 'whois.ripn.net' , \
               'ch'  : 'whois.nic.ch' , \
               # see http://www.nic.ch/whois_readme.html
               'jp'  : 'whois.nic.ad.jp' , \
               # (use DOM foo.jp/e for english; need to lookup !handles separately)
               'to'  : 'whois.tonic.to' , \
               'nu'  : 'whois.nic.nu' , \
               'fm'  : 'www.dot.fm' , \
               # http request http://www.dot.fm/search.html
               'am'  : 'whois.nic.am' , \
               'nu'  : 'www.nunames.nu' , \
               # http request
               # e.g. http://www.nunames.nu/cgi-bin/drill.cfm?domainname=nunames.nu
               #'cx'  : 'whois.nic.cx' , \	# no response from this server
               'af'  : 'whois.nic.af' , \
               'as'  : 'whois.nic.as' , \
               'li'  : 'whois.nic.li' , \
               'lk'  : 'whois.nic.lk' , \
               'mx'  : 'whois.nic.mx' , \
               'pw'  : 'whois.nic.pw' , \
               'sh'  : 'whois.nic.sh' , \
               # consistently resets connection
               'tj'  : 'whois.nic.tj' , \
               'tm'  : 'whois.nic.tm' , \
               'pt'  : 'whois.dns.pt' , \
               'kr'  : 'whois.nic.or.kr' , \
               # see also whois.krnic.net
               'kz'  : 'whois.nic.or.kr' , \
               # see also whois.krnic.net
               'al'  : 'whois.ripe.net' , \
               'az'  : 'whois.ripe.net' , \
               'ba'  : 'whois.ripe.net' , \
               'bg'  : 'whois.ripe.net' , \
               'by'  : 'whois.ripe.net' , \
               'cy'  : 'whois.ripe.net' , \
               'cz'  : 'whois.ripe.net' , \
               'dz'  : 'whois.ripe.net' , \
               'ee'  : 'whois.ripe.net' , \
               'eg'  : 'whois.ripe.net' , \
               'es'  : 'whois.ripe.net' , \
               'fi'  : 'whois.ripe.net' , \
               'gr'  : 'whois.ripe.net' , \
               'hr'  : 'whois.ripe.net' , \
               'lu'  : 'whois.ripe.net' , \
               'lv'  : 'whois.ripe.net' , \
               'ma'  : 'whois.ripe.net' , \
               'md'  : 'whois.ripe.net' , \
               'mk'  : 'whois.ripe.net' , \
               'mt'  : 'whois.ripe.net' , \
               'pl'  : 'whois.ripe.net' , \
               'ro'  : 'whois.ripe.net' , \
               'si'  : 'whois.ripe.net' , \
               'sm'  : 'whois.ripe.net' , \
               'su'  : 'whois.ripe.net' , \
               'tn'  : 'whois.ripe.net' , \
               'ua'  : 'whois.ripe.net' , \
               'va'  : 'whois.ripe.net' , \
               'yu'  : 'whois.ripe.net' , \
               # unchecked
               'ac'  : 'whois.nic.ac' , \
               'cc'  : 'whois.nic.cc' , \
               #'cn'  : 'whois.cnnic.cn' , \	# connection refused
               'gs'  : 'whois.adamsnames.tc' , \
               'hk'  : 'whois.apnic.net' , \
               #'ie'  : 'whois.ucd.ie' , \	# connection refused
               #'is'  : 'whois.isnet.is' , \# connection refused
               #'mm'  : 'whois.nic.mm' , \	# connection refused
               'ms'  : 'whois.adamsnames.tc' , \
               'my'  : 'whois.mynic.net' , \
               #'pe'  : 'whois.rcp.net.pe' , \	# connection refused
               'st'  : 'whois.nic.st' , \
               'tc'  : 'whois.adamsnames.tc' , \
               'tf'  : 'whois.adamsnames.tc' , \
               'th'  : 'whois.thnic.net' , \
               'tw'  : 'whois.twnic.net' , \
#	       'us'  : 'whois.isi.edu' , \
               'vg'  : 'whois.adamsnames.tc' , \
               #'za'  : 'whois.co.za'	# connection refused
               }



    def __init__(self,domain=None):
        self.domain=domain
        self.whoisserver=None	
        self.page=None

    def whois(self,domain=None, server=None, cache=0):
        if domain is not None:
            self.domain=domain

        if server is not None:
            self.whoisserver=server

        if self.domain is None:
            print "No Domain"
            raise "No Domain"

        if self.whoisserver is None:
            self.chooseserver()

        if self.whoisserver is None:
            print "No Server"
            raise "No Server"

        if cache:
            fn = "%s.dom" % domainname
            if os.path.exists(fn):
                return open(fn).read()

        self.page=self._whois()	

        if cache:
            open(fn, "w").write(page)


    def chooseserver(self):
        try:
            toplevel = string.split(self.domain, ".")[-1]

            self.whoisserver=WhoisRecord.whoismap.get(toplevel)
            #print toplevel, "---", self.whoisserver
            if self.whoisserver==None:
                self.whoisserver=WhoisRecord.defaultserver
                return
        except:
            self.whoisserver=WhoisRecord.defaultserver
            return

        if toplevel in ('com', 'org', 'net'):
            tmp=self._whois()
            m = re.search("Whois Server:(.+)", tmp)

            if m:
                self.whoisserver=string.strip(m.group(1))
                #print "server 2:", self.whoisserver
                return
            self.whoisserver='whois.networksolutions.com'
            tmp=self._whois()
            m=re.search("Whois Server:(.+)",tmp)
            if m:
                self.whoisserver=string.strip(m.group(1))
                #print "server 1:", self.whoisserver

                return
        #print "server 3:", self.whoisserver



    def _whois(self):
        def alrmhandler(signum,frame):
            raise "TimedOut", "on connect"

        s = None

        ## try until we timeout
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if HAS_ALARM:
            s.setblocking(0)
            signal.signal(signal.SIGALRM,alrmhandler)
            signal.alarm(timeout)
        while 1:	
            try:
                s.connect((self.whoisserver, 43))
            except socket.error, (ecode, reason):
                if ecode==errno.EINPROGRESS: 
                    continue
                elif ecode==errno.EALREADY:
                    continue
                else:
                    raise socket.error, (ecode, reason)
                pass

            break
        if HAS_ALARM: signal.alarm(0)

        ret = select.select ([s], [s], [], 30)

        if len(ret[1])== 0 and len(ret[0]) == 0:
            s.close()
            raise TimedOut, "on data"

        s.setblocking(1)

        s.send("%s\n" % self.domain)
        page = ""
        while 1:
            data = s.recv(8196)
            if not data: break
            page = page + data
            pass

        s.close()

        if string.find(page, "No match for") != -1:
            raise 'NoSuchDomain', self.domain

        if string.find(page, "No entries found") != -1:
            raise 'NoSuchDomain', self.domain

        if string.find(page, "no domain specified") != -1:
            raise 'NoSuchDomain', self.domain

        if string.find(page, "NO MATCH:") != -1:
            raise 'NoSuchDomain', self.domain

        return page

##
## ----------------------------------------------------------------------
##
class ContactRecord:
    def __init__(self):
        self.type=None
        self.organization=None
        self.person=None
        self.handle=None
        self.address=None
        self.address2=None
        self.address3=None
        self.city=None
        self.country=None
        self.state=None
        self.zip=None
        self.email=None
        self.phone=None
        self.fax=None
        self.lastupdated=None
        return
    def __str__(self):
        return "Type: %s\nOrganization: %s\nPerson: %s\nHandle: %s\nAddress: %s\nAddress2: %s\nAddress3: %s\nCity: %s\nState: %s\nZip: %s\nCountry: %s\nEmail: %s\nPhone: %s\nFax: %s\nLastupdate: %s\n" % (self.type,self.organization,self.person,self.handle,self.address, self.address2, self.address3, self.city, self.state, self.zip, self.country, self.email,self.phone,self.fax,self.lastupdated)


class DomainRecord(WhoisRecord):

    parsemap={ 'whois.networksolutions.com' : 'ParseWhois_NetworkSolutions' ,
               'whois.opensrs.net'          : 'ParseWhois_NetworkSolutions' , #needs to be customized!
               'whois.register.com'         : 'ParseWhois_RegisterCOM' ,
               'whois.alldomains.com'       : 'ParseWhois_AllDomainsCOM',
               'whois.iana.org'             : 'ParseWhois_INT', 
               'whois.nic.coop'             : 'ParseWhois_COOP',
               'whois.biz'                  : 'ParseWhois_BIZ' ,
               'whois.nic.us'               : 'ParseWhois_BIZ',
               'whois.information.aero'     : 'ParseWhois_INFO',
               'whois.nic.name'             : 'ParseWhois_INFO',
               'whois.pir.org'              : 'ParseWhois_INFO',
               'whois.museum'               : 'ParseWhois_INFO',
               'whois.afilias.info'         : 'ParseWhois_INFO' }

    def __init__(self,domain=None):
        WhoisRecord.__init__(self,domain)
        self.domainid = None
        self.created = None
        self.lastupdated = None
        self.expires = None
        self.databaseupdated = None
        self.servers = None
        self.registrant = ContactRecord()
        self.registrant.type='registrant'
        self.contacts = {}
        return

    def __str__(self):
        con=''
        for (k,v) in self.contacts.items():
            con=con + str(v) +'\n'
        return "%s (%s):\nWhoisServer: %s\nCreated : %s\nLastupdated : %s\nDatabaseupdated : %s\nExpires : %s\nServers : %s\nRegistrant >>\n\n%s\nContacts >>\n\n%s\n" % (self.domain, self.domainid,self.whoisserver,self.created, self.lastupdated, self.databaseupdated, self.expires,self.servers, self.registrant, con)

    def Parse(self):
        self._ParseWhois()
        return

    def _ParseWhois(self):
        m = re.search("Registrar Whois: (.*)", self.page)
        if m:
            self.whoisserver = m.group(1)
        
        parser=DomainRecord.parsemap.get(self.whoisserver)

        if parser==None:
            raise 'NoParser for', self.whoisserver

        #print "---> PARSER:", self.whoisserver, "-",  parser

        parser='self.'+parser+'()'
        eval(parser)
        return

    ##
    ## ----------------------------------------------------------------------
    ##
    def _ParseContacts_RegisterCOM(self,page):

        parts = re.split("((?:(?:Administrative|Billing|Technical|Zone) Contact,?[ ]*)+:)\n", page)

        contacttypes = None
        for part in parts:
            if string.find(part, "Contact:") != -1:
                if part[-1] == ":": part = part[:-1]
                contacttypes = string.split(part, ",")
                continue
            part = string.strip(part)
            if not part: continue

            contact=ContactRecord()

            m = re.search("Email: (.+@.+)", part)
            if m:
                contact.email=string.lower(string.strip(m.group(1)))

            m = re.search("\s+Fax\.\.: (.+)", part)
            if m:
                contact.fax=string.lower(string.strip(m.group(1)))                		
            m = re.search("\s+Phone: (.+)", part)
            if m:
                contact.phone=m.group(1)
                end=m.start(0)

            start=0

            lines = string.split(part[start:end], "\n")
            lines = map(string.strip,lines)

            contact.organization = lines.pop(0)
            contact.person = lines.pop(0)

            contact.address=string.join(lines,'\n')

            for contacttype in contacttypes:
                contacttype = string.lower(string.strip(contacttype))
                contacttype = string.replace(contacttype, " contact", "")
                contact.type=contacttype
                self.contacts[contacttype] = copy.copy(contact)


    def ParseWhois_NetworkSolutions(self):
        m = re.search("Record last updated on (.+)\.", self.page)
        if m: self.lastupdated = m.group(1)

        m = re.search("Record created on (.+)\.", self.page)
        if m: self.created = m.group(1)

        m = re.search("Database last updated on (.+)\.", self.page)
        if m: self.databaseupdated = m.group(1)

        m = re.search("Record expires on (.+)\.",self.page)
        if m: self.expires=m.group(1)

        m = re.search("Registrant:(.+?)\n\n", self.page, re.S)
        if m: 
            start= m.start(1)
            end = m.end(1)
            reg = string.strip(self.page[start:end])

            reg = string.split(reg, "\n")
            reg = map(string.strip,reg)
            self.registrant.organization = reg[0]
            self.registrant.address = string.join(reg[1:],'\n')

            m = re.search("(.+) \((.+)\)", self.registrant.organization)
            if m: 
                self.domainid   = m.group(2)

        m = re.search("Domain servers in listed order:\n\n", self.page)
        if m:
            i = m.end()
            m = re.search("\n\n", self.page[i:])
            j = m.start()
            servers = string.strip(self.page[i:i+j])
            lines = string.split(servers, "\n")
            self.servers = []
            for line in lines:
                m=re.search("([\w|\.]+?)\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",string.strip(line))
                if m:
                    self.servers.append((m.group(1), m.group(2)))

        m = re.search("((?:(?:Administrative|Billing|Technical|Zone) Contact,?[ ]*)+:)\n", self.page)
        if m:
            i = m.start()
            m = re.search("Record expires on", self.page)
            j = m.start()
            contacts = string.strip(self.page[i:j])

        self._ParseContacts_NetworkSolutions(contacts)


    def ParseWhois_RegisterCOM(self):
        m = re.search("Record last updated on.*: (.+)", self.page)
        if m: self.lastupdated = m.group(1)

        m = re.search("Created on.*: (.+)", self.page)
        if m: self.created = m.group(1)

        m = re.search("Expires on.*: (.+)", self.page)
        if m: self.expires = m.group(1)

        m = re.search("Phone: (.+)", self.page)
        if m: self.registrant.phone=m.group(1)

        m = re.search("Email: (.+@.+)",self.page)
        if m: self.registrant.email=m.group(1)

        m = re.search("Fax\.\.: (.+@.+)",self.page)
        if m: self.registrant.fax=m.group(1)

        m = re.search("Organization:(.+?)Phone:",self.page,re.S)
        if m: 
            start=m.start(1)
            end=m.end(1)
            registrant = string.strip(self.page[start:end])
            registrant = string.split(registrant, "\n")
            registrant = map(string.strip,registrant)

            self.registrant.organization = registrant[0]
            self.registrant.person =registrant[1]
            self.registrant.address = string.join(registrant[2:], "\n")

        m = re.search("Domain servers in listed order:\n\n(.+?)\n\n", self.page, re.S)
        if m:
            start = m.start(1)
            end = m.end(1)
            servers = string.strip(self.page[start:end])
            lines = string.split(servers, "\n")


            self.servers = []
            for line in lines:
                m=re.search("([\w|\.]+?)\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",string.strip(line))
                if m:
                    self.servers.append((m.group(1), m.group(2)))

        m = re.search("((?:(?:Administrative|Billing|Technical|Zone) Contact,?[ ]*)+:)\n", self.page)
        if m:
            i = m.start()
            m = re.search("Domain servers in listed order", self.page)
            j = m.start()
            contacts = string.strip(self.page[i:j])
        self._ParseContacts_RegisterCOM(contacts)


    def _ParseContacts_NetworkSolutions(self,page):
        parts = re.split("((?:(?:Administrative|Billing|Technical|Zone) Contact,?[ ]*)+:)\n", page)

        contacttypes = None
        for part in parts:
            if string.find(part, "Contact:") != -1:
                if part[-1] == ":": part = part[:-1]
                contacttypes = string.split(part, ",")
                continue
            part = string.strip(part)
            if not part: continue

            record=ContactRecord()

            lines = string.split(part, "\n")
            m = re.search("(.+) \((.+)\) (.+@.+)", lines.pop(0))
            if m:
                record.person = string.strip(m.group(1))
                record.handle = string.strip(m.group(2))
                record.email = string.lower(string.strip(m.group(3)))
                pass

            record.organization=string.strip(lines.pop(0))

            flag = 0
            addresslines = []
            phonelines = []
            phonelines.append(string.strip(lines.pop()))
            for line in lines:
                line = string.strip(line)
                #m=re.search("^(\d|-|\+|\s)+$",line)
                #if m: flag = 1
                if flag == 0:
                    addresslines.append(line)
                else:
                    phonelines.append(line)
                    pass
                pass
            record.phone = string.join(phonelines, "\n")
            record.address = string.join(addresslines, "\n")

            for contacttype in contacttypes:
                contacttype = string.lower(string.strip(contacttype))
                contacttype = string.replace(contacttype, " contact", "")
                record.type=contacttype
                self.contacts.update({contacttype:copy.copy(record)})
        return


    def ParseWhois_AllDomainsCOM(self):
        m = re.search("Record last updated on\.*: (.+)\.", self.page)
        if m: self.lastupdated = m.group(1)

        m = re.search("Created on\.*: (.+)\.", self.page)
        if m: self.created = m.group(1)

        m = re.search("Expires on\.*: (.+)\.",self.page)
        if m: self.expires=m.group(1)

        rawstr = r'Registrant:\n(?P<org>.*?)\s*\((?P<id>DOM-.*)\)'
        m = re.search(rawstr, self.page)

        if m:
            self.registrant.organization = m.group('org')

            idx = string.find(self.page, "\n\n", m.end(2))
            self.registrant.address = string.strip(self.page[m.end(2)+1:idx])

            m = re.search("(.+) \((.+)\)", self.registrant.organization)
            if m: 
                self.domainid   = m.group('id')

        m = re.search("Domain servers in listed order:\n\n", self.page)
        if m:
            i = m.end()
            m = re.search("\n\n", self.page[i:])
            j = m.start()
            servers = string.strip(self.page[i:i+j])
            lines = string.split(servers, "\n")
            self.servers = []
            for line in lines:
                m=re.search("([\w|\.]+?)\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",string.strip(line))
                if m:
                    self.servers.append((m.group(1), m.group(2)))

        m = re.search("((?:(?:Administrative|Billing|Technical|Zone) Contact,?[ ]*)+:)\n", self.page)
        if m:
            i = m.start()
            m = re.search("Created on", self.page)
            try:
                j = m.start()
            except:
                j = len(self.page)
            contacts = string.strip(self.page[i:j])

        self._ParseContacts_AllDomainsCOM(contacts)


    def _ParseContacts_AllDomainsCOM(self,page):
        parts = re.split("((?:(?:Administrative|Billing|Technical|Zone) Contact,?[ ]*)+:)\n", page)

        contacttypes = None
        for part in parts:
            if string.find(part, "Contact:") != -1:
                if part[-1] == ":": part = part[:-1]
                contacttypes = string.split(part, ",")
                continue
            part = string.strip(part)
            if not part: continue

            record=ContactRecord()

            rawstr = r'(?P<person>.*?)\s*\((?P<handle>NIC-.*)\)\s*(?P<org>.*?)\n'
            m = re.search(rawstr, part, re.DOTALL)
            if m:
                record.handle = m.group('handle')
                record.organization = m.group('org')
                record.person = m.group('person')
                part = part[m.end('org'):]

            rawstr = r'.*\s(?P<email>.*?@.*?)\s(?P<phone>.*?)\sFAX-\s(?P<fax>.*)'
            m = re.search(rawstr, part, re.IGNORECASE | re.DOTALL)
            if m:
                record.email = m.group('email')
                record.phone = string.strip(m.group('phone'))
                record.fax   = m.group('fax')
                part = part[:m.start('email')]

            lines = string.split(part, "\n")
            addresslines = map(string.strip, lines)
            record.address = string.strip(string.join(addresslines, "\n"))

            for contacttype in contacttypes:
                contacttype = string.lower(string.strip(contacttype))
                contacttype = string.replace(contacttype, " contact", "")
                record.type=contacttype
                self.contacts.update({contacttype:copy.copy(record)})


    def ParseWhois_BIZ(self):
        biz_contacts = (
            {"page_field": "Administrative",  "rec_field": "administrative"},
            {"page_field": "Billing",         "rec_field": "billing"},
            {"page_field": "Technical",       "rec_field": "technical"},
            {"page_field": "Registrant",      "rec_field": "registrant"}
            )

        # map of each page field name to the corresponding field of a ContactRecord()
        # struct is a tuple of dicts where each dict has "page_field" and "rec_field" key/vals
        biz_contact_fields = (
            {"page_field": "ID",             "rec_field": "handle"},
            {"page_field": "Organization",   "rec_field": "organization"},
            {"page_field": "Name",           "rec_field": "person"},
            {"page_field": "Address1",       "rec_field": "address"},
            {"page_field": "City",           "rec_field": "city"},
            {"page_field": "State/Province", "rec_field": "state"},
            {"page_field": "Postal Code",    "rec_field": "zip"},
            {"page_field": "Country",        "rec_field": "country"},
            {"page_field": "Phone Number",   "rec_field": "phone"},
            {"page_field": "Facsimile",      "rec_field": "fax"},
            {"page_field": "Email",          "rec_field": "email"}
            )

        self._ParseContacts_Generic(biz_contacts, biz_contact_fields)

        biz_fields = (
            {'page_field': "Domain ID",                  "rec_field": "domainid"},
            {'page_field': "Domain Registration Date",   "rec_field": "created"},
            {'page_field': "Domain Expiration Date",     "rec_field": "expires"},
            {'page_field': "Name Server",                "rec_field": "servers"}
            )

        self._ParseWhois_Generic(biz_fields)



    def ParseWhois_INFO(self):
        info_contacts = (
            {"page_field": "Admin",       "rec_field": "administrative"},
            {"page_field": "Billing",     "rec_field": "billing"},
            {"page_field": "Tech",        "rec_field": "technical"},
            {"page_field": "Registrant",  "rec_field": "registrant"}
            )

        # map of each page field name to the corresponding field of a ContactRecord()
        # struct is a tuple of dicts where each dict has "page_field" and "rec_field" key/vals
        info_contact_fields = (
            {"page_field": "ID",             "rec_field": "handle"},
            {"page_field": "Organization",   "rec_field": "organization"},
            {"page_field": "Name",           "rec_field": "person"},
            {"page_field": "Address",        "rec_field": "address"}, # for NAME
            {"page_field": "Adress",         "rec_field": "address"}, # for MUSEUM (mispelled!)
            {"page_field": "Street1",        "rec_field": "address"}, # for INFO
            {"page_field": "Street2",        "rec_field": "address2"},
            {"page_field": "Street3",        "rec_field": "address3"},
            {"page_field": "City",           "rec_field": "city"},
            {"page_field": "State/Province", "rec_field": "state"},
            {"page_field": "Postal Code",    "rec_field": "zip"},
            {"page_field": "Country",        "rec_field": "country"},
            {"page_field": "Phone",          "rec_field": "phone"},
            {"page_field": "Phone Number",   "rec_field": "phone"}, # for AERO, MUSEUM
            {"page_field": "Facsimile",      "rec_field": "fax"},
            {"page_field": "Fax Number",     "rec_field": "fax"}, # for AERO, MUSEUM
            {"page_field": "Email",          "rec_field": "email"}
            )

        self._ParseContacts_Generic(info_contacts, info_contact_fields)

        info_fields = (
            {'page_field': "Domain ID",           "rec_field": "domainid"},
            {'page_field': "Created On",          "rec_field": "created"},
            {'page_field': "Creation Date",       "rec_field": "created"},
            {'page_field': "Expires On",          "rec_field": "expires"}, #NAME
            {'page_field': "Expiration Date",     "rec_field": "expires"}, #INFO. #AERO
            {'page_field': "Last Updated",        "rec_field": "lastupdated"},
            {'page_field': "Updated On",          "rec_field": "lastupdated"}, #MUSEUM
            {'page_field': "Name Server",         "rec_field": "servers"}
            )

        self._ParseWhois_Generic(info_fields)


    def ParseWhois_COOP(self):
        coop_contacts = (
            {"page_field": "domain:Admin-",       "rec_field": "administrative"},
            {"page_field": "domain:Billing-",     "rec_field": "billing"},
            {"page_field": "domain:Tech-",        "rec_field": "technical"},
            {"page_field": "domain:Registrant-",  "rec_field": "registrant"}
            )

        # map of each page field name to the corresponding field of a ContactRecord()
        # struct is a tuple of dicts where each dict has "page_field" and "rec_field" key/vals
        coop_contact_fields = (
            {"page_field": "ID",                    "rec_field": "handle"},
            {"page_field": "Organization",          "rec_field": "organization"},
            {"page_field": "Name",                  "rec_field": "person"},
            {"page_field": "Address1",              "rec_field": "address"},
            {"page_field": "Address2",              "rec_field": "address2"},
            {"page_field": "City",                  "rec_field": "city"},
            {"page_field": "State/Province",        "rec_field": "state"},
            {"page_field": "Postcode",              "rec_field": "zip"},
            {"page_field": "Country",               "rec_field": "country"},
            {"page_field": "Phone-Number",          "rec_field": "phone"},
            {"page_field": "Facsimile-Number",      "rec_field": "fax"},
            {"page_field": "Email",                 "rec_field": "email"}
            )

        self._ParseContacts_Generic(coop_contacts, coop_contact_fields)

        coop_fields = (
            {'page_field': "domain:ID",           "rec_field": "domainid"},
            {'page_field': "domain:Registration", "rec_field": "created"},
            {'page_field': "domain:Expiration",   "rec_field": "expires"}, 
            {'page_field': "domain:Name-Server",  "rec_field": "servers"}
            )

        self._ParseWhois_Generic(coop_fields)


    def _ParseWhois_Generic(self, fields):
        for field in fields:
            regex = "%s: *(.+)" % field['page_field']
            #print regex
            if field['rec_field'] == "servers":
                self.servers = []
                servers = re.findall(regex, self.page)
                for server in servers:
                    try:
                        server = string.strip(server)
                        ip = socket.gethostbyname(server)
                    except:
                        ip = "?"
                    self.servers.append((server, ip))
            else:
                m = re.search(regex, self.page)
                #if m: print m.group(1)
                if m: setattr(self, field['rec_field'], string.strip(m.group(1)))



    def _ParseContacts_Generic(self, contacts, fields):
        for contact in contacts:
            if contact['rec_field'] == 'registrant':
                self._ParseGenericContact(self.registrant, contact['page_field'], fields)
            else:
                self.contacts[contact['rec_field']] = ContactRecord()
                self.contacts[contact['rec_field']].type = contact['rec_field']
                self._ParseGenericContact(self.contacts[contact['rec_field']], contact['page_field'], fields)


    def _ParseGenericContact(self, contact_rec, contact, fields):
        for field in fields:
            m = re.search("%s *.*%s: *(.+)" % (contact, field['page_field']), self.page)
            if not m: continue

            setattr(contact_rec, field['rec_field'], string.strip(m.group(1)))


    def ParseWhois_INT(self):
        int_contacts = (
            {"page_field": "Registrant", "rec_field": "registrant"},
            {"page_field": "Administrative Contact", "rec_field": "administrative"},
            {"page_field": "Technical Contact", "rec_field": "technical"})

        page = string.replace(self.page, "\r\n", "\n")
        for contact in int_contacts:
            page_field = contact['page_field']
            s = "%s:(.*)\n\W" % page_field
            m = re.search(s,  page, re.DOTALL)
            #if m: print m.group(1)
            print "-------------------"

##
## ----------------------------------------------------------------------
##




##
## ----------------------------------------------------------------------
##

def usage(progname):
    version = _version
    print __doc__ % vars()

def main(argv, stdout, environ):
    progname = argv[0]
    list, args = getopt.getopt(argv[1:], "", ["help", "version"])

    for (field, val) in list:
        if field == "--help":
            usage(progname)
            return
        elif field == "--version":
            print progname, _version
            return

    #rec=WhoisRecord()
    #rec=DomainRecord()

    for domain in args:
        whoisserver=None
        if string.find(domain,'@')!=-1:
            (domain, whoisserver)=string.split(domain,'@')
        try:
            d = DomainRecord(domain)
            d.whois(domain, whoisserver)
            #print "---> PAGE:",  d.page
            d.Parse()
            print str(d)
            #print rec.page
        except 'NoSuchDomain', reason:
            print "ERROR: no such domain %s" % domain
#	except socket.error, (ecode,reason):
            print reason
        except "TimedOut", reason:
            print "Timed out", reason

if __name__ == "__main__":
    main(sys.argv, sys.stdout, os.environ)
