. env.sh
mkdir -p output/investments/
relurl=$1
relname=$2
curl --retry 3 --max-time 10 -X GET "$realurl" > output/investments/$relname
sleep 1.0  # 200 requests / minute
