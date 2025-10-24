### 23 de Octubre del 2025
### Avance: Preparacion del entorno host 
Hoy trabaje para dejar preparado el entorno base para el LFS
1 **Instalacion del sistema base:**
  -VitualBox configurado con Rocky Linux 10 minimal
  -Asigne 4 GB de Ram, 2 CPU y 40 de disco
  -Configure usuario root y contraseña

2 **Creacion del script de verificacion:**
  -Escribi un script basado en el del libro pero simplificado con IA en bash para comprobar las herramientas necesarias del sistema host.
  -Al ejecutar el script, pude confirmar la presencia de la mayoria de programas pero nose si se colgaba el scrip o yo no le daba el tiempo suficiente+
  -El comando "Id" aparecia como no encontrado, por lo que falta resolver eso 

4 **Problemas encontrados**
  -No tenia un editor de texto por lo que no sabia como escribir el script, solucionado con "nano"
  -El scrip se queda como esperando, nose si no le doy el tiempo suficiente o porque no se cerraba el bloque "EOF"
  -Problemas aprendiendo los simbolos a usar en la terminal 

5 **Proximos pasos**
  -Corregir el deteccion de "Id"
  -Reejutar el script hasta que todas las herramientas aparezcan como instaladas
  -Luego continualr con la creacion de usuario LFS


### 24 de Octube del 2025
### Avance: Terminar el entorno del host
Seguimos configurando y dejando preparado el entorno
1 **Mejorar el spcrip para verificar las herramientas**
  -Mejore el scrpit de verificacion de versiones de las herramientas necesarias con un tiempo de espera 

4 **Problemas encontrados**
 -No encontro Id y coreutils
