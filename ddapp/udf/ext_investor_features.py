#! /usr/bin/env python

import json, sys, math
import ddlib  # Load the ddlib Python library for NLP functions

# For each input row
for line in sys.stdin:
  org_id, path = line.strip().split('\t')
  # Load the JSON object
  try:
    js = json.load(open(path))
  except:
    continue

  # "js" is the organization json object.
  ##### WRITE FEATURE EXTRACTOR HERE
  # feature: (type, key, value)
  features = []
  
  FEATURE_TYPE = 'basic_numeric'

  try: 
    relationships = js['data']['relationships']
  except:
    continue

  try:
    if 'investments' in relationships:
      numInvestments = relationships['investments']['paging']['total_items']
      features.append([FEATURE_TYPE, 'num_investments', numInvestments])
  except: 
    pass

  try:
    if 'acquisitions' in relationships:
      numAcquisitions = relationships['acquisitions']['paging']['total_items']
      features.append([FEATURE_TYPE, 'num_investments', numAcquisitions])
  except: 
    pass

  FEATURE_TYPE = 'basic_text'

  try:
    if 'headquarters' in relationships:
      headquarters = relationships['headquarters']['items']
      for o in headquarters:
        features.append([FEATURE_TYPE, 'headquarter=%s' % (o['city']), 1])
  except: 
    pass

  try:
    if 'categories' in relationships:
      categories = js['data']['relationships']['categories']['items']
      for o in categories:
        features.append([FEATURE_TYPE, 'category=%s' % (o['name']), 1])
  except: 
    pass

  FEATURE_TYPE = 'graph'

  try:
    if 'founders' in relationships:
      founders = js['data']['relationships']['founders']['items']
      for o in founders:
        features.append([FEATURE_TYPE, 'founder=%s' % (o['path'].split('/')[1]), 1])
  except:
    pass
  
  # Output data
  for f in features:
    try:
      print '\t'.join(str(_) for _ in [org_id] + f)
    except Exception as e:
      # print >>sys.stderr, 'Error:', org_id, f, e
      pass

