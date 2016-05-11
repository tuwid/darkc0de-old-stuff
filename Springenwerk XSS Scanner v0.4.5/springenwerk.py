"""
Springenwerk Security Scanner

(c)2006 by Johannes Fahrenkrug (jfahrenkrug@gmail.com)
http://springenwerk.org

A Python XSS Scanner.
"""

#Copyright (c) 2006, Johannes Fahrenkrug
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, 
#are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice, 
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice, 
#      this list of conditions and the following disclaimer in the documentation and/or 
#      other materials provided with the distribution.
#    * Neither the name of Johannes Fahrenkrug and the Springenwerk development team
#      nor the names of its contributors may be used to endorse or promote products 
#      derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
#EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
#OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
#SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED 
#TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
#BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
#CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
#ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH 
#DAMAGE.


__version__ = "0.4.5"

from urllib2 import Request, urlopen, URLError, HTTPError
import urllib
import string
import sys
import getopt
import time
from BaseHTTPServer import BaseHTTPRequestHandler
from BeautifulSoup import BeautifulSoup, UnicodeDammit

CSS_STYLES = """         
  body { background-color: #CCFFCC }
  h1 { font-size: 28px; color: #000000; margin: 0px 0px 10px; }
  h2 { font-size: 18px; color: #000000; margin: 0px 0px 10px; }
  h3 { font-size: 14px; color: #000000; margin: 0px 0px 10px; }
  td { font-size: 12px; line-height: 20px; padding: 2px 10px; }
  tr { background-color: #FFFFCC }
  .section { background-color: #FFFFFF; 
             line-height: 1.1; 
             padding: 10px; 
             border-top: 1px solid #666666; 
             border-right: 1px solid #666666; 
             border-bottom: 1px solid #666666; 
             border-left: 1px solid #666666; 
             margin: 15px; }
  table { border-top: 1px solid #666666;
          border-right: 1px solid #666666;
          border-bottom: 1px solid #666666;
          border-left: 1px solid #666666; }
  th { border-bottom: 2px solid #666666; }
  tr.even { background-color: #FFFF99 }
  """
USERAGENT_FF = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.1) Gecko/20060228 Firefox/1.5.0.1"  
USERAGENT_IE = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)"
USERAGENT_SW = "Springenwerk-" + __version__

def versionCheck():
    "Checks if Python is version 2.4.0 or greater"
    
    if sys.version_info[:3] < (2, 4, 0):
        print "You need Python 2.4.0 or greater to run Springenwerk."
        print "You are currently using version " + string.split(sys.version)[0] + "."
        sys.exit(2)
 
def main():
    "Parses the cmdline args and starts the scan"
    useragent = USERAGENT_SW
    resultfile = ''
    verbose = False
    checkargs = False
    withpost = False
    withactions = True
    
    print "Springenwerk Security Scanner, v" + __version__
    print "====================================="
    print "\"Is easy schnappen der Springenwerk.\""
    print
    print "(c)2006 by Johannes Fahrenkrug (jfahrenkrug@gmail.com)"
    print "http://springenwerk.org"
    print
    
    versionCheck()
    
    if (len(sys.argv) < 2):
        usage()
        sys.exit(2)
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'o:u:vpa', ['output=', 'useragent=', 'verbose', 'with-post', 'without-actions', 'checkargs'])
        # opts = opts[:1]
    except getopt.error, msg:
        sys.stdout = sys.stderr
        usage()
        print msg
        # print __doc__%globals()
        sys.exit(2)  
        
    if (len(args) < 1):
        usage()
        sys.exit(2)     
                    
    for o, a in opts:
        if (o == '-o' or o == '--output'):
            resultfile = a  
        if (o == '-v' or o == '--verbose'):
            verbose = True  
        if (o == '-p' or o == '--with-post'):
            withpost = True 
        if (o == '--without-actions'):
            withactions = False
        if (o == '-a' or o == '--checkargs'):
            checkargs = True
        if (o == '-u' or o == '--useragent'):
            if (a == 'ie'):
                useragent = USERAGENT_IE
            elif (a == 'ff'):
                useragent = USERAGENT_FF
            else:
                print "Unknown user-agent: " + a + ". Supported user-agents are \"ie\" and \"ff\"."
                usage()
                sys.exit(2) 
            
    startScan(args, resultfile, useragent, verbose, checkargs, withpost, withactions)    

def usage():
    "Prints the usage information"
    print "Usage: " + sys.argv[0] + " [--output=OUTPUT.HTML] [--useragent=(ie|ff)] [--verbose] [--with-post] [--without-actions] [--checkargs] TARGETURL [TARGETURL2 TARGETURL3...]"
    print 
    print "Options:"
    print "  -o|--output=OUTPUT.HTML"
    print "    Sets the html file that the scan results and exploits should be written to."
    print "    If the file doesn't exist, it will be created. If it exists, data will be appended."
    print "    Example: python springenwerk.py --output=/home/mbogo/spwkresults.html http://localhost/test.php"
    print "  -u|--useragent=(ie|ff)"
    print "    Sets the http user agent that will be used in the request headers;"
    print "    either Internet Explorer or Firefox."
    print "    The default is '" + USERAGENT_SW + "'"
    print "  -v|--verbose"
    print "    Hmmmmm....."
    print "  -p|--with-post"
    print "    Also checks for vulnerabilities by passing data to the target(s) using the http post method."
    print "  --without-actions"
    print "    Only checks the target itself, not the urls that have been found in the action attributes of its forms."
    print "  -a|--checkargs"
    print "    Also checks if the arguments that have been attached to the target url(s) are vulnerable."
    print "    Example: If the target url is 'http://localhost/test.php?arg1=fred&arg2=mbogo',"
    print "    arg1 and arg2 will be checked, too." 
    print
    print "Examples:"
    print "  python springenwerk.py http://localhost/test.php"
    print "  python springenwerk.py --output=/home/mbogo/spwkresults.html http://localhost/test.php"
    print "  python springenwerk.py --checkargs http://localhost/test.php?arg1=fred&arg2=mbogo"
    print "  python springenwerk.py --useragent=ff --verbose --with-post http://localhost/test1.php http://localhost/test2.php"
    
def startScan(urls, resultfile='', useragent=USERAGENT_SW, verbose=False, checkargs=False, withpost=False, withactions=True):
    "Scans a list of URLs for XSS vulnerabilities"
    print str(len(urls)) + " URL(s) to check..."  
    
    if (verbose):
        print "Using user-agent " + useragent                 
    
    for url in urls:     
        testTarget = TestTarget(url, resultfile, useragent, verbose, checkargs, withpost) 
        if (testTarget.urlOK):  
            testTarget.checkSelf()
            if (withactions):
                testTarget.checkFormActions()   
                
    print "Done."
    
def canBeConvertedToAscii(text):   
    "Checks if the given string can be converted to ASCII"
    
    if text != None:
        try:
            text.decode('ascii')
            return True
        except:
            return False
    else:
        return True  
        
                                  
class TestTarget:
    "Represents a target that should be checked for XSS vulnerabilities"
    
    def __init__(self, url, outputfile='', useragent=USERAGENT_SW, verbose=False, checkargs=False, withpost=False):
        "Sets the URL that should be scanned along with various options"   
        self.url = url
        self.useragent = useragent
        self.verbose = verbose
        self.checkargs = checkargs
        self.withpost = withpost
        self.outputfile = outputfile

        if (self.url.count("/") == 2):
            urlsplit = self.url.split('?', 1)
            if (len(urlsplit) == 2):
                self.url = urlsplit[0] + "/?" + urlsplit[1]
            else:
                self.url += "/"

        self.urlOK, self.origURLContents = self.getURLContents(self.url)
        
        if (self.urlOK): 
            self.forms = self.extractForms()
            
            #if args that are attached to the url should be checked, we have to extract them...
            if (self.checkargs):
                urlsplit = self.url.split('?', 1)
                if (len(urlsplit) == 2):
                    self.url = urlsplit[0]
                    args = urlsplit[1]
                    
                    self.forms.append({"formAction" : "", "inputs" : {}})
                    
                    for arg in args:
                        keyvalue = arg.split('=')
                        if (len(keyvalue) == 2):
                            value = keyvalue[1]
                        else:
                            value = ""
                        self.forms[len(self.forms)-1]["inputs"][keyvalue[0]] = value
            
            print str(len(self.forms)) + " form(s) to check..."
            #print parser.forms 
    
    def extractForms(self):
        "Extracts forms and their input and textarea fields from a (possibly) invalid html string using Beautiful Soup"
        
        forms = []
        soup = BeautifulSoup(self.origURLContents)

        for form in soup.findAll('form'):
            
            if form.has_key('action'):
                strAction = form['action']
            else:
                strAction = ""
            
            forms.append({"formAction" : strAction, "inputs" : {}})
        
            if self.verbose:
                if form.has_key('name'):
                    name = form['name']
                else:
                    name = "[noname]"
                
                print "  Found form '" + name + "', action: '" + strAction + "'"
    
            for input in form.findAll('input'):
                if input.has_key('name'):
                    if input.has_key('value'):
                        strValue = input['value']
                        
                        #urllib.quote doesn't like unicode... so unicode values have to go
                        if (not canBeConvertedToAscii(strValue)):
                            strValue = ""
                    else:
                        strValue = ""
                
                    forms[len(forms)-1]["inputs"][input['name']] = strValue
            
                    if self.verbose:                
                        print "    Found input '" + input['name'] + "', value: '" + strValue + "'"
                        
                        
            for textarea in form.findAll('textarea'):
                if textarea.has_key('name'):
                    if (len(textarea.contents) > 0):
                        text = textarea.contents[0]
                        
                        #urllib.quote doesn't like unicode... so unicode values have to go
                        if (not canBeConvertedToAscii(text)):
                            text = ""
                    else:
                        text = ""
                
                    forms[len(forms)-1]["inputs"][textarea['name']] = text
            
                    if self.verbose:                
                        print "    Found textarea '" + textarea['name'] + "', value: '" + text + "'"
                        
        return forms
    
    def checkSelf(self):
        "Scans only the target"
        if (self.verbose == False):
            print self.url
        formIndex = 1    
        for formItem in self.forms:   
            print "  Form " + str(formIndex) + " of " + str(len(self.forms)) 
            formIndex += 1
            self.checkTarget(self.url, formItem['inputs'], self.outputfile)
            if (self.withpost):
                if (self.verbose == False):
                    print "  Checking same form with POST..."
                self.checkTarget(self.url, formItem['inputs'], self.outputfile, True)
                
        print
        
    def checkFormActions(self):
        "Scans only the form actions of the target, but not the target itself"
        
        print "  Checking form actions..."
        
        formIndex = 1
        
        for formItem in self.forms:
            action = formItem['formAction']
            
            print "  Form " + str(formIndex) + " of " + str(len(self.forms)),
            formIndex += 1
            
            if (len(action) > 0):  
                if (action.startswith("http") == False):
                    action = self.url.rsplit('/', 1)[0] + "/" + action 

                print ", Action: " + action 
                self.checkTarget(action, formItem['inputs'], self.outputfile)
                if (self.withpost):
                    if (self.verbose == False):
                        print "  Checking same form with POST..."
                    self.checkTarget(action, formItem['inputs'], self.outputfile, True)
            else:
                print " ...skipping (already checked)"
        
    def checkTarget(self, url, params, outputfile='', postmethod=False):
        """
        Performs the actual scan.
        Takes a target url and a dictionary of parameters and values.
        One by one, each parameters original value is replaced by html control
        characters which are passed (via GET) to the target along with the rest 
        of the parameters with their original values.
        If the control characters are found in the resulting page, that parameter
        is vulnerable.
        """
        
        # XSS Test Strings
        xssTestCases = { "Script document.location" : "%22%3E%3Cscript%3Ealert(document.location)%3C%2Fscript%3E%3Cbr%20bla%3D%22", 
                         "Inputfield" : "%22%3E%3Cinput%20type%3D%22text%22%20value%3D%22SoylentGreen",
                         "IFrame" : "%22%3E%3Ciframe%20src=http://www.google.com%3E%3C/iframe%3E%3Cbr%20bla=%22",
                         "Body onLoad JS" : "%22%3E%3Cbody%20onload=%22javascript:alert(%27XSS%27)%22%3E%3C/body%3E%3Cbr%20bla=%22",
                         "onChange JS" : "%22%20onChange=%22alert(document.location)" }
        
        htmlControlString = u"\" >"
        
        writeoutput = False
        vulnerabilities = 0
        
        if (len(outputfile) > 0):
            writeoutput = True
            try:
                f = open(outputfile, "r")
                lines = f.readlines()
                f.close()
            except:
                lines = []
        
            f = open(outputfile, "w")
    
            if (len(lines) < 1):
                if (self.verbose):
                    print "    Writing output to new file " + outputfile
                f.write("<html><head><style>\n" + CSS_STYLES + """
                         </style>
                         <title>Springenwerk Security Scanner</title>
                         </head><body><div style="text-align: center">
                         <h1>Springenwerk Security Scanner v""" + __version__ + "</h1>\n")
            else:
                if (self.verbose):
                    print "    Appending output to existing file " + outputfile
                for i in range(len(lines)-1):
                    f.write(lines[i])
                    
            f.write("<div class=\"section\"><h2>" + url)
            if (postmethod):
                f.write(" (POST)")
            f.write("</h2>\n<h2>Arguments: ") 
            htmlArgsString = ""
            for arg in params.keys():
                if (len(htmlArgsString) > 0):
                    htmlArgsString += ", "
                htmlArgsString += arg
            f.write(htmlArgsString + "</h2>\n<h3>" + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) + "</h3>\n")
            f.write("<table border=\"0\" cellspacing=\"0\" cellpadding=\"0\"><tr><th>Parameter</th><th colspan=\"" + str(len(xssTestCases)) + "\">Tests</th></tr>\n")
    
            even = False;
            
    
        for pToBeChecked in params.keys():
            if (postmethod):
                postData = ""
                for origParam in params.keys():
                    if (origParam != pToBeChecked):
                        postData += origParam + "=" + urllib.quote(params[origParam]) + "&"
                postData += pToBeChecked + "=" + urllib.quote(htmlControlString) + pToBeChecked
                
                if (self.verbose):
                    print "    Checking " + url + " with POST data:"
                    print "      " + postData
    
                success, s = self.getURLContents(url, postData)
            else:    
                if (url.find("?") == -1):
                    urlWithParams = url + "?"
                else:
                    urlWithParams = url + "&"
                untouchedParams = ""
            
                for origParam in params.keys():
                    if (origParam != pToBeChecked):
                        untouchedParams += origParam + "=" + urllib.quote(params[origParam]) + "&"
                    
                    
                urlWithParams += untouchedParams + pToBeChecked + "=" + urllib.quote(htmlControlString) + pToBeChecked
            
                if (self.verbose):
                    print "    Checking " + urlWithParams
    
                success, s = self.getURLContents(urlWithParams)

            
            if (success):
                if (self.verbose):
                    print "    Looking for " + htmlControlString + pToBeChecked,
                pos = s.find(htmlControlString + pToBeChecked)
                if (pos != -1):
                    vulnerabilities += 1
                                        
                    if (self.verbose):
                        print "...FOUND!"
                    else:
                        print "    Vulnerable: " + pToBeChecked
            
                    if(writeoutput):
                        f.write("<tr")
        
                        if (even):
                            f.write(" class=\"even\"")
                        
                        f.write("><td>" + pToBeChecked + "</td>")
                        
                        if (postmethod):
                            hiddenFields=""
                            for origParam in params.keys():
                                if (origParam != pToBeChecked):
                                    hiddenFields += "<input type=\"hidden\" name=\"" + origParam + "\" value=\"" + params[origParam] + "\"/>"
                                
                            for xssCase in xssTestCases:
                                f.write("<td><form method=\"POST\" action=\"" + url + "\">" + hiddenFields + "<input type=\"hidden\" name=\"" + pToBeChecked + "\" value=\"" + xssTestCases[xssCase] + "\"><input type=\"submit\" value=\"" + xssCase + "\"/></form></td>\n")
                        else:
                            for xssCase in xssTestCases:
                                f.write("<td><a href=\"" + url + "?" + untouchedParams + pToBeChecked + "=" + xssTestCases[xssCase] + "\">" + xssCase + "</a></td>\n") 

                        f.write("</tr>\n")
  
                        even = not even    
                elif (self.verbose):
                    print
        
        if (writeoutput):
            if (vulnerabilities < 1):
                f.write("<tr><td colspan=\"" + str(len(xssTestCases)+1) + "\">No vulnerabilities found.</td></tr>\n")
            
            f.write("</table></div>\n")
            f.write("</div></body></html>")
            f.close()
            
        print "    " + str(vulnerabilities) + " vulnerabilit(y/ies) found."
        
    def getURLContents(self, url, data=None):    
        "Returns the contents of the given URL as an Unicode string" 
        
        s = ""
        success = False
        
        req = Request(url, data, {'User-agent': self.useragent})
        
        try:
            f = urlopen(req)  
            s = f.read()
            f.close()
            success = True
        except HTTPError, e:
            print 'Server error: ', e.code
            if (self.verbose and BaseHTTPRequestHandler.responses.has_key(e.code)):
                title, msg = BaseHTTPRequestHandler.responses[e.code]            
                print title + ": " + msg
        except URLError, e:
            print 'Connection error: ', e.reason
            
        dammit = UnicodeDammit(s)    
          
        return (success, dammit.unicode) 
    
if __name__ == '__main__':
    main()   
