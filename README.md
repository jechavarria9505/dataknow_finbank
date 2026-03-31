\# End-to-End Data Platform — FinBank  



\## Escenario A: Banca y Servicios Financieros



\---



\## Contexto



Este proyecto nace como respuesta a una prueba técnica de ingeniería de datos, cuyo objetivo era diseñar e implementar un pipeline completo, cubriendo desde la generación de datos hasta su disponibilidad para análisis.



Sin embargo, más allá de cumplir con los requisitos, el enfoque fue construir una solución que reflejara cómo se diseñaría una plataforma de datos en un entorno real.



El resultado es una implementación end-to-end que integra:



\- generación de datos sintéticos  

\- infraestructura como código  

\- orquestación de pipelines  

\- procesamiento distribuido  

\- gobierno de datos  

\- monitoreo y observabilidad  



\---



\## ¿Por qué elegí el escenario financiero?



Seleccioné el \*\*Escenario A — Banca y Servicios Financieros\*\* de forma intencional.



Este dominio no es el más simple, pero precisamente por eso es el más valioso desde el punto de vista de ingeniería.



El sector financiero introduce condiciones que obligan a elevar el nivel del diseño:



\- los datos son altamente sensibles  

\- los errores tienen impacto directo en el negocio  

\- la trazabilidad no es opcional  

\- la calidad de datos es crítica  

\- los patrones de uso son complejos y exigentes  



Trabajar sobre este escenario me permitió enfrentar problemas reales como:



\- inconsistencias entre fuentes  

\- registros incompletos  

\- duplicados  

\- necesidad de auditoría  

\- detección de comportamientos atípicos



En lugar de evitar la complejidad, decidí trabajar sobre ella.



\---



\## Visión de la solución



El pipeline fue diseñado como una plataforma de datos moderna, donde cada componente tiene una responsabilidad clara.



Generación → Ingesta → Bronze → Silver → Gold → Consumo



Este enfoque permite desacoplar responsabilidades y construir un sistema escalable y mantenible.



\---



\## Arquitectura general



La solución integra múltiples componentes que trabajan de forma coordinada:



* &#x20;Python para generación de datos  
* &#x20;Base de datos relacional como sistema fuente  
* &#x20;Terraform para aprovisionamiento  
* &#x20;Azure Data Factory para orquestación  
* &#x20;Databricks para procesamiento  
* &#x20;Data Lake por capas  
* &#x20;Unity Catalog para gobierno  
* &#x20;Key Vault para secretos  
* &#x20;Azure Monitor para alertas 



Cada componente fue seleccionado no solo por disponibilidad, sino por su rol dentro de una arquitectura coherente. 



\---



\## Generación de datos



Se construyó un modelo sintético que simula operaciones de una entidad financiera.



Los datos no fueron generados de forma trivial. Se incorporaron:



* relaciones entre entidades
* distribuciones realistas
* valores nulos controlados
* escenarios de error intencionales



Esto permitió validar que el pipeline no solo funciona en condiciones ideales, sino también frente a datos imperfectos.



\---



\## Infraestructura como código



Toda la infraestructura fue definida utilizando Terraform.



Esto garantiza:



* reproducibilidad del entorno
* consistencia entre despliegues
* facilidad para escalar o replicar la solución
* separación entre configuración y lógica



Se incluyeron componentes clave como almacenamiento, procesamiento, orquestación y gestión de secretos.



\---



\## Pipeline de datos



\### Bronze



La capa Bronze actúa como la representación fiel de la fuente.



Aquí se prioriza:



* mantener la estructura original  
* registrar metadata de carga 
* soportar ingestas incremental



No se realizan transformaciones complejas en esta capa.



\---



\### Silver - Control de calidad



La capa Silver es el núcleo del sistema.



En este punto tomé una de las decisiones más importantes del proyecto:

no tratar la calidad de datos como un paso opcional, sino como una responsabilidad central.



Aquí se implementan:



* Validaciones de integridad
* Estandarización de datos
* Control de duplicados
* Verificación de relaciones
* Enmascaramiento de datos sensibles 



\### Decisión clave:



En lugar de eliminar registros inválidos, diseñé una tabla de errores.



Esto responde a una necesidad real del dominio financiero:

los datos incorrectos también son información valiosa.



Esta decisión permite:



* auditoría
* análisis de calidad
* trazabilidad
* mejora continua de procesos



Los errores no se descartan, se gestionan.



\---



\### Gold - Capa analítica



En esta capa los datos se transforman en valor de negocio.



Se construyen:



* Modelos dimensionales
* Métricas agregadas
* Indicadores clave



Incluyendo:



* detección de transacciones atípicas
* análisis de comportamiento
* métricas de riesgo
* consolidación de información



Aquí el dato deja de ser técnico y se convierte en información útil para decisiones.



\---



\## Orquestación



El pipeline es controlado mediante Azure Data Factory.



Se implementó:



* ejecución dinámica por tabla
* dependencias explícitas
* control de errores
* reintentos automáticos



Esto garantiza que el flujo sea predecible y controlado.



\---



\## Monitoreo y observabilidad



Se incorporaron mecanismos de monitoreo desde el diseño.



* alertas por fallo
* notificaciones por correo
* registro de ejecuciones
* métricas de procesamiento



El objetivo fue evitar un sistema reactivo y construir uno observable.



\---



\## Gobierno y seguridad



El acceso a los datos fue diseñado bajo un modelo de roles:



* Administrador
* Ingeniero de Datos
* Analista



Además:



* uso de Unity Catalog para control centralizado
* enmascaramiento de información sensible
* gestión segura de credenciales



El gobierno no es un añadido, es parte del diseño.





\---



\## Conclusión



Este proyecto no fue abordado como un ejercicio académico, sino como una oportunidad para diseñar una solución cercana a un entorno real.



La elección del dominio financiero permitió trabajar sobre un escenario exigente, donde cada decisión tiene implicaciones en calidad, trazabilidad y confiabilidad.



Más allá de las herramientas utilizadas, el valor de la solución está en las decisiones tomadas:



* cómo se maneja el error
* cómo se garantiza la calidad
* cómo se organiza la arquitectura
* cómo se gobierna el dato



El resultado es una plataforma que no solo funciona, sino que puede explicarse, mantenerse y evolucionar.

