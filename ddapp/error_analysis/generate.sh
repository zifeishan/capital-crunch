psql $DBNAME -c " COPY(
        SELECT  investor_id,
                startup_id,
                is_true, expectation, features
        FROM    investment_is_true_inference NATURAL JOIN 
          ( SELECT  startup_id, 
                    ARRAY_AGG( CASE WHEN type='basic_text' THEN feature
		               ELSE feature || '==' || value END 
			       order by feature) as features
            FROM    startup_feature 
            WHERE   type='basic_text' OR type='basic_numeric'
            GROUP BY startup_id
            ) t
        WHERE   expectation > 0.95 AND is_true is not null
        order by random() limit 100
	) TO STDOUT HEADER;
" > ./investment-precision/input.tsv
