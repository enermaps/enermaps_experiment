

CREATE ROLE app WITH UNENCRYPTED PASSWORD 'app';
ALTER ROLE app WITH LOGIN;
CREATE DATABASE app OWNER 'app';
REVOKE ALL PRIVILEGES ON DATABASE app FROM public;

GRANT ALL PRIVILEGES ON DATABASE app TO app;

\c app
CREATE SCHEMA IF NOT EXISTS stat AUTHORIZATION app;
CREATE SCHEMA IF NOT EXISTS geo AUTHORIZATION app;
CREATE SCHEMA IF NOT EXISTS "user" AUTHORIZATION app;
