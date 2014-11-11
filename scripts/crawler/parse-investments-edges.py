import sys, os, json, time
import requests
import codecs 

datadir = 'output/investments/'

outputdir = 'output/investments-edges/'

files = os.listdir(datadir)

for f in files:
  source = f[:-5]
  
  print f
  try:
    js = json.load(open(datadir + f))
  except: 
    print 'Error at file', f
    continue

  # print js
  items = js['data']['items']
  # print items
  fout = open(outputdir + source, 'w')
  # print outputdir + source
  for item in items:
    # print item['invested_in']['path'].split('/')[1]
    try:
      if item['invested_in']['path'] is None: continue
      target = item['invested_in']['path'].split('/')[1]
    except Exception as e:
      print 'Error at file', item
      # print items
      # raw_input()
      print e
      continue

    print >>fout, '\t'.join([source, target])

  fout.close()
  print 'Parsed %d edges from %s' % (len(items), source)



