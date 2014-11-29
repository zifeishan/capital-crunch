Data to crawl
====

## Data model

Startup(startupId, [attributes])
Investor(investorId, [attributes])
Investment(investorId, startupId, isTrue)

Updates:

- oranization types:
  - company
  - investor
  - school
  - group

In parsed list:
- 214195 organizations
- 286658 people



----

crunchbase=# select count(distinct startup_id) from startup_feature ;
 count
-------
  4032
(1 row)
crunchbase=# select count(distinct startup_id) from startup ;
 count
-------
 12094
(1 row)

crunchbase=# select count(distinct investor_id) from investor_feature ;
 count
-------
   998
(1 row)

crunchbase=# select count(distinct investor_id) from investor ;
 count
-------
   998
(1 row)


3.4M variables
43M factors

ampler] INFO  # nvar                          : 3602283
03:47:38 [sampler] INFO  # nfac               : 78082173
03:47:38 [sampler] INFO  # nweight            : 1449845
03:47:38 [sampler] INFO  # nedge              : 78082173