#! /usr/bin/env python

import json, sys, os, re
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

def getPath(personId):
  return os.environ['DATA_DIR'] + '/people/' + personId

for line in sys.stdin:
  org_id, path = line.strip().split('\t')

  try : 
    js = json.load(open(path))
    relationships = js['data']['relationships']
    if 'current_team' in relationships:
      people = relationships['current_team']['items']
    else:
      continue
  except:
    continue

  for person in people:

    person_title = ''
    if 'title' not in person: continue
    title = person['title']
    if 'Founder' in title and 'CEO' in title:
      person_title = 'founder+ceo'
    elif 'Founder' in title:
      person_title = 'founder'
    elif 'CEO' in title:
      person_title = 'ceo'
    else:
      # Not an important person
      continue

    personId = person['path'].split('/')[-1]
    profilePath = getPath(personId) # a particular function that could give the profile 
    try: 
      peopleJs = json.load(open(profilePath))
    except:
      continue

    features = []
    FEATURE_TYPE = 'people_text'
    try:
      last_name = peopleJs['data']['properties']['last_name']
      features.append([FEATURE_TYPE, 'last_name=%s' % last_name, 1])
    except:
      pass
    try:
      first_name = peopleJs['data']['properties']['first_name']
      features.append([FEATURE_TYPE, 'first_name=%s' % first_name, 1])
    except:
      pass

    # person bio is Too sparse
    # try:
    #   bio = peopleJs['data']['properties']['bio']
    #   words = bio.strip().split(' ')
    #   for w in words:
    #     if w in ENGLISH_STOP_WORDS: continue
    #     features.append([FEATURE_TYPE, 'short_bio_1gram=%s' % w.lower(), 1])
    # except:
    #   pass

    try: 
      personRelationships = peopleJs['data']['relationships']
    except:
      continue

    if 'degrees' in personRelationships:
      degrees = personRelationships['degrees']['items']
      paging = personRelationships['degrees']['paging']
      isMBA = any(degree['degree_subject']  == 'MBA' for degree in degrees)
      if isMBA:
        features.append([FEATURE_TYPE, 'MBA_obtained', 1])

      if 'total_items' in paging:
        features.append(['people_numeric', 'num_degrees', paging['total_items']])

      for degree in degrees:
        if 'organization_name' not in degree: continue
        university_name = degree['organization_name']
        features.append([FEATURE_TYPE, 'university_name=%s' % university_name, 1])

        # if i == paging['total_items']:
        #   time = degree['completed_on']
        #   features.append(FEATURE_TYPE, 'time of graduation', time)

    else:
      features.append(['people_numeric', 'num_degrees', 0])

    try:
      experiences = personRelationships['experience']['items']
      for experience in experiences:
        if 'organization_name' not in experience: continue
        company_name = experience['organization_name']
        features.append([FEATURE_TYPE, 'company_name=%s' % company_name, 1])
    except:
      continue

    # Output data
    for f in features:
      try:
        print '\t'.join(re.sub(r'\\', r'\\\\', str(_)) for _ in [org_id, f[0], person_title+':'+f[1], f[2]])
      except Exception as e:
        # print >>sys.stderr, 'Error:', org_id, f, e
        pass

