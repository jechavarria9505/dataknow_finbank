<h1 align="center">Infraestructura como Código (IaC)</h1>
<p align="center"><b>Terraform Modular — FinBank Data Platform</b></p>

<br>

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Descripción</b></h2>

Este componente define la infraestructura completa de la plataforma de datos utilizando Terraform, bajo un enfoque modular, desacoplado y orientado a escalabilidad.

El objetivo no es únicamente aprovisionar recursos en Azure, sino establecer una base sólida que permita evolucionar la plataforma sin fricción.

<br>

<b>Este enfoque permite:</b>

* escalar la infraestructura de forma controlada
* mantener el código organizado y mantenible
* reutilizar componentes en distintos entornos
* facilitar el trabajo colaborativo

<br>

En este contexto, la infraestructura deja de ser un conjunto de configuraciones manuales y pasa a ser un activo versionado, reproducible y auditable.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Enfoque arquitectónico</b></h2>

La solución adopta un diseño modular, donde cada servicio de Azure se encapsula en un módulo independiente.

<br>

<p align="center"><b>Principio clave: desacoplamiento por servicio</b></p>

<br>

Esto permite que cada componente evolucione de forma aislada, sin generar impacto en el resto del sistema.

<hr style="border: 1px solid #eee;">

<h3><b>Estructura del proyecto</b></h3>

<pre>
infra/
└── modules/
    ├── adf/
    ├── databricks/
    ├── keyvault/
    ├── sql/
    └── storage/
</pre>

<br>

Cada módulo representa un dominio específico de infraestructura, lo que aporta:

* reducción de acoplamiento
* mayor mantenibilidad
* reutilización en otros proyectos

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Alcance de la infraestructura</b></h2>

A través de los módulos definidos, se despliegan los componentes principales de la plataforma:

* <b>Azure Data Factory</b> → orquestación de pipelines
* <b>Azure Databricks</b> → procesamiento distribuido
* <b>Azure Key Vault</b> → gestión de secretos
* <b>Azure SQL Database</b> → capa de serving
* <b>Azure Storage Account</b> → Data Lake

<br>

En conjunto, estos servicios soportan una arquitectura tipo Medallion (Bronze / Silver / Gold).

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Organización de Terraform</b></h2>

El proyecto sigue una separación clara entre lógica, configuración y estado.

<hr style="border: 1px solid #eee;">

<h3><b>backend.tf</b></h3>

Define el almacenamiento del estado de Terraform.

<br>

<b>Importancia:</b>

* habilita trabajo colaborativo
* evita inconsistencias entre ejecuciones
* permite trazabilidad de cambios

<br>

Sin un backend remoto, Terraform no escala correctamente en equipos.

<hr style="border: 1px solid #eee;">

<h3><b>providers.tf</b></h3>

Centraliza la configuración del provider de Azure (`azurerm`), incluyendo autenticación y suscripción.

<br>

Esto desacopla la infraestructura del entorno de ejecución.

<hr style="border: 1px solid #eee;">

<h3><b>variables.tf</b></h3>

Define las variables de entrada del proyecto.

<br>

Aquí se establece qué elementos son configurables:

* nombres de recursos
* regiones
* configuraciones específicas

<br>

Funciona como la interfaz pública del IaC.

<hr style="border: 1px solid #eee;">

<h3><b>terraform.tfvars</b></h3>

Contiene los valores concretos de las variables.

<br>

Permite:

* manejar múltiples entornos (dev / qa / prod)
* separar configuración del código
* evitar hardcoding

<hr style="border: 1px solid #eee;">

<h3><b>main.tf</b></h3>

Es el punto central donde se integran los módulos.

<br>

<pre>
module "storage" {
  source = "./modules/storage"
}

module "sql" {
  source = "./modules/sql"
}
</pre>

<br>

Aquí se ensamblan todos los componentes en una infraestructura coherente.

<hr style="border: 1px solid #eee;">

<h3><b>outputs.tf</b></h3>

Define los valores expuestos tras el despliegue.

<br>

Ejemplos:

* connection strings
* endpoints
* nombres de recursos

<br>

Permite integrar la infraestructura con otras capas del sistema.

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Flujo de ejecución</b></h2>

El ciclo de despliegue sigue el flujo estándar de Terraform:

<pre>
terraform init
terraform plan
terraform apply
</pre>

<br>

<b>Interpretación del flujo:</b>

* <b>init</b> → prepara el entorno
* <b>plan</b> → valida los cambios antes de ejecutarlos
* <b>apply</b> → aplica los cambios de forma controlada

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Buenas prácticas implementadas</b></h2>

<b>Modularización</b>

* servicios desacoplados por módulo
* evolución independiente de componentes

<b>Separación de responsabilidades</b>

* código → archivos .tf
* configuración → tfvars
* estado → backend remoto

<b>Reutilización</b>

* módulos reutilizables en múltiples entornos

<b>Escalabilidad organizacional</b>

* permite trabajo paralelo entre equipos

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Decisiones técnicas</b></h2>

| Decisión               | Justificación                              |
| ---------------------- | ------------------------------------------ |
| Arquitectura modular   | reduce acoplamiento y mejora mantenimiento |
| Backend remoto         | habilita trabajo en equipo                 |
| Variables externas     | flexibilidad entre entornos                |
| Separación por módulos | diseño limpio y escalable                  |

<hr style="height:2px;border:none;background-color:#eaeaea;">

<h2><b>Conclusión</b></h2>

Esta implementación no solo despliega infraestructura, sino que establece un estándar de trabajo alineado con prácticas reales de ingeniería.

<br>

<b>El valor de este enfoque está en:</b>

* organización clara de la infraestructura
* capacidad de escalar sin reestructuración
* facilidad de mantenimiento
* alineación con entornos productivos

<br>

En conjunto, se construye una base sólida para una plataforma de datos moderna, preparada para evolucionar de forma controlada.


