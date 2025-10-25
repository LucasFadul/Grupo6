### 23 de Octubre del 2025
### Avance: Preparacion del entorno host 
Hoy trabaje para dejar preparado el entorno base para el LFS
**Instalacion del sistema base:**
  -VitualBox configurado con Rocky Linux 10 minimal
  -Asigne 4 GB de Ram, 2 CPU y 40 de disco
  -Configure usuario root y contraseña

**Creacion del script de verificacion:**
  -Escribi un script basado en el del libro pero simplificado con IA en bash para comprobar las herramientas necesarias del sistema host.
  -Al ejecutar el script, pude confirmar la presencia de la mayoria de programas pero nose si se colgaba el scrip o yo no le daba el tiempo suficiente+
  -El comando "Id" aparecia como no encontrado, por lo que falta resolver eso 

**Problemas encontrados**
  -No tenia un editor de texto por lo que no sabia como escribir el script, solucionado con "nano"
  -El scrip se queda como esperando, nose si no le doy el tiempo suficiente o porque no se cerraba el bloque "EOF"
  -Problemas aprendiendo los simbolos a usar en la terminal 

**Proximos pasos**
  -Corregir el deteccion de "Id"
  -Reejutar el script hasta que todas las herramientas aparezcan como instaladas
  -Luego continualr con la creacion de usuario LFS


### 24 de Octube del 2025
### Avance: Terminar el entorno del host
Comprobar que el sistema anfitrion cumpla con todos los requisitos para construir el entorno LFS
**Cambios en el script y preparacion de entorno hostNo **
 -Tome la decicion de crear el script version-check.sh basado en el codigo del libro y no usar el anteriormente optimizado por la IA, este con el fin de verificar las versiones minimas de las herramientas criticas del sistema
 -Se ejecuto el script y se analizaron los resultados 
 -Se corrigeron las advertencias relacionadas con Texinfo y yacc instalando el paquete correspondiente y asegurando compatibilidad con Bison

 **Problemas encontrado**
 -El paquete Texinfo no estaba disponible inicialmente en los repositorios principales de Rocky Linux, por lo que fue necesario habilitar el repositorio CRB (CodeReady Builder) antes de poder instalarlo correctamente 
 -El comando yacc ya existia como binario independiente (no como enlace), lo que impidio crear el vinculo simbolico directamente hacia bison. Para resolverlo, elimine el binario anterior y cree un nuevo enlace simbolico que apunta a bison, dejando el entorno correctamente configurado como en el libor

 **Resultados**
 -Todas las herramientas esenciales (bash,gcc,make,coreutils,etc) se encuentran en versiones superiores a las requeridas por el libro
 -Se verifico que el kernel soporta UNIX98 PTY y que el compilador g++ funciona correctamente
 -El entorno anfitrion quedo completamente preparado para continuar con la siguiente etapa del proyecto LFS.
