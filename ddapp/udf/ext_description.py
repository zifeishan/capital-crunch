#! /usr/bin/env python

import json, sys, re
import ddlib  # Load the ddlib Python library for NLP functions

def IsASCII(s):
  return all(ord(c) < 128 for c in s)

# For each input row
for line in sys.stdin:
  org_id, path = line.strip().split('\t')
  # Load the JSON object
  try:
    js = json.load(open(path))
    description = js['data']['properties']['description']
    description = re.sub(r'\n', ' ', description)
    description = re.sub(r'\t', ' ', description)
    description = re.sub(r'\x00', '', description)
    if not IsASCII(description): continue
    print '\t'.join([org_id, description])
  except:
    continue
