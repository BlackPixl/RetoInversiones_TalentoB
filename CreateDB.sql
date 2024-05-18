-- Database: inversiones

DROP DATABASE IF EXISTS inversiones;

CREATE DATABASE inversiones
    WITH
    OWNER = admin
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE postgres
    IS 'base de datos para informacion de inversiones';