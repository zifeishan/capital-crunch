DROP TABLE IF EXISTS organization CASCADE;

CREATE TABLE organization (
  crunchbase_uuid TEXT,
  type TEXT,
  name TEXT,
  crunchbase_url TEXT,
  homepage_domain TEXT,
  homepage_url TEXT,
  profile_image_url TEXT,
  facebook_url TEXT,
  twitter_url TEXT,
  linkedin_url TEXT,
  location_city TEXT,
  location_region TEXT,
  location_country_code TEXT,
  short_description TEXT
); 

DROP TABLE IF EXISTS person CASCADE;

CREATE TABLE person (
  crunchbase_uuid TEXT,
  type TEXT,
  first_name TEXT,
  first_name2 TEXT,
  last_name TEXT,
  last_name2 TEXT,
  crunchbase_url TEXT,
  profile_image_url TEXT,
  facebook_url TEXT,
  twitter_url TEXT,
  linkedin_url TEXT,
  location_city TEXT,
  location_region TEXT,
  location_country_code TEXT,
  short_description TEXT
);


---- Load data: 

-- COPY organization FROM 'filepath' CSV;

---- Sample queries:

-- SELECT * FROM organization
-- WHERE
-- crunchbase_uuid is not null and
-- type is not null and
-- name is not null and
-- crunchbase_url is not null and
-- homepage_domain is not null and
-- homepage_url is not null and
-- profile_image_url is not null and
-- facebook_url is not null and
-- twitter_url is not null and
-- linkedin_url is not null and
-- location_city is not null and
-- location_region is not null and
-- location_country_code is not null and
-- short_description is not null;


-- SELECT * FROM organization
-- WHERE 
-- crunchbase_uuid is not null and
-- type is not null and
-- name is not null and
-- homepage_domain is not null and
-- location_city is not null and
-- location_region is not null and
-- location_country_code is not null and
-- short_description is not null;


