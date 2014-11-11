. env.sh
mkdir -p output/people

peoplelist="data/people-list.txt"

for person in $(cat $peoplelist); do
  echo "Getting $person..."
  curl --retry 3 --max-time 10 -X GET "http://api.crunchbase.com/v/2/person/$person?user_key=$USER_KEY" > output/people/$person
  sleep 0.5  # 200 requests / minute
done
