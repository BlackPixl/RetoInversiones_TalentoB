SELECT historico.year, historico.month, historico.id_sistema_cliente, historico.macroactivo, CAST(historico.aba AS FLOAT), riesgo.perfil_riesgo, activos.activo, banca.banca
FROM public.historico_aba_macroactivos historico
INNER JOIN public.cat_perfil_riesgo riesgo ON riesgo.cod_perfil_riesgo = historico.cod_perfil_riesgo
INNER JOIN public.catalogo_activos activos ON activos.cod_activo = historico.cod_activo
INNER JOIN public.catalogo_banca banca ON banca.cod_banca = historico.cod_banca
ORDER BY historico.year ASC, historico.month ASC;