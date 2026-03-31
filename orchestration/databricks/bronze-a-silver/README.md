<h1 align="center">Capa Silver en Databricks</h1>
<p align="center"><b>Diseño, Gobierno y Optimización — FinBank Data Platform</b></p>

<br>

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Descripción</b></h2>

La capa Silver representa el punto donde los datos dejan de ser información cruda y pasan a convertirse en activos confiables dentro de la plataforma.

En esta etapa no solo se realizan transformaciones, sino que se establece un control riguroso sobre calidad, estructura, gobierno y rendimiento.

<br>

<b>Objetivo del diseño:</b>

* consistencia técnica
* reutilización para múltiples fuentes
* gobierno bajo estándares enterprise
* eficiencia en lectura y escritura
* capacidad de escalar sin fricción

<br>

Más que una transformación, esta capa actúa como un filtro crítico que determina qué datos pueden avanzar en la arquitectura.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Gobierno de datos — Unity Catalog</b></h2>

La implementación se soporta sobre Unity Catalog, permitiendo centralizar el control de accesos, la organización y la trazabilidad de los datos.

<br>

![catalogo silver](https://github.com/jechavarria9505/dataknow_finbank/blob/691bec6b3e7c781068ffc7e1fbd246d6e3b50561/docs/images/Databricks/catalogo_silver.jpeg)

<br>

<h3><b>Estructura de schemas</b></h3>

* silver_dev.sql_finbank → datos curados
* silver_dev.errores_tables → registros inválidos

<br>

Ambos schemas fueron definidos como <b>managed locations</b>.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Decisión técnica: Managed vs External</b></h2>

El diseño diferencia claramente entre gestión a nivel de schema y a nivel de tabla.

<br>

<h3><b>Managed schemas</b></h3>

Se utilizan porque permiten:

* delegar la administración del almacenamiento a Unity Catalog
* garantizar consistencia en la organización
* simplificar la operación
* centralizar el gobierno del dominio

<br>

<h3><b>External tables (LOCATION)</b></h3>

A nivel de tabla se define LOCATION explícito para:

* controlar rutas físicas en el Data Lake
* mantener alineación con arquitectura Medallion
* facilitar integración con ADF
* asegurar trazabilidad del almacenamiento

<br>

<h3><b>Conclusión</b></h3>

Se adopta un enfoque híbrido que combina:

* gobierno centralizado
* control físico del almacenamiento

Esto permite equilibrar control y flexibilidad.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Diseño del procesamiento</b></h2>

El notebook está completamente parametrizado:

* table_name
* bronze_path
* load_type

<br>

Esto permite procesar múltiples tablas con un solo flujo, eliminando duplicación de lógica.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Configuración basada en metadata</b></h2>

Las reglas no están hardcodeadas, sino definidas en configuración por tabla:

* claves primarias
* columnas críticas
* validaciones
* reglas técnicas
* relaciones de integridad
* columnas sensibles
* tipos de datos

<br>

Esta decisión desacopla la lógica del código y facilita la escalabilidad.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Flujo de procesamiento</b></h2>

<h3><b>Lectura</b></h3>

* FULL → lectura completa
* INCREMENTAL → lectura por particiones

<br>

Optimiza recursos y reduce volumen procesado.

<hr style="border: 1px solid #eee;">

<h3><b>Control temprano</b></h3>

Si no hay datos, el proceso se detiene.

<br>

Evita consumo innecesario de cómputo.

<hr style="border: 1px solid #eee;">

<h3><b>Normalización temporal</b></h3>

Se unifica el concepto de fecha de proceso independientemente del origen.

<hr style="border: 1px solid #eee;">

<h3><b>Cacheo</b></h3>

Se aplica cache para evitar recomputaciones durante validaciones y transformaciones.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Validación de calidad</b></h2>

<h3><b>Nulos críticos</b></h3>

Los registros inválidos no se eliminan, se separan y almacenan en tablas de errores.

<br>

<b>Justificación:</b>

En el contexto financiero, incluso los datos incorrectos pueden ser relevantes para:

* auditoría
* análisis de calidad
* investigaciones

<br>

Los errores se preservan sin contaminar los datos curados.

<hr style="border: 1px solid #eee;">

<h3><b>Validaciones de dominio</b></h3>

Se controlan valores permitidos para evitar inconsistencias semánticas.

<hr style="border: 1px solid #eee;">

<h3><b>Integridad referencial</b></h3>

Se validan relaciones entre tablas mediante joins.

<br>

Los registros inválidos se separan como errores.

<hr style="border: 1px solid #eee;">

<h3><b>Reglas técnicas</b></h3>

Se aplican controles como validación de valores negativos en campos financieros.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Manejo de duplicados</b></h2>

Se utilizan funciones de ventana para conservar el registro más reciente de forma determinística.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Enmascaramiento</b></h2>

Se implementa masking en:

* nombre
* apellido
* documento
* cuenta

<br>

Protege datos sensibles manteniendo trazabilidad parcial.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Feature engineering</b></h2>

Se incorporan métricas como:

* promedio móvil
* desviación estándar
* z-score

<br>

Permiten detectar comportamientos atípicos desde etapas tempranas.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Métricas de calidad</b></h2>

Se calculan indicadores como:

* total de registros
* válidos
* inválidos
* porcentaje de error

<br>

Esto convierte el proceso en un sistema observable.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Persistencia en Delta Lake</b></h2>

Se utiliza Delta Lake para garantizar:

* consistencia ACID
* cargas incrementales
* evolución de esquema

<br>

<b>Estrategia:</b>

* catálogos → overwrite
* transaccionales → merge

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Manejo de errores</b></h2>

Los errores se almacenan en un schema independiente.

<br>

Esto permite:

* auditoría
* análisis
* debugging
* trazabilidad

<br>

Los errores se gestionan como información, no como desecho.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Optimización — Liquid Clustering</b></h2>

Se implementa optimización basada en:

<pre>
OPTIMIZE tabla
ZORDER BY (columnas_clave)
</pre>

<br>

<b>Beneficios:</b>

* reducción de archivos pequeños
* mejor localización de datos
* optimización de consultas
* mayor flexibilidad que particiones tradicionales

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Integración</b></h2>

El notebook es ejecutado desde Azure Data Factory, lo que permite un flujo completamente orquestado.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Conclusión</b></h2>

La capa Silver es el punto donde se define la calidad, el gobierno y el rendimiento de la plataforma.

<br>

<b>Este diseño permite construir una solución:</b>

* escalable
* auditable
* mantenible
* alineada con prácticas reales de producción

<br>

Garantiza que las capas posteriores trabajen sobre una base sólida y confiable.



