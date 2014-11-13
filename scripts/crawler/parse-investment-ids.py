import sys, os, json, time
import requests
import codecs 

userkey = os.getenv('USER_KEY')
datadir = 'output/organizations/'
outputdir = 'output/investments/'


files = os.listdir(datadir)
existing = set(os.listdir(outputdir))
lastfiles = set([l.strip() for l in open('investment-file-lists-11121524.txt').readlines()])

# Write all files for this round if not existing
fout = open('investment-file-lists.txt', 'w')
for f in files:
  if f not in existing:
    print >>fout, f
fout.close()

files = [f for f in files if f not in existing and f not in lastfiles]

print "Start parsing..."
for i, f in enumerate(files):
  if f in existing:
    continue

  try:
    js = json.load(open(datadir + f))
    if 'investments' not in js['data']['relationships']: continue
    url = js['data']['relationships']['investments']['paging']['first_page_url']
  except Exception as e:
    # print e
    continue
  # print 'Crawling investment for', f
  realurl = "%s?user_key=%s" % (url, userkey)
  print "[%d / %d] bash crawl-investment-byid.sh %s %s" % (i, len(files), realurl, f)
  time.sleep(0.5)  
  os.system("bash crawl-investment-byid.sh %s %s" % (realurl, f)) # relid relname  

