import sys, os
path = sys.argv[1]

files = os.listdir(path)

for fname in files:
  fpath = path + '/' + fname
  print '%s\t%s' % (fname[:-5], fpath)
