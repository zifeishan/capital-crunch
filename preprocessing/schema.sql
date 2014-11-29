
DROP TABLE IF EXISTS investor CASCADE;

CREATE TABLE investor (
  investor_id text
);

DROP TABLE IF EXISTS startup CASCADE;

CREATE TABLE startup (
  startup_id text
);

DROP TABLE IF EXISTS organization_path CASCADE;

CREATE TABLE organization_path (
  org_id text,
  path text
);

DROP TABLE IF EXISTS known_investment CASCADE;

CREATE TABLE known_investment (
  investor_id text,
  startup_id text
);


DROP TABLE IF EXISTS investment CASCADE;

CREATE TABLE investment (
  investor_id text,
  startup_id text,
  is_true boolean,
  id bigint
);

DROP TABLE IF EXISTS startup_feature CASCADE;

CREATE TABLE startup_feature (
  startup_id text,
  type text,
  feature text,
  value real
);

DROP TABLE IF EXISTS investor_feature CASCADE;

CREATE TABLE investor_feature (
  investor_id text,
  type text,
  feature text,
  value real
);

DROP TABLE IF EXISTS description CASCADE;

CREATE TABLE description (
  org_id text,
  description text
);

DROP TABLE IF EXISTS sentences CASCADE;

CREATE TABLE sentences (
  document_id text,      -- document id
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
