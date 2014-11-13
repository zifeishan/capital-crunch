psql $DBNAME -c "
        SELECT  investor_id, features,
                startup_id
                is_true, expectation
        FROM    investment_is_true_inference NATURAL JOIN 
          ( SELECT  startup_id, 
                    ARRAY_AGG(feature) as features
            FROM    startup_feature 
            WHERE   type='basic_text'
            GROUP BY startup_id
            ) t
        WHERE   expectation > 0.95
        order by random() limit 100;
" | less