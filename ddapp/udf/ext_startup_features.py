#! /usr/bin/env python

import json, sys
import ddlib  # Load the ddlib Python library for NLP functions

ENGLISH_STOP_WORDS = frozenset([
      "a", "about", "above", "across", "after", "afterwards", "again", "against",
      "all", "almost", "alone", "along", "already", "also", "although", "always",
      "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
      "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
      "around", "as", "at", "back", "be", "became", "because", "become",
      "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
      "below", "beside", "besides", "between", "beyond", "bill", "both",
      "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
      "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
      "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
      "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
      "everything", "everywhere", "except", "few", "fifteen", "fify", "fill",
      "find", "fire", "first", "five", "for", "former", "formerly", "forty",
      "found", "four", "from", "front", "full", "further", "get", "give", "go",
      "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
      "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
      "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
      "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
      "latterly", "least", "less", "ltd", "made", "many", "may", "me",
      "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
      "move", "much", "must", "my", "myself", "name", "namely", "neither",
      "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
      "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
      "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
      "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
      "please", "put", "rather", "re", "same", "see", "seem", "seemed",
      "seeming", "seems", "serious", "several", "she", "should", "show", "side",
      "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
      "something", "sometime", "sometimes", "somewhere", "still", "such",
      "system", "take", "ten", "than", "that", "the", "their", "them",
      "themselves", "then", "thence", "there", "thereafter", "thereby",
      "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
      "third", "this", "those", "though", "three", "through", "throughout",
      "thru", "thus", "to", "together", "too", "top", "toward", "towards",
      "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
      "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
      "whence", "whenever", "where", "whereafter", "whereas", "whereby",
      "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
      "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
      "within", "without", "would", "yet", "you", "your", "yours", "yourself",
      "yourselves"])

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
  
  # FEATURE_TYPE = 'basic_numeric'

  # try:
  #   totalFunding = log(js['data']['properties']['total_funding_usd'])
  #   features.append([FEATURE_TYPE, 'total_funding_log', totalFunding])
  # except:
  #   pass

  FEATURE_TYPE = 'basic_text'

  try:
    foundYear = js['data']['properties']['founded_on_year']
    features.append([FEATURE_TYPE, 'founded_on_year=%d' % foundYear, 1])
  except:
    pass

  try: 
    relationships = js['data']['relationships']
  except:
    continue

  # try:
  #   text = js['data']['properties']['short_description']
  #   words = text.strip().split(' ')
  #   for w in words:
  #     if w in ENGLISH_STOP_WORDS: continue
  #     features.append([FEATURE_TYPE, 'short_bio_1gram=%s' % w.lower(), 1]) # addable
  # except:
  #   pass


  FEATURE_TYPE = 'basic_numeric'

  try:
    if 'competitors' in relationships:
      numCompetitors = relationships['competitors']['paging']['total_items']
      features.append([FEATURE_TYPE, 'num_competitors', numCompetitors])
  except: 
    pass

  try:
    if 'websites' in relationships:
      numWebsites = relationships['websites']['paging']['total_items']
      features.append([FEATURE_TYPE, 'num_websites', numWebsites])
  except: 
    pass

  # try:
  #   if 'acquisitions' in relationships:
  #     numAcquisitions = relationships['acquisitions']['paging']['total_items']
  #     features.append([FEATURE_TYPE, 'num_investments', numAcquisitions])
  # except: 
  #   pass

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

  FEATURE_TYPE = 'cheat'

  # Cheat with funding rounds
  if 'funding_rounds' in relationships:
    num_funding_rounds = relationships['funding_rounds']['paging']['total_items']
    features.append([FEATURE_TYPE, 'funding_rounds', num_funding_rounds])
    if num_funding_rounds > 0:
      features.append([FEATURE_TYPE, 'has_funding_rounds', 1])
  else:
    features.append([FEATURE_TYPE, 'funding_rounds', 0])

    

  
  # Output data
  for f in features:
    try:
      # print '\t'.join(re.sub(r'\\', r'\\\\', str(_)) for _ in [org_id] + f)
      print '\t'.join(str(_) for _ in [org_id] + f)
    except Exception as e:
      # print >>sys.stderr, 'Error:', org_id, f, e
      pass

