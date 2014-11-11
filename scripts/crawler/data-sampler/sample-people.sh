# Compute observed overlaps
for file in $(cat $1); do
  mkdir -p sampled-people-output
  cp ../output/people/$file sampled-people-output/
done
