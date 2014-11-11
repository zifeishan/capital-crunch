. env.sh
mkdir -p output/investments/
relurl=$1
relname=$2
curl --retry 3 --max-time 10 -X GET "$relurl" > output/investments/$relname
