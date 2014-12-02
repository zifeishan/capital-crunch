#! /bin/bash

. "$(dirname $0)/env.sh"

export GPPATH=/tmp/
export GPPORT=15433
export GPHOST=rambo

# Launch gpfdist if not launched.
gpfdist -d $GPPATH -p $GPPORT &

export DATA_DIR=../scripts/crawler/output/

### Run with deepdive binary:
deepdive -c application.conf

### Compile and run:
# sbt "run -c $APP_HOME/application.conf"
