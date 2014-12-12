#! /usr/bin/env python

import sys
import ddlib     # DeepDive python utility
from collections import defaultdict

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


ARR_DELIM = '~^~'

def ngrams(words, gram_len):
  ngram = {}
  for i in range(len(words) - gram_len):
    gram = ' '.join(words[i : i + gram_len])
    if gram not in ngram:
      ngram[gram] = 0
    ngram[gram] += 1
    # Optimize: cross product...
  return ngram

# For each input tuple
for row in sys.stdin:
  features = []
  parts = row.strip().split('\t')
  document_id, sentence_id = parts[:2]
  words, lemmas, pos_tags, ner_tags, dep_paths, dep_parents = [part.split(ARR_DELIM) for part in parts[2:]]
  

  # Locations
  FEATURE_TYPE = 'nlp'
  start_index = 0
  phrases = set()

  while start_index < len(words):
    # Checking if there is a LOCATION phrase starting from start_index
    index = start_index
    while index < len(words) and ner_tags[index] == "LOCATION":
      index += 1
    if index != start_index:   # found a person from "start_index" to "index"
      text = ' '.join(words[start_index:index])
      length = index - start_index
      phrases.add(text)
    start_index = index + 1

  for text in phrases:
    features.append([FEATURE_TYPE, 'location=%s' % text, 1])

  # Bigrams
  # TODO too large.. not used

  # # Special NERs
  # start_index = 0
  # phrases = set()

  # while start_index < len(words):
  #   # Checking if there is a phrase starting from start_index
  #   index = start_index
  #   current_ner = "O"
  #   # must have coherent tags
  #   while index < len(words) and ner_tags[index] not in ["LOCATION", "O"] and (index == start_index or ner_tags[index] == ner_tags[index - 1]): 
  #     index += 1
  #   if index != start_index:   # found a person from "start_index" to "index"
  #     text = ' '.join(words[start_index:index])
  #     length = index - start_index
  #     phrases.add((ner_tags[index], text))
  #   start_index = index + 1

  # for ner, text in phrases:
  #   features.append([FEATURE_TYPE, 'phase[%s]=%s' % (ner, text), 1])

  # unigram-lemmas of Nouns (non-stop-words)
  start_index = 0
  phrases = set([lemmas[i] for i in range(len(words)) if \
      pos_tags[i].startswith('NN') and \
      lemmas[i] not in ENGLISH_STOP_WORDS and \
      ner_tags[i] != "LOCATION" # redundant
    ])

  for word in phrases:
    features.append([FEATURE_TYPE, 'noun-1gram=%s' % word, 1])

  # Output data
  for f in features:
    try:
      print '\t'.join(str(_) for _ in [document_id] + f)
    except Exception as e:
      # print >>sys.stderr, 'Error:', document_id, f, e
      pass

