cat data/generated-negative-example/* | psql $DBNAME -c "COPY investment(investor_id, startup_id, is_true) FROM STDIN"
psql $DBNAME -c "ANALYZE investment"