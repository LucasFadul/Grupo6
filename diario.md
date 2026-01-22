### 23 de Octubre del 2025
### Avance: Preparacion del entorno host 
Hoy trabaje para dejar preparado el entorno base para el LFS
**Instalacion del sistema base:**
- VitualBox configurado con Rocky Linux 10 minimal
- Asigne 4 GB de Ram, 2 CPU y 40 de disco
- Configure usuario root y contraseña

**Creacion del script de verificacion:**
- Escribi un script basado en el del libro pero simplificado con IA en bash para comprobar las herramientas necesarias del sistema host.
- Al ejecutar el script, pude confirmar la presencia de la mayoria de programas pero nose si se colgaba el scrip o yo no le daba el tiempo suficiente+
- El comando "Id" aparecia como no encontrado, por lo que falta resolver eso 

**Problemas encontrados**
- No tenia un editor de texto por lo que no sabia como escribir el script, solucionado con "nano"
- El scrip se queda como esperando, nose si no le doy el tiempo suficiente o porque no se cerraba el bloque "EOF"
- Problemas aprendiendo los simbolos a usar en la terminal 

**Proximos pasos**
- Corregir el deteccion de "Id"
- Reejutar el script hasta que todas las herramientas aparezcan como instaladas
- Luego continualr con la creacion de usuario LFS


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

 ### 25 de Octubre del 2025
 ### Avance: Creacion de la particion y montaje del entorno LFS
 Hoy continue con al preparacion del entorno del sistema anfitrion, siguiendo las indicaciones del CAP. 2.4 del libro LFS. EL objetivo fue crear y montar la particion donde se construira el sistema LFS
**Creacion del nuevo disco**
-Agregue un segundo disco virtual de 25 GB en VirtuaBox, con almacenamiento dinamico tipo VDI, para evitar ocupar espacio fisico innecesario en el host.
-El nuevo disco fue detectado dentro del sistema como /dev/sdb

**Particiones del disco**
-Utilice la herramienta fdisk para crear una nueva tabla de particiones y una particion primaria que ocupe todo el disco
-Comandos utilizados: 
* sudo fdisk /dev/sdb
* n -> p -> Entern -> Enter -> w
-Luego de guardar los cammbios, verifica la particion mediante lsblk confirmando la creacion de /dev/sda1

**Formateo y montaje del sistema de archivos**
-Formatee la particion con ext4 utilizando:
* sudo mkfs -v -t ext4 /dev/sda1
-Cree el punto de montaje y monte la particion:
* sudo mkdir -pv /mnt/lfs
* sudo mount -v -t ext4 /dev/sda1 /mnt/lfs
-El sistema mostro una advertencia relacionada con SELinux labels, la cual no afecta al proceso LFS
Confirme el montaje ejecutando:
* df -h | grep lfs

### 20 de Diciembre del 2025
### Avance: Reconstruccion del Host y Preparacion del entorno LFS 2.0
Debido a una falla critica en la VM anterior, nos vimos en la necesidad de realizar el proyecto desde cero. Permitiendonos corregir el hardware para mayor eficiencia y aplicar la experencia previa para optimizar la instalacion del sistema anfitrion
**Configuracion de Hardware**
- Se instalo Rocky Linux 10.0 en una nueva VM de VirtualBox
- Se ajustaron los recursos para cumplir con los requisitos minimos del TP: 8 GB de RAM y 4 nucleos de CPU
- Se configuraron dos unidades de almacenamiento: un disco de 40 GB para el sistema host y un segudno disco virtual de 25 GB (VDI) dedicado exclusivamente al sistema LFS

**Preparacion del software anfitrion**
- Habilitacion de repositorios: Se activo el repositorio CRB, esencial en Rocky 10 para las herramientoas de desarrollo
- Instalacion de dependencias: Se instalo el grupo Development Tools y los paquetes texinfo, patch y bison
- Validacion: Se ejecuto el script version-check.sh del libro LFS 12.4 para garantizar un entorno de compilacion eficiente
- Enlaces simbolicos: Se crearon manualmente los enlaces /usr/bin/yacc -> /usr/bin/bison y /bin/sh -> /bin/bash para cumplir con los estandares del manual

**Estructura de directorios y seguridad**
- Se creo la jerarquia inicial de carpetas en el punto de montaje (/usr, /bin, /lib, /sbin, /etc, /var, /tools)
- Se configuraron los enlaces simbolicos de 64 bits para asegurar la compatibilidad de la arquitectura
- Usuario LFS: Se creo el usuario y grupo lfs para realizar la compilacion sin privilegios de root, protegiendo la integridad del host
- Se transfirio la propiedad de todos los directorios en $LFS al usuario lfs

**Problemas encontrados y soluciones**
- Repositorio CRB y lo vacio del host "minimal":
    Al ejecutar el script de validacion de herramientas en el nuevo anfitrion Rocky Linux 10, detectamos una ausencia critica de paquetes esenciales como texinfo, patch y bison. En esta version de Rocky, estas herramientas de desarrollo no se encuentran en los repositorios estandar por defecto
    *Solucion*: Activamos el repositorio CRB mediante el gestor de paquetes dnf. Una vez activo, pudimos satisfacer las dependencias exigidas por el manual LFS 12.4, asegurarndo que el sistema sea capaz de generar la documentacion y aplicar parches durante la compilacion de la cadena de herramientas

### 21 de Diciembre del 2025
### Avance Obtencion de fuentes y parches
Se completo la descarga y verificacion de los aprox. 90 archivos (paquetes base y parche) requeridos por el manual LFS 12.4. Este dia nos centramos en optimizar las descargas y la depuracion del entorno para asegurar que la "materia prima" del sistema sea exacta y no presente corrupciones

**Descargas y eficiencia aplicada**
-Para maximizar el tiempo, se utilizo una estrategia hibrida:
  -WinSCP: Se utilizo para trasferir los paquetes mas pesados (como gcc-13.2.0.tar.xz de 84 MB) desde el sistema anfitrion.
  Esto evito saturar la conexion de la maquina virtual y permitio usar gestores de descargas mas rapidos en Windows

  -Wget-list:Se automatizo la descarga de parches y paquetes ligeros mediante el uso de las listas oficiales wget-list y wget-list-patches directamente en la terminal de linux

**Gestion de permisos y seguridad**
-Tras las transferencias por WinSCP, se detecto que algunos archivos no pertenecian al usuario constructor. Se ejecuto:
    "chow -v lfs:lfs $LFS/sources?*" Esto garantiza que el usuario lfs tenga control total durante la fase de extraccion y compilacion en los capitulos siguientes

**Problemas encontrados y soluciones**
-Incompatibilidad de versiones (Version Drift)
  Debido a que algunos comandos wget apuntaron a repositorios "latest", se descargaron versiones excesivamente modernas como GCC 15 y Binutils 2.45. Estas versiones son incompatibles con las instrucciones y parches específicos de la receta LFS 12.4.
  *Soulcion*: Realizamos una auditoría de versiones y una purga manual de todos los paquetes excedentes. Esto asegura que el compilador no intente enlazar librerías de versiones distintas, lo que garantiza la estabilidad de la cadena de herramientas.

-Latencia en descargas de archivos grandes vía Terminal
  La descarga directa en la máquina virtual para paquetes de gran volumen (GCC, Python, Glibc) presentaba tiempos de espera ineficientes y riesgos de desconexión.
  *Solucion*: Implementamos una estrategia de transferencia híbrida utilizando WinSCP. Descargamos los paquetes pesados en el sistema anfitrión y los transferimos por SFTP, asegurando la propiedad de los archivos mediante chown lfs:lfs para evitar conflictos de permisos posteriores.


### 22 de Diciembre del 2025
### Avance: Vinculacion de entorno y preparacion para el cap 5
El dia de hoy buscamos dejar el terreno listo. El objetivo fue que la MV y el disco externo se entendieran bien para que el usuario lfs pueda trabajar tranquilo sin romper el sistema principal

**El puente de /tools**
- Creacion de un enlace simbolico de /tools hacia mi disco externo (/mnt/lfs/tools). Esto es clave porque el manual pide que todo se instale en /tools, pero necesitamos que los archivos fisicamente se almacenen em el disco de 25GB y no en el de la VM

**Configuracion del usuario lfs** 
- Preparacion de los archivos .bash_profile y .bashrc. Ahora cada vez que se ingresa con su - lfs, el sistema ya sabe que la ruta es /mnt/lfs y el compilador usa un entorno limpio, para que no se mezcle nada del Rocky Linux con lo que se construira

**Permisos**
- Asignacion de propiedad a la carpeta tools al usuario lfs. Si este paso, cuando se quisiera instalar Binultis saltaria error

**Problemas y soluciones**
- Enlace roto: Si se reinicia la VM y no se monta el disco externo primero, el enlace /tools no serviria de nada
  - *Solucion*: Primero montar el disco sbd1 y recien ahi entrar como usuario cosntructor 

- Espacio de memoria: Activacion de la particion Swap del disco externo por la dudas. Los compiladores como GCC exigen mucha RAM y se busca que la VM no se cuelgue a la mitad del proceso

### 06 de Enero del 2026
### Avance: Compilacion de herramientas basicas y problemas en diffutils
El objetivo de hoy fue llenar /usr/bin del nuevo sistema con las utilidades esenciales. Ya pasamos la fase mas pesada de compilacion (GCC, Flibc) y entramos en la fase de herramiebtas de usuario

**Binario de sistema**
- Instalacion exitosa de Bash y Corenutils. Con esto, el sistema LFS ya tiene su propia terminal y comandos basicos de archivos (ls, cp, mv)

**Verificacion de Ejecutables**
- Se comprobo mediante el comando file que los binarios estan correctamente vinculados al interprete de LFS y no la del host 

**Compilacion cruzada**
- Instalacion de herramientas de soporte como M4, Ncuses y file. Se aplico un metodo de compilacion doble para file, creando una version nativa temporal para poder compilar la version del target

**Problemas y Soluciones**
- Error de Enlace en Bash: Al intentar crear el enlace simbólico /usr/bin/sh, el sistema arrojó "File exists".
  *Solucion*: Uso de ln -sfv para forzar la creación del enlace apuntando a bash

- Bloqueo en Diffutils: El script configure aborta con un error. Esto sucede porque el paquete intenta ejecutar pruebas de funciones que son incompatibles con la arquitectura del host durante la construcción.
  - *Estado*: Pendiente a solucionarlo


### 21 de enero 2026
### Avance: Finalizacion del Toolchain, Chroot y herramientas criticas
El objetivo de hoy fue terminar la cadena de herramientas temporal, aislar el sistema dentro del entorno Chroot y dejar listas las utilidades de lenguaje para la construccion final

**Aislamiento del sistema (toolchain)**
- Compilacion de Binutils y gcc fase 2 configurados con --with-sysroot. Esto garantiza que el enlazador busque librerias en /mnt/lfs y no en el host.

**Configuracion de Entorno (Chroot)**
- Creacion de la jerarquia de directorios, usuarios root y archivos de configuracion basicos (passwd, group). Se montaron los sistemas virtuales (/dev, /proc) para hacer funcional el entorno

**Herrasmientas de lenguaje**
- Instalacion exitosa de Perl y de Python dentro del chroot. Se verifico que texinfo y util-linux compilaran correctamente tras resolver dependencias

**Problemas y soluciones**
- Borrado accidental de archivos: Se elimino el .tar.xz de Python por errror antes de compilar
  *Solucion*: Descargar mediante wget desde el host hacia la carpeta de fuentes montadas

- Bloqueo de Terminal (PTY): Perdida de acceso a sudo por mal montaje de /dev/pts
  *Solucion*: Script de montaje secuencial para restaurar la conectividad del chroot

-Error en Util-linux: Fallo en configure por flag --static obsoleto y falta de sqlite3 para liblastlog2
  *Solucion*: Se desactivo la libreria conflictiva y se removio el flag incompatible en la configuracion

