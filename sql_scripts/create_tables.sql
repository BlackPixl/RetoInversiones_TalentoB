-- Table: catalogo_activos
CREATE TABLE IF NOT EXISTS catalogo_activos (
    activo VARCHAR(255),
    cod_activo SERIAL PRIMARY KEY
);

-- Table: catalogo_banca
CREATE TABLE IF NOT EXISTS catalogo_banca (
    cod_banca VARCHAR(255) PRIMARY KEY,
    banca VARCHAR(255)
);

-- Table: cat_perfil_riesgo
CREATE TABLE IF NOT EXISTS cat_perfil_riesgo (
    cod_perfil_riesgo SERIAL PRIMARY KEY,
    perfil_riesgo VARCHAR(255)
);

-- Table: hisorico_aba_macroactivos
CREATE TABLE IF NOT EXISTS historico_aba_macroactivos (
    ingestion_year INT,
    ingestion_month INT,
    ingestion_day INT,
    id_sistema_cliente VARCHAR(255),
    macroactivo VARCHAR(255),
    cod_activo INT,
    aba VARCHAR(255),
    cod_perfil_riesgo INT,
    cod_banca VARCHAR(255),
    year INT,
    month INT,
    FOREIGN KEY (cod_activo) REFERENCES catalogo_activos (cod_activo),
    FOREIGN KEY (cod_perfil_riesgo) REFERENCES cat_perfil_riesgo (cod_perfil_riesgo),
    FOREIGN KEY (cod_banca) REFERENCES catalogo_banca (cod_banca)
);

-- crear tabla para staging
DROP TABLE IF EXISTS staging_hist_aba_macroactivos;

CREATE TABLE staging_hist_aba_macroactivos (
    ingestion_year VARCHAR(255),
    ingestion_month VARCHAR(255),
    ingestion_day VARCHAR(255),
    id_sistema_cliente VARCHAR(255),
    macroactivo VARCHAR(255),
    cod_activo VARCHAR(255),
    aba VARCHAR(255),
    cod_perfil_riesgo VARCHAR(255),
    cod_banca VARCHAR(255),
    year VARCHAR(255),
    month VARCHAR(255)
);
