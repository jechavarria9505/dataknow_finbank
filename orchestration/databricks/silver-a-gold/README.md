\### **Capa GOLD – Modelo Analítico y KPIs (Unity Catalog)**



**## Descripcion**



La capa GOLD representa el nivel analítico del Lakehouse, donde los datos previamente estandarizados en Silver se transforman en estructuras optimizadas para consumo por negocio, BI y analítica avanzada. En esta capa se implementa un modelo dimensional tipo estrella (Star Schema), junto con la construcción de KPIs estratégicos y una vista integral del cliente. Todo el modelado se gestiona en Unity Catalog, garantizando gobierno, trazabilidad y control sobre los datos.



\---



**## Organización en Unity Catalog**



<p align="center">

&#x20; <img src="docs/images/databricks/catalogo\_gold.jpeg" width="800"/>

</p>



&#x20;                                   

* dim: dimensiones del modelo
* fact: tablas de hechos
* kpis: métricas agregadas de negocio
* clientes\_360: vista analítica integral



Todas las tablas se crean como external tables usando LOCATION, permitiendo controlar directamente el almacenamiento en Data Lake y evitando rutas gestionadas automáticamente por Unity Catalog.



\---



**## Dimensiones**



**# dim\_clientes**



Esta tabla se implementa como Slowly Changing Dimension Tipo 2 (SCD Tipo 2) para preservar historial de cambios en atributos del cliente. Incluye:



* id\_cliente\_sk (clave surrogate)
* id\_cliente (clave de negocio)
* fecha\_inicio, fecha\_fin
* es\_actual
* hash\_diff para detección de cambios



El uso de SCD2 permite que los hechos históricos se analicen con el contexto correcto del cliente en el tiempo, lo cual es crítico en entornos financieros.



**# Otras dimensiones**

dim\_productos → catálogo de productos financieros

dim\_geografia → ciudad y departamento

dim\_canal → clasificación de canales (digital / físico)

dim\_tiempo → calendario completo



Todas las dimensiones utilizan surrogate keys, lo que mejora el rendimiento en joins y desacopla el modelo de las claves de negocio.



\---



**## Tablas de Hechos**



**## fact\_transacciones**



Contiene el comportamiento transaccional de los clientes.



Incluye:



* claves: id\_cliente\_sk, id\_producto\_sk, id\_canal\_sk, id\_tiempo
* métricas: monto, monto\_abs
* features:

  * horario\_habil
  * transaccion\_nocturna
  * flag\_anomalia



Se incorpora feature engineering directamente en GOLD para habilitar analítica avanzada sin depender de capas adicionales.



**## fact\_cartera:**



Representa el estado de las obligaciones financieras.



Incluye:



* sdo\_capital
* dias\_mora\_act
* bucket\_mora
* clasif\_regulatoria
* provision
* flag\_mora
* flag\_alto\_riesgo



Se modelan métricas regulatorias y de riesgo directamente en la tabla de hechos para facilitar análisis crediticio y reporting.



**## fact\_rentabilidad\_cliente**



Modela los ingresos generados por cliente.



Incluye:



* ingresos\_intereses
* ingresos\_comisiones
* ingreso\_total
* cltv\_mes
* cltv\_12m



El CLTV se calcula mediante ventanas analíticas para capturar el valor acumulado en los últimos 12 meses, alineado con prácticas de negocio.



\---



**## KPIs**



**## KPI Cartera**



Agrega información de cartera para análisis de riesgo.



Métricas:



* total de obligaciones
* monto total
* monto en mora
* tasa de mora
* clientes en mora



Debido a la granularidad del dataset, algunos grupos presentan un único registro esto debido a los datos dummy, lo que genera métricas determinísticas (0 o 1). Esto no es un error del modelo, sino una característica de los datos.





**## KPI Ejecutivo**



Tabla consolidada de una sola fila para visión gerencial.



Incluye:



* cartera\_total
* monto\_mora
* tasa\_mora
* total\_transacciones
* ticket\_promedio
* ratio\_tx\_sospechosas
* ingreso\_promedio\_cliente



**Implementación:**



* KPIs calculados de forma independiente
* Integración mediante crossJoin



**##Vista Cliente 360**



Vista analítica que integra todas las dimensiones del cliente.



Integra:



* comportamiento transaccional
* estado de cartera
* rentabilidad



Features:



* tasa\_mora\_cliente
* ratio\_tx\_anomalas
* segmento\_valor
* perfil\_cliente



Centralizar la información del cliente en una única vista facilita análisis, segmentación y futuros modelos de machine learning.



\---

##### 

\##Conclusión



La capa GOLD consolida el valor del pipeline, transformando datos en activos analíticos de alto nivel. El diseño implementado permite:



* análisis eficiente mediante modelo estrella
* métricas alineadas a negocio financiero
* escalabilidad en entornos productivos
* integración directa con herramientas de BI y analítica avanzada



