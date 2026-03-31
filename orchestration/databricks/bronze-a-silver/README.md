\# Capa Silver en Databricks — Diseño, Gobierno y Optimización



\---



\## Descripcion



La capa Silver representa el punto donde los datos dejan de ser simplemente información cruda y pasan a convertirse en activos confiables dentro de la plataforma. En esta etapa no solo realizo transformaciones, sino que establezco un control riguroso sobre calidad, estructura, gobierno y rendimiento.



El objetivo de este diseño fue construir una capa que sea:



\- consistente en términos técnicos  

\- reutilizable para múltiples fuentes  

\- gobernada bajo estándares enterprise  

\- eficiente en lectura y escritura  

\- preparada para escalar sin fricción  



Más que una transformación, esta capa actúa como un filtro crítico que determina qué datos son aptos para avanzar en la arquitectura.



\---



\## Gobierno de datos con Unity Catalog



La implementación se soporta sobre Unity Catalog, lo cual me permite centralizar el gobierno de los datos y mantener control sobre accesos, estructuras y trazabilidad.



<p align="center">

&#x20; <img src="docs/images/databricks/catalogo\_silver.jpeg" width="800"/>

</p>



\### Estructura de schemas



\- silver\_dev.sql\_finbank → almacenamiento de datos curados  

\- silver\_dev.errores\_tables → almacenamiento de registros inválidos  



Ambos schemas fueron definidos como managed locations.



\---



\## Decisión técnica: Managed vs External



A nivel de diseño diferencié claramente el uso de managed schemas y external tables.



\### Managed schemas



Definí los schemas como managed porque:



\- delego la administración del almacenamiento a Unity Catalog  

\- garantizo consistencia en la organización  

\- reduzco la complejidad operativa  

\- centralizo el gobierno del dominio Silver  



\### External tables (LOCATION)



A nivel de tabla utilicé LOCATION explícito porque necesitaba:



\- control directo sobre rutas físicas en el Data Lake  

\- alineación con la estructura Medallion  

\- trazabilidad sobre almacenamiento  

\- integración con otros componentes como ADF  



\### Conclusión de la decisión



Adopté un enfoque híbrido por que me da:



\- gobierno centralizado en el schema  

\- control físico a nivel de tabla  



Esto me permite equilibrar gobernanza con flexibilidad operativa.



\---



\## Diseño del procesamiento



El notebook está completamente parametrizado:



\- table\_name  

\- bronze\_path  

\- load\_type  



Esto elimina la necesidad de duplicar lógica y permite procesar múltiples tablas con un solo flujo.



\---



\## Configuración basada en metadata



En lugar de codificar reglas directamente, implementé una capa de configuración por tabla donde defino:



\- claves primarias  

\- columnas críticas  

\- validaciones  

\- reglas técnicas  

\- relaciones de integridad  

\- columnas sensibles  

\- tipos de datos  



Esta decisión desacopla completamente la lógica del código y facilita la escalabilidad.



\---



\## Flujo de procesamiento



\### Lectura



La estrategia de lectura depende del tipo de carga:



\- FULL → lectura completa  

\- INCREMENTAL → lectura por particiones  



Esto optimiza el uso de recursos y reduce el volumen procesado.



\---



\### Control temprano



Antes de procesar, valido si existen datos. Si no hay información, detengo la ejecución.



Esto evita consumo innecesario de cómputo.



\---



\### Normalización temporal



Estandarizo el concepto de fecha de proceso independientemente del origen.



Esto garantiza consistencia en el modelo temporal.



\---



\### Cacheo



Aplico cache sobre el dataframe para evitar recomputaciones durante validaciones y transformaciones.



\---



\## Validación de calidad



\---



\### Nulos críticos



Los registros con valores nulos en columnas críticas no se eliminan.



En su lugar:



\- se separan del dataset principal  

\- se almacenan en una tabla de errores  



\### Justificación



Decidí no descartar estos datos porque en el contexto bancario incluso la información inválida puede ser relevante para:



\- auditoría  

\- análisis de calidad  

\- investigaciones posteriores  



La tabla de errores permite preservar esta información sin contaminar los datos curados.



\---



\### Validaciones de dominio



Se controlan valores permitidos para evitar inconsistencias semánticas.



\---



\### Integridad referencial



Valido relaciones entre tablas mediante joins con datasets de referencia.



Los registros inválidos se separan como errores.



Esta decisión evita propagar inconsistencias hacia capas superiores.



\---



\### Reglas técnicas



Se aplican controles básicos como validación de valores negativos en campos financieros.



\---



\## Manejo de duplicados



Utilizo funciones de ventana para identificar duplicados y conservar el registro más reciente.



Esta estrategia es determinística y permite mantener control sobre la versión del dato.



\---



\## Enmascaramiento



Se implementa enmascaramiento dinámico en nombre, apellido, numero de documento y numero de cuenta para proteger datos sensibles sin perder completamente su trazabilidad.



\---



\## Feature engineering



En datasets financieros incorporo métricas como:



\- promedio móvil  

\- desviación estándar  

\- z-score  



Esto permite identificar comportamientos atípicos desde etapas tempranas.



\---



\## Métricas de calidad



Se calculan indicadores como:



\- total de registros  

\- registros válidos  

\- registros inválidos  

\- porcentaje de error  



Esto convierte el proceso en un sistema observable.



\---



\## Persistencia en Delta Lake



Se utiliza Delta Lake para garantizar:



\- consistencia ACID  

\- manejo de cargas incrementales  

\- evolución de esquema  



\### Estrategia



\- catálogos → overwrite  

\- transaccionales → merge incremental  



\---



\## Manejo de errores



Los errores se almacenan en un schema independiente dentro de Unity Catalog.



Esto permite:



\- auditoría estructurada  

\- análisis posterior  

\- debugging  

\- preservación de información  



Los errores se tratan como un activo, no como desecho.



\---



\## Optimización con Liquid Clustering



\---



En lugar de particiones, se implementa una estrategia moderna basada en optimización dinámica:



OPTIMIZE tabla

ZORDER BY (columnas\_clave)



Esta estrategia permite:



* reducir la cantidad de archivos pequeños
* mejorar la localización de datos en disco
* optimizar consultas filtradas por columnas clave
* evitar la rigidez del particionamiento tradicional



La optimización se ejecuta únicamente sobre tablas de alto volumen y bajo una lógica controlada, evitando costos innecesarios.

&#x20;



\---



\## Integración



El notebook es ejecutado desde Azure Data Factory, que provee los parámetros necesarios.



Esto permite un flujo completamente orquestado y desacoplado.



\---



\## Conclusión



La capa Silver no es únicamente un paso intermedio, sino el componente donde se define la calidad, el gobierno y el rendimiento de la plataforma.



Las decisiones tomadas permiten construir una solución:



\- escalable  

\- auditable  

\- mantenible  

\- alineada con prácticas reales de producción  



Este diseño asegura que las capas posteriores trabajen sobre una base sólida y confiable.



