-- reparar casos donde los valores estan corridos un espacio a la izquierda.
UPDATE staging_hist_aba_macroactivos
SET
    month = year,
    year = cod_banca,
    cod_banca = cod_perfil_riesgo,
    cod_perfil_riesgo = aba,
    aba = cod_activo,
    cod_activo = macroactivo,
    macroactivo = SUBSTRING(id_sistema_cliente FROM 4),
    id_sistema_cliente = LEFT(id_sistema_cliente, 3)||ingestion_day,
    ingestion_day = NULL
WHERE
    LENGTH(id_sistema_cliente) > 3
    AND SUBSTRING(id_sistema_cliente, 1, 3) ~ '^\d+$'
    AND SUBSTRING(id_sistema_cliente, 4) ~ '^[A-Za-z ]+$';

-- reparar los codigos de activo cuando tienen un cero de más.
UPDATE staging_hist_aba_macroactivos
SET
    cod_activo = '1007'
WHERE
    cod_activo = '10007'
    OR cod_activo = '10007.0';

-- crear una nueva entrada en catalogo_activos para observaciónes sin activos.
INSERT INTO catalogo_activos(activo, cod_activo)
VALUES ('SIN ACTIVO', 9999);

-- actualizar entradas donde cod_activo es nulo
UPDATE staging_hist_aba_macroactivos
SET cod_activo = '9999'
WHERE cod_activo IS NULL;

-- agregar información faltante en ingestion month.
UPDATE staging_hist_aba_macroactivos
SET ingestion_month = month
WHERE ingestion_month IS NULL;

-- borrar observaciones donde aba = NULL, ya que no se puede inferir que valor peude ser. NULL != en terminos de dinero.
DELETE FROM staging_hist_aba_macroactivos
WHERE aba IS NULL;

-- reparar observacio con valores corridos a la derecha.
UPDATE staging_hist_aba_macroactivos
SET
    macroactivo = cod_activo,
    cod_activo = aba,
    aba = cod_perfil_riesgo,
    cod_perfil_riesgo = cod_banca,
    cod_banca = year,
    year = month,   
    month = ingestion_month
WHERE
    macroactivo IS NULL
    AND cod_activo = 'Renta Variable';

-- reparar observacion con cod_perfil_riesgo corrido a la derecha.
UPDATE staging_hist_aba_macroactivos
SET
    cod_perfil_riesgo = cod_banca
WHERE
    cod_perfil_riesgo IS NULL
    AND cod_banca NOT IN (SELECT cod_banca from catalogo_banca);

-- se puede asumir que observaciones con cod_perfil_riesgo=NULL es porque no tienen perfil de riesgo.
UPDATE staging_hist_aba_macroactivos
SET
    cod_perfil_riesgo = '1466'
WHERE
    cod_perfil_riesgo IS NULL;

-- reparar observacion cuando id_sistema_cliente esta separado
UPDATE staging_hist_aba_macroactivos
SET
    id_sistema_cliente = id_sistema_cliente || macroactivo,
    macroactivo = cod_activo,
    cod_activo = aba,
    aba = cod_perfil_riesgo,
    cod_perfil_riesgo = cod_banca,
    cod_banca = year,
    year = month,
    month = ingestion_month
WHERE cod_banca NOT IN (SELECT cod_banca from catalogo_banca)
    AND id_sistema_cliente = '100';

-- reparar observaicones corridas a la derecha.
UPDATE staging_hist_aba_macroactivos
SET
    id_sistema_cliente = macroactivo,
    macroactivo = cod_activo,
    cod_activo = aba,
    aba = cod_perfil_riesgo,
    cod_perfil_riesgo = cod_banca,
    cod_banca = year,
    year = month,
    month = ingestion_month
WHERE cod_banca NOT IN (SELECT cod_banca from catalogo_banca)
    AND id_sistema_cliente IS NULL;

-- 
UPDATE staging_hist_aba_macroactivos
SET
    year = cod_banca,
    cod_banca = cod_perfil_riesgo,
    cod_perfil_riesgo = '1466'
WHERE cod_banca NOT IN (SELECT cod_banca from catalogo_banca)
    AND year IS NULL;

UPDATE staging_hist_aba_macroactivos
SET
    cod_perfil_riesgo = cod_banca,
    cod_banca = year,
    year = ingestion_year
WHERE cod_banca NOT IN (SELECT cod_banca from catalogo_banca)
    AND year = 'PN';

-- actualizar datos con punto decimal:
UPDATE staging_hist_aba_macroactivos
SET cod_perfil_riesgo = 
    CASE
        WHEN position('.' IN cod_perfil_riesgo) > 0 THEN 
            substring(cod_perfil_riesgo FROM 1 FOR position('.' IN cod_perfil_riesgo) - 1)
        ELSE cod_perfil_riesgo
    END,
    cod_activo = 
    CASE
        WHEN position('.' IN cod_activo) > 0 THEN 
            substring(cod_activo FROM 1 FOR position('.' IN cod_activo) - 1)
        ELSE cod_activo
    END
WHERE cod_perfil_riesgo NOT IN (SELECT CAST(cod_perfil_riesgo AS VARCHAR(255)) from cat_perfil_riesgo)
    OR cod_activo NOT IN (SELECT CAST(cod_activo AS VARCHAR(255)) from catalogo_activos);
    
-- para no perder informacion se guardan los activos que no existen en la tabla public.catalogo_activos_pkey
INSERT INTO catalogo_activos (cod_activo, activo)
SELECT
    CAST(cod_activo AS INT),
    'ACTIVO_DESCONOCIDO'
FROM (
    SELECT DISTINCT cod_activo
    FROM staging_hist_aba_macroactivos
    WHERE cod_activo NOT IN (SELECT CAST(cod_activo AS VARCHAR(255)) from catalogo_activos));
    
INSERT INTO catalogo_banca (cod_banca, banca)
VALUES('XX', 'BANCA_DESCONOCIDA');

UPDATE staging_hist_aba_macroactivos
SET
    cod_banca = 'XX'
WHERE cod_banca IS NULL;


UPDATE staging_hist_aba_macroactivos
SET month = 
    CASE
        WHEN position('.' IN month) > 0 THEN 
            substring(month FROM 1 FOR position('.' IN month) - 1)
        ELSE month
    END,
    ingestion_day = 
    CASE
        WHEN position('.' IN ingestion_day) > 0 THEN 
            substring(ingestion_day FROM 1 FOR position('.' IN ingestion_day) - 1)
        ELSE ingestion_day
    END,
    ingestion_month = 
    CASE
        WHEN position('.' IN ingestion_month) > 0 THEN 
            substring(ingestion_month FROM 1 FOR position('.' IN ingestion_month) - 1)
        ELSE ingestion_month
    END,
    year = 
    CASE
        WHEN position('.' IN year) > 0 THEN 
            substring(year FROM 1 FOR position('.' IN year) - 1)
        ELSE year
    END;

DELETE FROM staging_hist_aba_macroactivos
WHERE id_sistema_cliente = '100';

INSERT INTO public.historico_aba_macroactivos (ingestion_year, ingestion_month, ingestion_day, id_sistema_cliente, macroactivo, cod_activo, aba, cod_perfil_riesgo, cod_banca, year, month)
SELECT CAST(ingestion_year AS INTEGER), CAST(ingestion_month AS INTEGER), CAST(ingestion_day AS INTEGER), id_sistema_cliente, macroactivo, CAST(cod_activo AS INTEGER), aba, CAST(cod_perfil_riesgo AS INTEGER), cod_banca, CAST(year AS INTEGER), CAST(month AS INTEGER)
FROM public.staging_hist_aba_macroactivos;