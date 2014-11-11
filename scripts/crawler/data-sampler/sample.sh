# Compute observed overlaps
for file in $(cat sampled-companies.txt); do
  mkdir -p output
  cp ../output/organizations/$file output/
done
