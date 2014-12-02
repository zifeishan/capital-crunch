psql $DBNAME -c " COPY(
        SELECT  investor_id,
                startup_id,
		ss.description as startup_description,
		si.description as investor_description,
                is_true, expectation, features
        FROM    investment_is_true_inference NATURAL JOIN 
          ( SELECT  startup_id, 
                    ARRAY_AGG( CASE WHEN type like '%_numeric' THEN feature || '==' || value
		               ELSE feature END 
			       order by feature) as features
            FROM    startup_feature 
            -- WHERE   type='basic_text' OR type='basic_numeric'
            GROUP BY startup_id
            ) t, description si, description ss
        WHERE   expectation > 0.95 AND is_true is not null
	AND ss.org_id = startup_id
	AND si.org_id = investor_id
        order by random() limit 1000
	) TO STDOUT CSV HEADER;
" > ./investment-precision/input.csv
