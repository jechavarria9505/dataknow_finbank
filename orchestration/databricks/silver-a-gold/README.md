<h1 align="center">Capa GOLD</h1>
<p align="center"><b>Modelo Analítico y KPIs — FinBank Data Platform</b></p>

<br>

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Descripción</b></h2>

La capa GOLD representa el nivel analítico del Lakehouse, donde los datos previamente estandarizados en Silver se transforman en estructuras optimizadas para consumo por negocio, BI y analítica avanzada.

En esta capa no solo se modela información, sino que se construyen activos analíticos listos para responder preguntas de negocio.

<br>

<b>El diseño implementa:</b>

* modelo dimensional tipo estrella (Star Schema)
* construcción de KPIs estratégicos
* vista integral del cliente (Customer 360)

<br>

Todo el modelado se gestiona en Unity Catalog, garantizando gobierno, trazabilidad y control sobre los datos.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Organización en Unity Catalog</b></h2>

![catalogo gold](https://github.com/jechavarria9505/dataknow_finbank/blob/691bec6b3e7c781068ffc7e1fbd246d6e3b50561/docs/images/Databricks/catalogo_gold.jpeg)

<br>

<b>Estructura lógica:</b>

* <b>dim</b> → dimensiones del modelo
* <b>fact</b> → tablas de hechos
* <b>kpis</b> → métricas agregadas
* <b>clientes_360</b> → vista analítica integrada

<br>

Todas las tablas se crean como <b>external tables (LOCATION)</b>, lo que permite:

* control directo sobre el almacenamiento en Data Lake
* alineación con arquitectura Medallion
* trazabilidad de rutas físicas
* integración con otros componentes

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Dimensiones</b></h2>

<h3><b>dim_clientes — SCD Tipo 2</b></h3>

Se implementa como Slowly Changing Dimension Tipo 2 para preservar historial de cambios.

<br>

<b>Incluye:</b>

* id_cliente_sk (surrogate key)
* id_cliente (clave de negocio)
* fecha_inicio / fecha_fin
* es_actual
* hash_diff para detección de cambios

<br>

<b>Justificación:</b>

Permite analizar hechos históricos con el contexto correcto del cliente en el tiempo, lo cual es crítico en entornos financieros.

<hr style="border: 1px solid #eee;">

<h3><b>Otras dimensiones</b></h3>

* <b>dim_productos</b> → catálogo financiero
* <b>dim_geografia</b> → ciudad y departamento
* <b>dim_canal</b> → canal digital / físico
* <b>dim_tiempo</b> → calendario completo

<br>

Todas las dimensiones utilizan <b>surrogate keys</b>, lo que:

* mejora el rendimiento en joins
* desacopla el modelo de las claves de negocio

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Tablas de hechos</b></h2>

<h3><b>fact_transacciones</b></h3>

Representa el comportamiento transaccional de los clientes.

<br>

<b>Incluye:</b>

* claves: cliente, producto, canal, tiempo
* métricas: monto, monto_abs

<br>

<b>Features analíticas:</b>

* horario_habil
* transaccion_nocturna
* flag_anomalia

<br>

Se incorpora feature engineering directamente en GOLD para habilitar analítica avanzada sin depender de capas adicionales.

<hr style="border: 1px solid #eee;">

<h3><b>fact_cartera</b></h3>

Modela el estado de las obligaciones financieras.

<br>

<b>Incluye:</b>

* saldo de capital
* días de mora
* bucket de mora
* clasificación regulatoria
* provisiones

<br>

<b>Flags de negocio:</b>

* flag_mora
* flag_alto_riesgo

<br>

Permite análisis crediticio y reporting regulatorio.

<hr style="border: 1px solid #eee;">

<h3><b>fact_rentabilidad_cliente</b></h3>

Modela los ingresos generados por cliente.

<br>

<b>Incluye:</b>

* ingresos por intereses
* ingresos por comisiones
* ingreso total

<br>

<b>Métricas avanzadas:</b>

* CLTV mensual
* CLTV 12 meses

<br>

El CLTV se calcula mediante ventanas analíticas, alineado con prácticas reales de negocio.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>KPIs</b></h2>

<h3><b>KPI Cartera</b></h3>

Agrega información para análisis de riesgo.

<br>

<b>Métricas:</b>

* total de obligaciones
* monto total
* monto en mora
* tasa de mora
* clientes en mora

<br>

Debido a la naturaleza de los datos dummy, algunos grupos presentan valores determinísticos (0 o 1). Esto no es un error del modelo, sino una característica del dataset.

<hr style="border: 1px solid #eee;">

<h3><b>KPI Ejecutivo</b></h3>

Tabla consolidada de una sola fila para visión gerencial.

<br>

<b>Incluye:</b>

* cartera total
* monto en mora
* tasa de mora
* total de transacciones
* ticket promedio
* ratio de transacciones sospechosas
* ingreso promedio por cliente

<br>

<b>Implementación:</b>

* KPIs calculados de forma independiente
* integración mediante <b>cross join</b>

<hr style="border: 1px solid #eee;">

<h3><b>Vista Cliente 360</b></h3>

Vista analítica que centraliza toda la información del cliente.

<br>

<b>Integra:</b>

* comportamiento transaccional
* estado de cartera
* rentabilidad

<br>

<b>Features derivadas:</b>

* tasa de mora por cliente
* ratio de transacciones anómalas
* segmentación de valor
* perfil del cliente

<br>

Centralizar esta información facilita análisis, segmentación y futuros modelos de machine learning.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Conclusión</b></h2>

La capa GOLD es donde el pipeline genera valor de negocio, transformando datos en información analítica de alto nivel.

<br>

<b>El diseño permite:</b>

* análisis eficiente mediante modelo estrella
* métricas alineadas al negocio financiero
* escalabilidad en entornos productivos
* integración directa con herramientas de BI

<br>

En conjunto, esta capa consolida el propósito del Lakehouse: convertir datos en decisiones.



