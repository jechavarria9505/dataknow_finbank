# Changelog

Todos los cambios relevantes del proyecto son documentados en este archivo siguiendo un enfoque cronológico del desarrollo del pipeline end-to-end.

---

## [0.1.0] - 2026-03-24

### Added

* Inicialización del repositorio del proyecto
* Definición del escenario: **Banca y Servicios Financieros**
* Diseño conceptual del modelo de datos (dimensiones y hechos)
* Estructura base del proyecto:

  * data-generation
  * ingestion
  * processing (bronze, silver, gold)
  * documentation (README, diagrams)

---

## [0.2.0] - 2026-03-26

### Added

* Implementación de infraestructura como código (IaC) con Terraform:

  * Azure Storage Account
  * Azure SQL Database
  * Azure Key Vault
  * Configuración de accesos y seguridad
* Desarrollo del script de generación de datos sintéticos:

  * Clientes, productos, sucursales
  * Movimientos financieros, obligaciones y comisiones
* Generación de datos con:

  * Distribuciones realistas (lognormal, normal)
  * Cobertura temporal de 12 meses
  * Integridad referencial entre tablas
* Exportación en formatos:

  * CSV
  * Parquet
* Implementación del proceso de carga a Azure SQL:

  * Uso de pandas + pyodbc
  * Manejo de credenciales con Azure Key Vault

### Changed

* Ajustes en estructuras de datos para alinearse con modelo relacional
* Optimización de tipos de datos para mejorar compatibilidad con SQL Server

### Fixed

* Problemas iniciales de conexión a Azure SQL (firewall / autenticación)
* Errores en generación de tipos de datos (fechas y numéricos)

---

## [0.3.0] - 2026-03-27

### Added

* Implementación de la capa **Bronze**:

  * Ingesta de datos desde fuentes (CSV/Parquet)
  * Almacenamiento en formato Delta
  * Registro de metadata de ingesta
* Creación de pipeline de ingestión:

  * Orquestación de carga
  * Manejo de cargas FULL e incremental
* Aplicación de particionamiento inicial y optimización de almacenamiento

### Changed

* Ajuste en naming conventions para capas (bronze, silver, gold)
* Mejora en estructura de carpetas y organización de datos

---

## [0.4.0] - 2026-03-29

### Added

* Implementación de la capa **Silver**:

  * Limpieza de datos
  * Tratamiento de nulos
  * Eliminación de duplicados
  * Validación de integridad referencial
  * Manejo de anomalías (fechas fuera de rango, valores negativos)
* Implementación de la capa **Gold**:

  * Modelos analíticos orientados a negocio
  * Cálculo de KPIs:

    * Indicadores de mora
    * Volumen de transacciones
    * Comisiones
    * Segmentación de clientes
* Optimización de consultas:

  * Uso de clustering / optimize
  * Mejora en performance de lectura

### Changed

* Refinamiento de reglas de calidad de datos
* Mejora en transformación de datos para análisis

### Fixed

* Problemas en tratamiento de duplicados en Silver
* Inconsistencias en cálculos agregados en Gold

---

## [1.0.0] - 2026-03-30

### Added

  * Detección de anomalías
  * Validación de reglas de negocio
  * Generación de métricas de calidad

 Automatización de reportes:

  * Resumen de ejecución de pipelines
  * Número de registros procesados
  * Alertas generadas

 Documentación completa del proyecto:
  * README técnico (generación, carga, arquitectura)
  * Explicación de capas Bronze, Silver y Gold
  * Buenas prácticas y decisiones de diseño

### Changed

* Optimización final del pipeline end-to-end
* Ajustes en estructura de documentación para mayor claridad



---
