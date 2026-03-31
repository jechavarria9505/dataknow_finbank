\# Data Platform Governance \& Monitoring Implementation



\## 1. Descripcion



Este documento describe la implementación de capacidades de gobernanza,

control de acceso, monitoreo y alertamiento dentro de una plataforma de

datos en Azure.



El alcance se centra en: - Definición de roles y grupos de acceso -

Aplicación de RBAC - Implementación de controles en Unity Catalog -

Configuración de monitoreo centralizado - Automatización de alertas y

notificaciones



\---



\## 2. Recursos Implementados



\-   Azure Data Factory

\-   Azure Data Lake Storage Gen2

\-   Azure Databricks + Unity Catalog

\-   Log Analytics Workspace

\-   Azure Monitor

\-   Logic App

\-   Microsoft Entra ID



\---



\## 3. Grupos de Seguridad



Se crearon los siguientes grupos:



\-   grp-data-engineers

\-   grp-analysts

\-   grp-admins



<p align="center">

&#x20; <img src="docs/images/Governance/group\_creation.jpeg" width="800"/>

</p>





\---



\## 4. Control de Acceso



\### Storage (ADLS)



\-   Data Engineers: Storage Blob Data Contributor

\-   Analysts: acceso solo a carpeta Gold (Read + Execute)

\-   Admins: Owner



<p align="center">

&#x20; <img src="docs/images/Governance/analyst\_permissions.jpeg" width="800"/>

</p>



<p align="center">

&#x20; <img src="docs/images/Governance/engineer\_admins\_permissions.jpeg" width="800"/>

</p>







\### Data Factory



\-   Data Engineers: Data Factory Contributor

\-   Analysts: sin acceso

\-   Admins: Owner



<p align="center">

&#x20; <img src="docs/images/Governance/permissions\_adf\_group.jpeg" width="800"/>

</p>





\### Log Analytics



\-   Data Engineers: Contributor

\-   Analysts: Reader

\-   Admins: Owner



\---



\## 5. Unity Catalog



Estructura: - bronze - silver - gold



Permisos:



\-   Data Engineers: ALL PRIVILEGES

\-   Analysts: SELECT solo en gold

\-   Admins: ALL PRIVILEGES



<p align="center">

&#x20; <img src="docs/images/Governance/permissions\_UC\_silver\_group.jpeg" width="800"/>

</p>



<p align="center">

&#x20; <img src="docs/images/Governance/permissions\_UC\_group.jpeg" width="800"/>

</p>







\---



\## 6. Mínimo Privilegio



\-   Uso de Managed Identity en ADF

\-   Accesos limitados por servicio

\-   Eliminación de credenciales personales



\---



\## 7. Monitoreo



Logs centralizados en Log Analytics:



\-   Pipeline runs

\-   Activity runs



Query utilizada:



ADFActivityRun \\| where Status == "Failed"



\---



\## 8. Alertas



\-   Azure Monitor basado en logs

\-   Detección de fallos

\-   Evaluación periódica



<p align="center">

&#x20; <img src="docs/images/Governance/alert.jpeg" width="800"/>

</p>





\---



\## 9. Logic App



Flujo:



Alert → Logic App → Email



Contenido del correo: - Pipeline - Activity - Error - Timestamp



<p align="center">

&#x20; <img src="docs/images/Governance/send\_email.jpeg" width="800"/>

</p>





\---



\## 10. Conclusión



Se implementó una solución de gobernanza completa con:



\-   RBAC

\-   Control de acceso por capa

\-   Observabilidad

\-   Alertamiento automático





