import sys, os, json
import requests
import codecs 

userkey = os.getenv('USER_KEY')


# http://api.crunchbase.com/v/2/organizations?user_key=<user-key>&order=updated_at%20desc

organizations = json.load(open(sys.argv[1]))

# fout = codecs.open('organization-list.txt', 'w', 'utf-8')
fout = open('organization-list.txt', 'w')
for i, org in enumerate(organizations):
  if i % 10000 == 0:
    print 'Iteration #',i

  curl = org['crunchbase_url']
  # print curl
  assert curl.startswith('http://www.crunchbase.com/organization/')
  cid = curl[len('http://www.crunchbase.com/organization/'):].split('?')[0]
  # Ignore encoding errors: drop all companies with non-ASCII id
  try: 
    print >>fout, cid
  except:
    continue

fout.close()
# url = "http://api.crunchbase.com/v/2/organization/%s?user_key=%s" % (cid, userkey)

# r = requests.get(url)
# js = r.json()
# fout = ('organization/%s' % cid, 'w')
# json.dump(js, fout, indent=2)
# fout.close()