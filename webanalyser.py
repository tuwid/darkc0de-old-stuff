# Download Chilkat library,it free :)
import chilkat,sys,os
if len(sys.argv)<2:
	print "\n beenudel1986[at]gmail[dot]com "
	print "./webanalyser.py <site-name> "
	sys.exit(1)

url=sys.argv[1]
spider = chilkat.CkSpider()
spider.Initialize(url)
print "\n[+] Fetching Robots.txt for the directory listing"
robotsText = spider.fetchRobotsText()
print robotsText
spider = chilkat.CkSpider()
spider.Initialize(url)
spider.AddUnspidered(url)
spider.CrawlNext()

print "\n[-] Website Title: "+spider.lastHtmlTitle()
print "[-] Website Description:"+spider.lastHtmlDescription()
print "[-] Website Keywords:"+spider.lastHtmlKeywords()
print "\n[+] Crawling the Website.\n"
num=raw_input('\n Enter the Number of links you want to crawl\n\t')

for i in range(0,int(num)):

    success = spider.CrawlNext()
    if (success == True):
        print spider.lastUrl()
	file=open('links.txt', 'a')
	file.write(spider.lastUrl() +"\n")
     
    else:
     
        if (spider.get_NumUnspidered() == 0):
            print "No more URLs to spider"
	    break
        else:
            print spider.lastErrorText()

    spider.SleepMs(1000)