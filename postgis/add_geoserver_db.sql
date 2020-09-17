/* create the database for the toolbox */


CREATE ROLE geoserver WITH UNENCRYPTED PASSWORD 'geoserver';
ALTER ROLE geoserver WITH LOGIN;
CREATE DATABASE geoserver OWNER 'geoserver';
REVOKE ALL PRIVILEGES ON DATABASE geoserver FROM public;

GRANT ALL PRIVILEGES ON DATABASE geoserver TO geoserver;

ALTER DATABASE geoserver SET search_path = public, postgis;
\c geoserver

CREATE EXTENSION IF NOT EXISTS postgis ;
