\## Generación y Carga de Datos Dummy (Data Engineering)



\---



\## Overview



Este proyecto implementa un flujo completo de \*\*simulación de datos bancarios\*\* y su posterior \*\*carga optimizada en Azure SQL Database\*\*, siguiendo prácticas modernas de ingeniería de datos.



El objetivo es construir un entorno robusto para:



\- Validación de pipelines (Bronze / Silver / Gold)

\- Pruebas de calidad de datos

\- Simulación de escenarios reales del negocio financiero

\- Evaluación de performance en cargas masivas



\---



\## Arquitectura



```

┌──────────────────────────────────────────────┐

│        Generación de Datos (Python)          │

│   Faker + NumPy + Distribuciones reales      │

└─────────────────────────────┬────────────────┘

&#x20;                             │

&#x20;                             ▼

┌──────────────────────────────────────────────┐

│   Archivos Output (CSV / Parquet / JSON)     │

└─────────────────────────────┬────────────────┘

&#x20;                             │

&#x20;                             ▼

┌──────────────────────────────────────────────┐

│   Loader Optimizado (Streaming + Chunking)   │

└─────────────────────────────┬────────────────┘

&#x20;                             │

&#x20;                             ▼

┌──────────────────────────────────────────────┐

│        Azure SQL Database (Serving)          │

└──────────────────────────────────────────────┘

```



\---



\# 1. Generación de Datos Dummy



\## Objetivo



Simular un ecosistema bancario completo con datos:



\- Realistas  

\- Escalables  

\- Con errores controlados  

\- Útiles para testing de pipelines  



\---



\## Volumen de Datos



| Tabla | Registros |

|------|--------|

| TB\_CLIENTES\_CORE | 10,000 |

| TB\_PRODUCTOS\_CAT | 50 |

| TB\_SUCURSALES\_RED | 200 |

| TB\_MOV\_FINANCIEROS | 500,000 |

| TB\_OBLIGACIONES | 30,000 |

| TB\_COMISIONES\_LOG | 80,000 |



\---



\## Modelado de Datos



\### Clientes

\- Segmentación (BASICO, ESTANDAR, PREMIUM, ELITE)

\- Score crediticio (simulación tipo buró)

\- Canal de adquisición



\### Productos

\- Tipos: Crédito, Ahorro, Transaccional

\- Tasas de interés y condiciones



\### Sucursales

\- Ubicación geográfica (latitud/longitud)

\- Tipos de punto físico



\### Movimientos Financieros

\- Distribución realista (lognormal)

\- Diferentes canales (APP, WEB, CAJERO)

\- Identificador de dispositivo



\### Obligaciones

\- Simulación de créditos reales

\- Mora, cuotas, riesgo



\### Comisiones

\- Tipos de cobro

\- Estado de pago



\---



\## Generación Temporal Inteligente



Se usa una distribución no uniforme:



```python

pesos = np.sin(np.linspace(0, 3\*np.pi, len(fechas))) + 1.5

```



Simula comportamiento real:

\- picos de actividad

\- ciclos financieros (quincenas, cierres)



\---



\## Inyección de Anomalías



Se generan errores intencionales para pruebas de calidad:



1\. Duplicados en TB\_MOV\_FINANCIEROS  

2\. Valores negativos en vr\_mov  

3\. Fechas futuras inválidas  



Esto permite validar:

\- reglas de negocio

\- detección de fraude

\- limpieza en Silver Layer



\---



\## Simulación de Datos Sucios



```python

apply\_nulls(df, pct=0.05)

```



\- \~5% de valores nulos

\- Excluye:

&#x20; - IDs

&#x20; - fechas

&#x20; - booleanos



Ideal para:

\- testing de imputación

\- reglas de calidad



\---



\## Validación de Integridad Referencial



```python

validar\_fk(df, col, ref\_df, ref\_col)

```



Ejemplos:

\- `id\_cli` en movimientos

\- `cod\_prod` en obligaciones



Detecta inconsistencias antes de carga



\---



\## Persistencia



Cada dataset se guarda en:



/output  

├── CSV  

├── Parquet  

└── JSON  



Flexibilidad para distintos pipelines



\---



\# 2. Carga de Datos a Azure SQL



\## Objetivo



Cargar datos de forma:



\- Eficiente  

\- Escalable  

\- Segura  



\---



\## Seguridad — Azure Key Vault



```python

password = client.get\_secret("sql-password").value

```



Beneficios:



\- No hardcoding

\- Rotación de credenciales

\- Seguridad enterprise



\---



\## Conexión a SQL Server



```python

engine = sa.create\_engine(

&#x20;   connection\_string,

&#x20;   fast\_executemany=True

)

```



\### Optimización clave:



\- `fast\_executemany=True`



Reduce drásticamente el tiempo de carga



\---



\## Limpieza Pre-Carga



```python

def clean\_df(df):

```



Transformaciones:



\- Columnas → lowercase  

\- Fechas → formato estándar  

\- NaN → NULL  



Garantiza compatibilidad con SQL Server



\---



\## Estrategia de Carga — Streaming



```python

pd.read\_csv(path, chunksize=chunksize)

```



Ventajas:



\- No consume toda la memoria  

\- Escalable a millones de registros  

\- Evita fallos por tamaño  



\---



\## Inserción por Bloques



```python

chunk.to\_sql(..., if\_exists="append")

```



Cada chunk:



\- se limpia  

\- se inserta  

\- se monitorea  



\---



\## Monitoreo



TB\_MOV\_FINANCIEROS: 20000 registros cargados  

COMPLETADA en X segundos  



Permite seguimiento en tiempo real



\---



\## Estrategia de Chunk Size



| Tipo de tabla | Tamaño |

|--------------|--------|

| Pequeñas | 1K – 2K |

| Medianas | 10K |

| Grandes | 20K |



Balance entre:

\- memoria  

\- velocidad  

\- estabilidad  



\---



\## Ejecución



```bash

python load\_data.py

```



Orden:



1\. Clientes  

2\. Productos  

3\. Sucursales  

4\. Movimientos  

5\. Obligaciones  

6\. Comisiones  



\---



\# Buenas Prácticas Implementadas



\## Data Engineering



\- Separación de responsabilidades

\- Datos realistas

\- Control de calidad desde origen



\## Performance



\- Chunking

\- fast\_executemany

\- Ajuste por volumen



\## Seguridad



\- Azure Key Vault

\- Sin credenciales expuestas



\## Data Quality



\- Nulos simulados

\- anomalías controladas

\- validación de integridad



\---



\# Decisiones Técnicas



| Decisión | Justificación |

|--------|-------------|

| Faker | Realismo en datos |

| NumPy | Control estadístico |

| Distribución lognormal | Simulación financiera |

| Chunking | Escalabilidad |

| Key Vault | Seguridad |

| Anomalías | Testing de calidad |

| Multi-formato | Flexibilidad |



\---







\---

\# Conclusión



Este proyecto:



\* Simula un sistema bancario real  

\* Introduce problemas reales de datos  

\* Implementa carga eficiente y segura  

\* Prepara el terreno para analítica avanzada  

