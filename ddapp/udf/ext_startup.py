#! /usr/bin/env python

import json, sys, re
import ddlib  # Load the ddlib Python library for NLP functions

# For each input row
for line in sys.stdin:
  org_id, path = line.strip().split('\t')
  # Load the JSON object
  try:
    js = json.load(open(path))
    role = js['data']['properties']['primary_role']
    if role == "company":
      # description = re.sub(r'\n', ' ', description)
      # description = re.sub(r'\t', ' ', description)
      # description = re.sub(r'\x00', '', description)
      # if not IsASCII(description): continue
      print org_id
  except:
    continue
