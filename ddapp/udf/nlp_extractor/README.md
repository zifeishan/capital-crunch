# NLP Extractor

### Input

JSON of following form, where `key` and `value` are specified using command line options. For example `./run.sh --key id --value text`

    { id: [document_id], text: [raw_text] }

### Output

JSON tuple of the form:

    {
      document_id: [document_id_from_input],
      sentence: [raw_sentence_text],
      words: [array_of_words],
      post_tags: [array_of_pos_tags],
      ner_tags: [array_of_ner_tags],
      dependencies: [array of collapsed dependencies]
      sentence_offset: [0,1,2... which sentence is it in document]
      sentence_id: [document_id@sentence_offset]
    }

You can create a table like this, to be the `output_relation`:

    CREATE TABLE sentences (
      document_id bigint,      -- document id
      sentence text,           -- sentence id
      wordidxs int[],          -- word indexes
      words text[],            -- words
      lemma text[],            -- lemmified version of words
      pos_tags text[],         -- parts of speech
      dep_paths text[],        -- dependency path labels. "_" for no dependency
      dep_parents text[],      -- dependency path parents, range from 1--N. 0 for no dependency.
      ner_tags text[],         -- named entity recognition tags
      sentence_offset bigint,  -- sentence offset in article (0...N-1)
      sentence_id text         -- sentence id, unique identifier for sentences
    );

crunchbase=# select is_true, count(*) from investment group by is_true;
 is_true |  count
---------+---------
 f       | 4026782
 t       |    8327
(2 rows)


$ cat /lfs/rambo/0/zifei/cs221/capital-crunch/ddapp/out/2014-12-01T221854/calibration/investment.is_true.tsv
0.00    0.10    1006224 1911    1004313
0.10    0.20    1107    45      1062
0.20    0.30    459     10      449
0.30    0.40    269     7       262
0.40    0.50    81      6       75
0.50    0.60    46      2       44
0.60    0.70    47      6       41
0.70    0.80    24      5       19
0.80    0.90    16      1       15
0.90    1.00    16      4       12

$ cat /lfs/rambo/0/zifei/cs221/capital-crunch/ddapp/out/2014-12-01T233736/calibration/investment.is_true.tsv
0.00    0.10    1003444 1931    1001513
0.10    0.20    2062    58      2004
0.20    0.30    701     25      676
0.30    0.40    271     10      261
0.40    0.50    140     6       134
0.50    0.60    85      4       81
0.60    0.70    57      1       56
0.70    0.80    44      6       38
0.80    0.90    27      1       26
0.90    1.00    15      1       14


## AFTER re-extraction:

crunchbase=# select count(*) from startup;
 count
-------
 73589
(1 row)

crunchbase=# select count(distinct startup_id) from known_investment ;
 count
-------
 12094
(1 row)

# First run: without people / NLP
$ cat /lfs/rambo/0/zifei/cs221/capital-crunch/ddapp/out/2014-12-02T020412/calibration/investment.is_true.tsv
0.00    0.10    4399    168     4231
0.10    0.20    3727    175     3552
0.20    0.30    1614    104     1510
0.30    0.40    742     74      668
0.40    0.50    8330    694     7636
0.50    0.60    7725    632     7093
0.60    0.70    160     77      83
0.70    0.80    156     112     44
0.80    0.90    277     250     27
0.90    1.00    806     787     19

## AFTER PRUNE:

### Training + Testing

crunchbase=# select count(*) from investment;
 count
-------
 50956
(1 row)

crunchbase=# select count(distinct startup_id) from investment;
 count
-------
 25205
(1 row)

crunchbase=# select count(distinct investor_id) from investment;
 count
-------
   998
(1 row)

crunchbase=# select is_true, count(*) from investment group by is_true;
 is_true | count
---------+-------
 t       |  7749
 f       | 43207
(2 rows)

## Testing 

crunchbase=# select count(*) from investment_is_true_inference;
 count
-------
 12663
(1 row)

crunchbase=# select is_true, count(*) from investment_is_true_inference group by is_true;
 is_true | count
---------+-------
 t       |  1918
 f       | 10745
(2 rows)

