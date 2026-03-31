\# Infraestructura como Código IaC (Terraform Modular)



\## Descripcion



Este componente del proyecto define la \*\*infraestructura completa de la plataforma de datos\*\* utilizando \*\*Terraform\*\*, siguiendo un enfoque \*\*modular, desacoplado y escalable\*\*.



El objetivo no es solo aprovisionar recursos en Azure, sino construir una base sólida que permita:



\- Escalar la plataforma sin fricción  

\- Mantener el código de infraestructura organizado  

\- Reutilizar componentes en múltiples entornos  

\- Facilitar el trabajo colaborativo entre equipos  



En otras palabras, esta capa convierte la infraestructura en un \*\*activo versionado, reproducible y mantenible\*\*.



\---



\## Enfoque Arquitectónico



La solución adopta un diseño \*\*modular\*\*, donde cada servicio de Azure es encapsulado en su propio módulo independiente.



Esto permite que cada componente evolucione de forma aislada, sin impactar el resto del sistema.



\### Estructura del proyecto



infra/

└── modules/

&#x20;   ├── adf/

&#x20;   ├── databricks/

&#x20;   ├── keyvault/

&#x20;   ├── sql/

&#x20;   └── storage/



Cada carpeta representa un dominio de infraestructura específico, lo cual:



\* Reduce el acoplamiento  

\* Mejora la mantenibilidad  

\* Facilita la reutilización en otros proyectos  



\---



\## Alcance de la Infraestructura



A través de estos módulos se despliegan los componentes principales de la Data Platform:



\- \*\*Azure Data Factory\*\* → Orquestación de pipelines  

\- \*\*Azure Databricks\*\* → Procesamiento distribuido  

\- \*\*Azure Key Vault\*\* → Gestión segura de secretos  

\- \*\*Azure SQL Database\*\* → Capa de serving  

\- \*\*Azure Storage Account\*\* → Data Lake  



En conjunto, estos servicios conforman la base de una arquitectura tipo \*\*Medallion (Bronze / Silver / Gold)\*\*.



\---



\## Organización de Terraform



El proyecto sigue una separación clara entre lógica, configuración y estado.



\---



\### backend.tf



Define dónde se almacena el estado de Terraform.



Este punto es crítico porque:



\- Permite trabajo colaborativo  

\- Evita inconsistencias entre ejecuciones  

\- Garantiza trazabilidad de cambios  



Sin backend remoto, Terraform no escala en equipos.



\### providers.tf — Configuración de Azure



Centraliza la configuración del provider (`azurerm`), incluyendo autenticación y suscripción.



Esto desacopla la lógica de infraestructura del entorno donde se ejecuta.



\### variables.tf



Define las variables de entrada del proyecto.



Aquí se establece \*\*qué es configurable\*\*:



\- nombres de recursos  

\- regiones  

\- configuraciones específicas  



Funciona como la interfaz pública del IaC.



\### terraform.tfvars



Contiene los valores concretos de las variables.



Esto permite:



\- Manejar múltiples entornos (dev / qa / prod)  

\- Separar código de configuración  

\- Evitar hardcoding  



\### main.tf — Orquestación



Es el punto central donde se integran todos los módulos.



Ejemplo conceptual:



module "storage" {

&#x20; source = "./modules/storage"

}



module "sql" {

&#x20; source = "./modules/sql"

}



Aquí ocurre lo importante:



Se ensamblan todos los componentes en una sola infraestructura coherente.



\### outputs.tf — Exposición de Resultados



Define qué valores exporta Terraform tras el despliegue.



Ejemplos:



\- connection strings  

\- endpoints  

\- nombres de recursos  



Esto permite integrar la infraestructura con otras capas del sistema (ej: pipelines o aplicaciones).



\---



\## Flujo de Ejecución



El ciclo de vida del despliegue es el estándar de Terraform:



terraform init  

terraform plan  

terraform apply  



Pero más allá de los comandos, lo importante es:



1\. init → prepara el entorno  

2\. plan → valida cambios antes de aplicarlos  

3\. apply → ejecuta el despliegue de forma controlada  



\---



\## Buenas Prácticas Implementadas



\### Modularización real

Cada servicio está aislado en su propio módulo.



Esto permite cambiar, escalar o reutilizar sin afectar otros componentes.





\### Separación de responsabilidades

\- Código → \*.tf  

\- Configuración → tfvars  

\- Estado → backend remoto  



\### Reutilización

Los módulos pueden ser reutilizados en otros proyectos o entornos sin modificaciones.



\### Escalabilidad organizacional

El diseño permite que distintos equipos trabajen en paralelo (por módulo).



\---



\## Decisiones Técnicas



| Decisión | Justificación |

|--------|-------------|

| Arquitectura modular | Reduce acoplamiento y mejora mantenimiento |

| Backend remoto | Permite trabajo en equipo |

| Variables externas | Flexibilidad entre entornos |

| Separación por módulos | Diseño limpio y escalable |



\---



\## Conclusión



Esta implementación no solo despliega infraestructura, sino que establece:



\* Un estándar de organización profesional  

\* Un modelo escalable de crecimiento  

\* Una base sólida para una Data Platform moderna  

\* Un enfoque alineado con buenas prácticas de la industria 

