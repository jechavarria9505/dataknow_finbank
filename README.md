<h1 align="center">FinBank Data Platform</h1>
<p align="center"><b>End-to-End Data Engineering Project</b></p>

<p align="center"><b>Escenario A — Banca y Servicios Financieros</b></p>

<br>

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Contexto</b></h2>

Este proyecto nace como respuesta a una prueba técnica de ingeniería de datos, cuyo objetivo era diseñar e implementar un pipeline completo, cubriendo desde la generación de datos hasta su disponibilidad para análisis.

Más allá de cumplir con los requisitos, el enfoque fue construir una solución que reflejara cómo se diseñaría una plataforma de datos en un entorno real.

<br>

<b>El resultado es una implementación end-to-end que integra:</b>

* generación de datos sintéticos
* infraestructura como código
* orquestación de pipelines
* procesamiento distribuido
* gobierno de datos
* monitoreo y observabilidad

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>¿Por qué elegí el escenario financiero?</b></h2>

Seleccioné el <b>Escenario A — Banca y Servicios Financieros</b> de forma intencional.

Este dominio no es el más simple, pero precisamente por eso es uno de los más exigentes y valiosos desde el punto de vista de ingeniería.

<br>

<b>El sector financiero introduce retos clave:</b>

* datos altamente sensibles
* impacto directo de errores en el negocio
* necesidad de trazabilidad
* alta exigencia en calidad de datos
* patrones de uso complejos

<br>

Trabajar sobre este escenario permitió abordar problemas reales como:

* inconsistencias entre fuentes
* registros incompletos
* duplicados
* necesidad de auditoría
* detección de comportamientos atípicos

<br>

<b>Decisión:</b> en lugar de simplificar el problema, se abordó la complejidad para construir una solución más robusta y cercana a un entorno productivo.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Visión de la solución</b></h2>

El pipeline fue diseñado como una plataforma de datos moderna, donde cada componente tiene una responsabilidad clara.

<br>

<p align="center"><b>Generación → Ingesta → Bronze → Silver → Gold → Consumo</b></p>

<br>

Este enfoque permite desacoplar responsabilidades y construir un sistema escalable, mantenible y gobernado.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Arquitectura general</b></h2>

La solución integra múltiples componentes que trabajan de forma coordinada:

* Python para generación de datos
* Base de datos relacional como sistema fuente
* Terraform para aprovisionamiento
* Azure Data Factory para orquestación
* Databricks para procesamiento
* Data Lake organizado por capas
* Unity Catalog para gobierno
* Key Vault para gestión de secretos
* Azure Monitor para alertas

<br>

Cada componente fue seleccionado por su rol dentro de una arquitectura coherente y alineada con prácticas reales.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Generación de datos</b></h2>

Se construyó un modelo sintético que simula operaciones de una entidad financiera.

<br>

<b>Se incorporaron elementos clave:</b>

* relaciones entre entidades
* distribuciones realistas
* valores nulos controlados
* escenarios de error intencionales

<br>

Esto permite validar el comportamiento del pipeline frente a datos imperfectos.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Infraestructura como código</b></h2>

Toda la infraestructura fue definida utilizando Terraform.

<br>

<b>Beneficios del enfoque:</b>

* reproducibilidad del entorno
* consistencia entre despliegues
* facilidad de escalabilidad
* separación entre configuración y lógica

<br>

Se incluyen componentes de almacenamiento, procesamiento, orquestación y gestión de secretos.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Pipeline de datos</b></h2>

<h3><b>Bronze — Punto de entrada</b></h3>

La capa Bronze actúa como la representación fiel de la fuente.

<br>

* mantiene la estructura original
* registra metadata de carga
* soporta ingestas incrementales

<br>

No se realizan transformaciones complejas en esta capa.

<hr style="border: 1px solid #eee;">

<h3><b>Silver — Control de calidad</b></h3>

La capa Silver es el núcleo del sistema.

<br>

Aquí la calidad de datos se trata como una responsabilidad central.

<br>

<b>Incluye:</b>

* validaciones de integridad
* estandarización de datos
* control de duplicados
* verificación de relaciones
* enmascaramiento de datos sensibles

<br>

<b>Decisión clave:</b>

Se implementó una tabla de errores en lugar de eliminar registros inválidos.

<br>

Esto permite:

* auditoría
* trazabilidad
* análisis de calidad
* mejora continua

<br>

Los errores no se descartan, se gestionan.

<hr style="border: 1px solid #eee;">

<h3><b>Gold — Capa analítica</b></h3>

En esta capa los datos se transforman en valor de negocio.

<br>

<b>Se construyen:</b>

* modelos dimensionales
* métricas agregadas
* indicadores clave

<br>

Incluyendo:

* detección de transacciones atípicas
* análisis de comportamiento
* métricas de riesgo
* consolidación de información

<br>

Aquí el dato deja de ser técnico y se convierte en información para decisiones.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Orquestación</b></h2>

El pipeline es controlado mediante Azure Data Factory.

<br>

<b>Se implementó:</b>

* ejecución dinámica por tabla
* dependencias explícitas
* control de errores
* reintentos automáticos

<br>

Garantiza un flujo predecible y controlado.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Monitoreo y observabilidad</b></h2>

Se incorporaron mecanismos de monitoreo desde el diseño.

<br>

* alertas por fallo
* notificaciones por correo
* registro de ejecuciones
* métricas de procesamiento

<br>

El objetivo es contar con un sistema observable y confiable.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Gobierno y seguridad</b></h2>

El acceso a los datos se diseñó bajo un modelo de roles:

* Administrador
* Ingeniero de Datos
* Analista

<br>

Además:

* uso de Unity Catalog para gobierno centralizado
* enmascaramiento de datos sensibles
* gestión segura de credenciales

<br>

El gobierno forma parte del diseño desde el inicio.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Conclusión</b></h2>

Este proyecto no fue abordado como un ejercicio académico, sino como una implementación cercana a un entorno real.

<br>

La elección del dominio financiero permitió trabajar sobre un escenario exigente, donde cada decisión impacta directamente la calidad, trazabilidad y confiabilidad del sistema.

<br>

<b>El valor del proyecto está en:</b>

* cómo se maneja el error
* cómo se garantiza la calidad
* cómo se organiza la arquitectura
* cómo se gobierna el dato

<br>

El resultado es una plataforma que no solo funciona, sino que puede explicarse, mantenerse y evolucionar.


