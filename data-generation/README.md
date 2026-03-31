<h1 align="center">Generación y Carga de Datos Dummy</h1>
<p align="center"><b>Data Engineering Module — FinBank</b></p>

<br>

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Descripcion</b></h2>

Este módulo implementa un flujo completo de generación de datos sintéticos en el dominio financiero y su posterior carga optimizada hacia Azure SQL Database.

El objetivo no es únicamente generar datos, sino construir un entorno controlado que permita simular condiciones reales de negocio, evaluar rendimiento y validar pipelines de datos en diferentes capas.

<br>

<b>Este componente permite:</b>

* validar pipelines bajo arquitectura Bronze, Silver y Gold
* probar reglas de calidad de datos en escenarios reales
* simular comportamiento financiero con datos controlados
* evaluar rendimiento en cargas de gran volumen

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Arquitectura</b></h2>

<br>

<pre>
Generación (Python)
        │
        ▼
Archivos (CSV / Parquet / JSON)
        │
        ▼
Loader Optimizado (Streaming + Chunking)
        │
        ▼
Azure SQL Database
</pre>

<br>

Este flujo desacopla la generación, persistencia y carga de datos, permitiendo mayor control y escalabilidad.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Generación de Datos</b></h2>

<h3><b>Objetivo</b></h3>

Simular un ecosistema bancario completo mediante datos:

* realistas
* escalables
* con errores controlados
* diseñados para pruebas de calidad y pipelines

<br>

<h3><b>Volumen de datos</b></h3>

| Tabla              | Registros |
| ------------------ | --------- |
| TB_CLIENTES_CORE   | 10,000    |
| TB_PRODUCTOS_CAT   | 50        |
| TB_SUCURSALES_RED  | 200       |
| TB_MOV_FINANCIEROS | 500,000   |
| TB_OBLIGACIONES    | 30,000    |
| TB_COMISIONES_LOG  | 80,000    |

<br>

<h3><b>Modelado</b></h3>

El modelo de datos busca representar un entorno financiero realista:

<b>Clientes</b>

* segmentación (BASICO, ESTANDAR, PREMIUM, ELITE)
* score crediticio
* canal de adquisición

<b>Productos</b>

* crédito, ahorro y transaccional
* tasas y condiciones

<b>Sucursales</b>

* ubicación geográfica
* tipo de punto

<b>Movimientos</b>

* distribución lognormal
* múltiples canales (APP, WEB, CAJERO)
* identificación de dispositivo

<b>Obligaciones</b>

* simulación de créditos
* mora y riesgo

<b>Comisiones</b>

* tipos de cobro
* estado de pago

<hr style="border: 1px solid #eee;">

<h3><b>Distribución temporal</b></h3>

Se implementa una distribución no uniforme para simular comportamiento real:

<pre>
pesos = np.sin(np.linspace(0, 3*np.pi, len(fechas))) + 1.5
</pre>

Esto permite generar:

* picos de actividad
* ciclos financieros
* comportamiento periódico

<hr style="border: 1px solid #eee;">

<h3><b>Inyección de anomalías</b></h3>

Se introducen errores controlados de forma intencional:

* duplicados en movimientos
* valores negativos
* fechas inválidas

<br>

<b>Objetivo:</b>

* validar reglas de negocio
* probar procesos de limpieza
* simular escenarios de fraude

<hr style="border: 1px solid #eee;">

<h3><b>Simulación de datos incompletos</b></h3>

<pre>
apply_nulls(df, pct=0.05)
</pre>

* aproximadamente 5% de valores nulos
* exclusión de identificadores y campos críticos

<br>

Esto permite probar:

* imputación
* validaciones
* calidad de datos

<hr style="border: 1px solid #eee;">

<h3><b>Integridad referencial</b></h3>

<pre>
validar_fk(df, col, ref_df, ref_col)
</pre>

Se valida consistencia entre entidades antes de la carga, evitando propagación de errores.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Persistencia</b></h2>

Los datasets se almacenan en múltiples formatos:

* CSV
* Parquet
* JSON

<br>

Esto permite flexibilidad para distintos tipos de consumo y pruebas.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Carga de Datos</b></h2>

<h3><b>Objetivo</b></h3>

Implementar un proceso de carga eficiente, escalable y seguro hacia Azure SQL Database.

<hr style="border: 1px solid #eee;">

<h3><b>Seguridad</b></h3>

<pre>
password = client.get_secret("sql-password").value
</pre>

Se utiliza Azure Key Vault para:

* evitar hardcoding
* permitir rotación de credenciales
* cumplir estándares de seguridad

<hr style="border: 1px solid #eee;">

<h3><b>Optimización de conexión</b></h3>

<pre>
fast_executemany=True
</pre>

Esta configuración reduce significativamente los tiempos de inserción masiva.

<hr style="border: 1px solid #eee;">

<h3><b>Limpieza previa</b></h3>

Se aplican transformaciones antes de la carga:

* columnas en minúscula
* estandarización de fechas
* conversión de nulos a NULL

<br>

Esto garantiza compatibilidad con el motor SQL.

<hr style="border: 1px solid #eee;">

<h3><b>Estrategia de carga</b></h3>

Se utiliza lectura en streaming:

<pre>
pd.read_csv(path, chunksize=chunksize)
</pre>

<br>

<b>Ventajas:</b>

* menor uso de memoria
* escalabilidad
* estabilidad en grandes volúmenes

<hr style="border: 1px solid #eee;">

<h3><b>Inserción por bloques</b></h3>

Cada chunk es:

* procesado
* limpiado
* insertado
* monitoreado

<br>

Esto permite control granular del proceso.

<hr style="border: 1px solid #eee;">

<h3><b>Configuración de chunk size</b></h3>

| Tipo     | Tamaño  |
| -------- | ------- |
| Pequeñas | 1K – 2K |
| Medianas | 10K     |
| Grandes  | 20K     |

<br>

Balancea:

* memoria
* velocidad
* estabilidad

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Buenas prácticas implementadas</b></h2>

<b>Data Engineering</b>

* separación de responsabilidades
* generación realista de datos
* control de calidad desde origen

<b>Performance</b>

* chunking
* optimización de inserción
* ajuste por volumen

<b>Seguridad</b>

* uso de Key Vault
* eliminación de credenciales en código

<b>Data Quality</b>

* simulación de errores
* validación de integridad
* datos incompletos controlados

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Decisiones técnicas</b></h2>

| Decisión               | Justificación         |
| ---------------------- | --------------------- |
| Faker                  | Generación realista   |
| NumPy                  | Control estadístico   |
| Distribución lognormal | Simulación financiera |
| Chunking               | Escalabilidad         |
| Key Vault              | Seguridad             |
| Anomalías              | Testing de calidad    |
| Multi-formato          | Flexibilidad          |

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Conclusión</b></h2>

Este módulo no solo genera datos, sino que construye un entorno controlado que replica condiciones reales de un sistema financiero.

Permite:

* simular escenarios complejos
* validar pipelines de datos
* probar calidad y consistencia
* evaluar rendimiento en cargas masivas

<br>

En conjunto, establece una base sólida para el desarrollo de soluciones analíticas y de ingeniería de datos en entornos productivos.


