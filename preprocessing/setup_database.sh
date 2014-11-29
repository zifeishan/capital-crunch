#! /usr/bin/env bash

set -eu

DBNAME=crunchbase
echo "Set DB_NAME to ${DBNAME}."
echo "HOST is ${PGHOST}, PORT is ${PGPORT}."

psql -d $DBNAME < schema.sql

DATADIR=../scripts/crawler/output/
EDGEDIR=$DATADIR/investments-edges/
STARTUPS=../data/startups.txt
INVESTORS=../data/investors.txt

psql -d $DBNAME -c "COPY startup from STDIN;" < $STARTUPS
psql -d $DBNAME -c "COPY investor from STDIN;" < $INVESTORS
cat $EDGEDIR/* | psql -d $DBNAME -c "COPY known_investment from STDIN;"

python generate_tsv.py ../scripts/crawler/output/organizations/ | psql -d $DBNAME -c "COPY organization_path from STDIN;"