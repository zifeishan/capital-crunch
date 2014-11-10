. env.sh
mkdir -p output/organizations

orglist="data/organization-list.txt"
for org in $(cat $orglist); do
  echo "Getting $org..."
  curl -v  -X GET "http://api.crunchbase.com/v/2/organization/$org?user_key=$USER_KEY" > output/organizations/$org.json
  sleep 0.3  # 200 requests / minute
done

# curl -v  -X GET "http://api.crunchbase.com/v/2/organization/$1?user_key=$USER_KEY" > organizations/$1.json