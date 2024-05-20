# RetoInversiones_TalentoB
Repositorio para la prueba técnica de analítica de inversiones bajo el programa Talento B.

## Características

- Cargue de datos.
- Limpieza de datos.
- Visualización de datos.

## Instalación

```bash
# Clona el repositorio
git clone https://github.com/usuario/nombre-del-proyecto.git

# Entra en el directorio del proyecto
cd nombre-del-proyecto

# Inicia el servidor postgres
docker compose up

```
Luego de iniciar el servidor deberás ejecutar el script create_db el cual es encargado de crear la base de datos donde se guardará la información.

```bash

# Ejecuta el pipeline (solo linux)
bash pipeline.sh

# Ejecuta la app
python3 porfolio.py
```

Ahora puedes ingresar a [localhost:8050](http://localhost:8050/) y visualizar el dashboard.

## Respuestas a Preguntas formuladas.

### Conclusiones Tecnicas.
- Es increíblemente necesario la integrración de datos de multiples fuentes y la epxlotación de la informacioń para obtener ventaja en las actividades de la compañía.
- Las gráficas facilitan exponencialmente la visualización de los datos.
- Los datos financieros son dinámicos y cambian constantemente, es crucial establecer un sistema de actualización automática que garantice que las visualizacionessiempre estén actualizadas.
- La limpieza de los datos depende mucho del objetivo para el que se quieran utilizar. Es importante rescatar la mayor cantidad de datos posible.

### Conclusiones de Negocio.

- Es prioridad una visión integral y consolidada de los portafolios de inversión de sus clientes, permitiéndoles identificar fácilmente la distribución de activos y macroactivos y tomar decisiones informadas para optimizar las inversiones.

- El análisis visua reduce significativamente el tiempo que los gerentes deben invertir para identificar estrategias en los portafolios de sus clientes.

- Con datos accesibles y bien organizados, los gerentes pueden tomar decisiones más rápidas y basadas en datos concretos, minimizando el riesgo de errores.