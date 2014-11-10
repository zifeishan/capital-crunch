. env.sh
mkdir -p quickget_output
curl -v  -X GET "http://api.crunchbase.com/v/2/organization/$1?user_key=$USER_KEY" > quickget_output/$1.json