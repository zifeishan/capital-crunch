#! /bin/bash
set -eu

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

echo "Saving configurations.."
OUT_DIR=out/`ls -t out/ | head -n 1`
cp application.conf $OUT_DIR/
echo "Saved to out/"`ls -t out/ | head -n 1`
echo " ========= Bucket distribution: =========="
cat $OUT_DIR/calibration/*.tsv

echo ""
echo " ========= Evaluation: ========== "
echo ""
python scoring.py < $OUT_DIR/calibration/*.tsv > $OUT_DIR/score.tsv
