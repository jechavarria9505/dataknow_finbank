<h1 align="center">Pipeline de Ingesta Dinámica</h1>
<p align="center"><b>Orquestación y Procesamiento End-to-End — FinBank Data Platform</b></p>

<br>

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Descripción</b></h2>

El pipeline <b>PL_ingesta</b> implementa un patrón de ingestión dinámico, escalable y orientado a metadata, diseñado para procesar múltiples tablas desde una fuente transaccional (Azure SQL) hacia un Data Lake bajo una arquitectura Medallion (Bronze → Silver → Gold).

<br>

A diferencia de enfoques tradicionales donde cada tabla requiere su propio pipeline, este diseño centraliza la lógica en un único flujo reutilizable, gobernado por una tabla de control.

<br>

<b>Esto permite:</b>

* reducir complejidad operativa
* evitar duplicación de pipelines
* mejorar mantenibilidad
* escalar el sistema de forma controlada

<br>

En esencia, el pipeline actúa como un <b>motor de ingestión configurable</b>, donde el comportamiento no está codificado, sino definido por datos.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Arquitectura del pipeline</b></h2>

![arquitectura pipeline](https://github.com/jechavarria9505/dataknow_finbank/blob/ec643dc763a3c6098249f4dce5a3ddc0b1e276e6/docs/images/Pipeline/pipeline_ingesta.jpeg)
![arquitectura pipeline2](https://github.com/jechavarria9505/dataknow_finbank/blob/b4bf10d2a65e66a51f6063ced3c7e291961e01a2/docs/images/Pipeline/pipeline_2.jpeg)
![arquitectura pipeline3](https://github.com/jechavarria9505/dataknow_finbank/blob/b4bf10d2a65e66a51f6063ced3c7e291961e01a2/docs/images/Pipeline/pipeline_3.jpeg)

<br>

Este flujo integra ingesta, transformación y procesamiento analítico en un pipeline orquestado de extremo a extremo.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Enfoque arquitectónico</b></h2>

La solución se basa en tres principios clave:

<br>

<b>Metadata-Driven</b>
El comportamiento del pipeline se define desde una tabla de control, eliminando lógica hardcodeada.

<br>

<b>Procesamiento dinámico</b>
Un único pipeline es capaz de procesar múltiples tablas con diferentes configuraciones.

<br>

<b>Arquitectura Medallion</b>
Se garantiza separación clara entre Bronze, Silver y Gold.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Flujo general</b></h2>

El pipeline sigue un proceso secuencial claramente definido:

<br>

1. lectura de configuración desde tabla de control
2. iteración dinámica por cada tabla
3. validación de existencia de datos nuevos
4. carga a Bronze (FULL o incremental)
5. transformación en Silver (Databricks)
6. logging y auditoría
7. actualización de watermark
8. procesamiento final en Gold

<br>

Este flujo asegura control completo del ciclo de vida del dato.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Detalle del pipeline</b></h2>

<h3><b>Lookup — Configuración</b></h3>

Obtiene las tablas activas desde la tabla de control, incluyendo:

* nombre de tabla
* tipo de carga
* watermark
* configuración adicional

<br>

Este paso habilita el comportamiento dinámico del pipeline.

<hr style="border: 1px solid #eee;">

<h3><b>ForEach — Ejecución dinámica</b></h3>

Permite iterar sobre múltiples tablas utilizando un único flujo de procesamiento.

<br>

El pipeline se adapta a cada tabla sin necesidad de duplicación.

<hr style="border: 1px solid #eee;">

<h3><b>Validación de datos</b></h3>

Evalúa si existen registros nuevos antes de ejecutar la carga.

<br>

Evita ejecuciones innecesarias y optimiza el uso de recursos.

<hr style="border: 1px solid #eee;">

<h3><b>Carga a Bronze</b></h3>

Se implementan dos estrategias:

* <b>FULL</b> → sobrescribe datos
* <b>INCREMENTAL</b> → carga por particiones

<br>

<b>Formato:</b> Parquet

<br>

Se prioriza eficiencia en almacenamiento y lectura.

<hr style="border: 1px solid #eee;">

<h3><b>Procesamiento en Silver</b></h3>

Se ejecuta un notebook en Databricks que:

* limpia datos
* valida calidad
* aplica transformaciones

<br>

Este paso garantiza consistencia antes de avanzar a capas analíticas.

<hr style="border: 1px solid #eee;">

<h3><b>Logging y auditoría</b></h3>

Se registra el estado de ejecución:

* SUCCESS
* ERROR
* NO_DATA

<br>

Incluye:

* timestamps
* número de registros
* tipo de carga

<br>

Esto permite trazabilidad completa del pipeline.

<hr style="border: 1px solid #eee;">

<h3><b>Watermark</b></h3>

Se actualiza el valor máximo procesado para soportar cargas incrementales.

<br>

Evita reprocesamiento y garantiza continuidad.

<hr style="border: 1px solid #eee;">

<h3><b>Procesamiento en Gold</b></h3>

Se ejecuta un notebook final que construye:

* modelo analítico
* KPIs
* vistas de negocio

<br>

Completa el flujo end-to-end.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Variables del pipeline</b></h2>

| Variable      | Descripción          |
| ------------- | -------------------- |
| start_time    | inicio de ejecución  |
| end_time      | fin de ejecución     |
| records_count | registros procesados |

<br>

Permiten monitorear ejecución y medir desempeño.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Características clave</b></h2>

* diseño completamente escalable
* parametrización avanzada
* soporte para cargas FULL e incremental
* trazabilidad y auditoría completa
* integración end-to-end entre capas

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Conclusión</b></h2>

Este pipeline representa un diseño moderno de orquestación de datos, donde la lógica se desacopla del código y se controla mediante metadata.

<br>

<b>El resultado es una solución:</b>

* reutilizable
* mantenible
* escalable
* alineada con prácticas reales de Data Engineering

<br>

En conjunto, actúa como el eje central de la plataforma, conectando ingesta, procesamiento y analítica en un flujo coherente y controlado.

