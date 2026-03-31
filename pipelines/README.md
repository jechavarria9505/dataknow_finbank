## Pipeline de Ingesta Dinámica



---



## Descripcion



El pipeline **`PL_ingesta`** implementa un patrón de ingestión **dinámico, escalable y orientado a metadata**, diseñado para procesar múltiples tablas desde una fuente transaccional (Azure SQL) hacia un Data Lake bajo una arquitectura **Medallion (Bronze → Silver → Gold)**.



A diferencia de enfoques tradicionales donde cada tabla requiere su propio pipeline este diseño centraliza la lógica en un único flujo reutilizable, gobernado por una tabla de control. Esto permite reducir complejidad operativa, mejorar la mantenibilidad y escalar el sistema sin necesidad de duplicar código.



En esencia, este pipeline actúa como un **motor de ingestión configurable**, donde el comportamiento no está codificado, sino definido por datos.



---



## Arquitectura del Pipeline


![arquitectura pipeline ](https://github.com/jechavarria9505/dataknow_finbank/blob/4d289d7ccc656fdb26299cc8b5d20ed5bf2b9984/docs/images/Pipeline/pipeline_ingesta.jpeg)





---



## Enfoque Arquitectónico



La solución sigue un enfoque moderno basado en tres principios:



- **Metadata-Driven** → El comportamiento se controla desde base de datos  

- **Procesamiento Dinámico** → Un solo pipeline para múltiples tablas  

- **Arquitectura Medallion** → Separación clara por capas  



---



## Flujo General



1. Lectura de configuración desde tabla de control  

2. Iteración dinámica por cada tabla  

3. Validación de datos nuevos  

4. Carga a Bronze (FULL o incremental)  

5. Transformación en Silver (Databricks)  

6. Logging y auditoría  

7. Actualización de watermark  

8. Procesamiento final en Gold  



---



## Detalle del Pipeline



### Lookup — Configuración



Obtiene las tablas activas a procesar:



- tabla  

- tipo de carga  

- watermark  

- configuración  



---



### ForEach — Ejecución dinámica



Permite procesar múltiples tablas usando el mismo flujo.



---



### Validación



Evalúa si existen datos nuevos antes de ejecutar la carga.



---



### Copy a Bronze



- FULL → sobrescribe  

- INCREMENTAL → particiona por fecha  



Formato: **Parquet**



---



### Procesamiento Silver



Notebook en Databricks que:



- limpia datos  

- valida  

- transforma  



---



### Logging



Registra:



- SUCCESS  

- ERROR  

- NO_DATA  



Incluye métricas y timestamps.



---



### Watermark



Actualiza el último valor procesado para cargas incrementales.



---



### Gold Layer



Notebook final que construye modelos analíticos.



---



## Variables



| Variable | Descripción |

|--------|------------|

| start_time | inicio ejecución |

| end_time | fin ejecución |

| records_count | registros procesados |



---



## Características Clave



- Diseño escalable  

- Alta parametrización  

- Soporte FULL + incremental  

- Auditoría completa  

- Integración end-to-end  



---



## Conclusión



Este pipeline representa un diseño **robusto, reutilizable y alineado con prácticas reales de Data Engineering**, permitiendo construir una plataforma de datos moderna, gobernada y escalable.

