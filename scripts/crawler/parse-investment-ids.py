import sys, os, json, time
import requests
import codecs 

userkey = os.getenv('USER_KEY')
datadir = 'output/organizations/'
outputdir = 'output/investments/'
files = os.listdir(datadir)

fout = open('investment-file-lists.txt', 'w')
for f in files:
  print >>fout, f
fout.close()


for f in files:
  js = json.load(open(datadir + f))

  try:
    url = js['data']['relationships']['investments']['paging']['first_page_url']
  except:
    continue
  # print 'Crawling investment for', f
  realurl = "%s?user_key=%s" % (url, userkey)
  print "bash crawl-investment-byid.sh %s %s" % (realurl, f)
  time.sleep(2.0)  
  os.system("bash crawl-investment-byid.sh %s %s" % (realurl, f)) # relid relname  

