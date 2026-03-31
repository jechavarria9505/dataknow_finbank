<h1 align="center">Data Platform Governance & Monitoring</h1>
<p align="center"><b>Seguridad, Control de Acceso y Observabilidad — FinBank</b></p>

<br>

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Descripción</b></h2>

Este documento describe la implementación de capacidades de gobernanza, control de acceso, monitoreo y alertamiento dentro de la plataforma de datos en Azure.

El diseño no se limita a asignar permisos, sino a establecer un modelo de acceso seguro, auditable y alineado con prácticas reales de producción.

<br>

<b>El alcance incluye:</b>

* definición de roles y grupos de acceso
* aplicación de RBAC en servicios Azure
* control de acceso a nivel de datos con Unity Catalog
* monitoreo centralizado de ejecución
* automatización de alertas y notificaciones

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Recursos implementados</b></h2>

La solución integra múltiples servicios que trabajan de forma coordinada:

* Azure Data Factory
* Azure Data Lake Storage Gen2
* Azure Databricks con Unity Catalog
* Log Analytics Workspace
* Azure Monitor
* Logic App
* Microsoft Entra ID

<br>

Cada componente cumple un rol específico dentro del modelo de gobierno y observabilidad.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Grupos de seguridad</b></h2>

Se definieron grupos alineados a responsabilidades dentro del flujo de datos:

* <b>grp-data-engineers</b>
* <b>grp-analysts</b>
* <b>grp-admins</b>

<br>

![creacion de grupos](https://github.com/jechavarria9505/dataknow_finbank/blob/bc72002486b90878830234af2345506e9bcf4423/docs/images/Governance/group_creation.jpeg)

<br>

Este enfoque permite desacoplar identidades de permisos y simplificar la administración de accesos.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Control de acceso</b></h2>

<h3><b>Storage — ADLS Gen2</b></h3>

* Data Engineers → Storage Blob Data Contributor
* Analysts → acceso restringido a capa Gold (lectura)
* Admins → Owner

<br>

![permisos analistas](https://github.com/jechavarria9505/dataknow_finbank/blob/bc72002486b90878830234af2345506e9bcf4423/docs/images/Governance/analyst_permissions.jpeg)

![permisos admins e ing](https://github.com/jechavarria9505/dataknow_finbank/blob/bc72002486b90878830234af2345506e9bcf4423/docs/images/Governance/engineer_admins_permissions.jpeg)>

<br>

Se aplica segmentación por capas para evitar exposición innecesaria de datos.

<hr style="border: 1px solid #eee;">

<h3><b>Azure Data Factory</b></h3>

* Data Engineers → Data Factory Contributor
* Analysts → sin acceso
* Admins → Owner

<br>

![permisos adf](https://github.com/jechavarria9505/dataknow_finbank/blob/bc72002486b90878830234af2345506e9bcf4423/docs/images/Governance/permissions_adf_group.jpeg)

<br>

Esto asegura que únicamente los perfiles operativos puedan modificar pipelines.

<hr style="border: 1px solid #eee;">

<h3><b>Log Analytics</b></h3>

* Data Engineers → Contributor
* Analysts → Reader
* Admins → Owner

<br>

Permite acceso controlado a logs y monitoreo sin comprometer seguridad.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Gobierno de datos — Unity Catalog</b></h2>

Se definió una estructura por capas:

* bronze
* silver
* gold

<br>

<b>Permisos aplicados:</b>

* Data Engineers → ALL PRIVILEGES
* Analysts → SELECT únicamente en capa Gold
* Admins → ALL PRIVILEGES

<br>


![permisos silver](https://github.com/jechavarria9505/dataknow_finbank/blob/bc72002486b90878830234af2345506e9bcf4423/docs/images/Governance/permissions_UC_silver_group.jpeg)

![permisos gold](https://github.com/jechavarria9505/dataknow_finbank/blob/bc72002486b90878830234af2345506e9bcf4423/docs/images/Governance/permissions_UC_group.jpeg)

<br>

Este modelo garantiza que los analistas consuman únicamente datos curados.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Principio de mínimo privilegio</b></h2>

Se implementaron controles orientados a reducir exposición de accesos:

* uso de Managed Identity en Data Factory
* permisos restringidos por servicio
* eliminación de credenciales personales

<br>

Este enfoque minimiza riesgos y mejora la seguridad operativa.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Monitoreo</b></h2>

Se centralizaron logs en Log Analytics, permitiendo visibilidad sobre:

* ejecución de pipelines
* ejecución de actividades
* estados y fallos

<br>

<b>Ejemplo de query:</b>

<pre>
ADFActivityRun | where Status == "Failed"
</pre>

<br>

Esto permite identificar fallos de forma rápida y estructurada.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Alertas</b></h2>

Se implementaron alertas basadas en Azure Monitor:

* detección automática de fallos
* evaluación periódica
* integración con logs

<br>

![alertas](https://github.com/jechavarria9505/dataknow_finbank/blob/bc72002486b90878830234af2345506e9bcf4423/docs/images/Governance/alert.jpeg)

<br>

El objetivo es pasar de un modelo reactivo a uno proactivo.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Automatización — Logic App</b></h2>

Se configuró un flujo de notificación automática:

<br>

<p align="center"><b>Alert → Logic App → Email</b></p>

<br>

<b>El correo incluye:</b>

* nombre del pipeline
* actividad fallida
* descripción del error
* timestamp

<br>

![email enviado](https://github.com/jechavarria9505/dataknow_finbank/blob/bc72002486b90878830234af2345506e9bcf4423/docs/images/Governance/send_email.jpeg)

<br>

Esto reduce el tiempo de respuesta ante incidentes.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Conclusión</b></h2>

Se implementó una solución de gobernanza y monitoreo alineada con prácticas de entornos productivos.

<br>

<b>La solución permite:</b>

* control de acceso basado en roles
* segmentación por capas de datos
* observabilidad completa del pipeline
* detección y notificación automática de fallos

<br>

En conjunto, se establece una plataforma segura, auditable y preparada para operar a escala.





