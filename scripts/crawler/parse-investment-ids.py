import sys, os, json
import requests
import codecs 

userkey = os.getenv('USER_KEY')
datadir = 'output/organizations/'
outputdir = 'output/investments/'
files = os.listdir(datadir)

for f in files:
  js = json.load(open(datadir + f))

  try:
    url = js['data']['relationships']['investments']['paging']['first_page_url']
  except:
    continue
  print 'Crawling investment for', f
  realurl = "%s?user_key=%s" % (url, userkey)
  os.system("bash crawl-investment-byid.sh %s %s" % (realurl, f)) # relid relname  

