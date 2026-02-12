### 23 de Octubre del 2025
### Avance: Preparacion del entorno host 
### Participante: Lucas
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
- Luego continuar con la creacion de usuario LFS


### 24 de Octube del 2025
### Avance: Terminar el entorno del host
### Participante: Lucas
Comprobar que el sistema anfitrion cumpla con todos los requisitos para construir el entorno LFS
**Cambios en el script y preparacion de entorno hostNo **
- Tome la decicion de crear el script version-check.sh basado en el codigo del libro y no usar el anteriormente optimizado por la IA, este con el fin de verificar las versiones minimas de las herramientas criticas del sistema
- Se ejecuto el script y se analizaron los resultados 
- Se corrigeron las advertencias relacionadas con Texinfo y yacc instalando el paquete correspondiente y asegurando compatibilidad con Bison

 **Problemas encontrado**
- El paquete Texinfo no estaba disponible inicialmente en los repositorios principales de Rocky Linux, por lo que fue necesario habilitar el repositorio CRB (CodeReady Builder) antes de poder instalarlo correctamente 
- El comando yacc ya existia como binario independiente (no como enlace), lo que impidio crear el vinculo simbolico directamente hacia bison. Para resolverlo, elimine el binario anterior y cree un nuevo enlace simbolico que apunta a bison, dejando el entorno correctamente configurado como en el libor

 **Resultados**
- Todas las herramientas esenciales (bash,gcc,make,coreutils,etc) se encuentran en versiones superiores a las requeridas por el libro
- Se verifico que el kernel soporta UNIX98 PTY y que el compilador g++ funciona correctamente
- El entorno anfitrion quedo completamente preparado para continuar con la siguiente etapa del proyecto LFS.

 ### 25 de Octubre del 2025
 ### Avance: Creacion de la particion y montaje del entorno LFS
 ### Participante: Lucas
 Hoy continue con al preparacion del entorno del sistema anfitrion, siguiendo las indicaciones del CAP. 2.4 del libro LFS. EL objetivo fue crear y montar la particion donde se construira el sistema LFS
**Creacion del nuevo disco**
- Agregue un segundo disco virtual de 25 GB en VirtuaBox, con almacenamiento dinamico tipo VDI, para evitar ocupar espacio fisico innecesario en el host.
- El nuevo disco fue detectado dentro del sistema como /dev/sdb

**Particiones del disco**
- Utilice la herramienta fdisk para crear una nueva tabla de particiones y una particion primaria que ocupe todo el disco
- Comandos utilizados: 
  - sudo fdisk /dev/sdb
  - n -> p -> Entern -> Enter -> w
- Luego de guardar los cammbios, verifica la particion mediante lsblk confirmando la creacion de /dev/sda1

**Formateo y montaje del sistema de archivos**
- Formatee la particion con ext4 utilizando:
  - sudo mkfs -v -t ext4 /dev/sda1
- Cree el punto de montaje y monte la particion:
  - sudo mkdir -pv /mnt/lfs
  - sudo mount -v -t ext4 /dev/sda1 /mnt/lfs
- El sistema mostro una advertencia relacionada con SELinux labels, la cual no afecta al proceso LFS
Confirme el montaje ejecutando:
  - df -h | grep lfs

### 20 de Diciembre del 2025
### Avance: Reconstruccion del Host y Preparacion del entorno LFS 2.0
### PArticipante: Lucas
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
### Participante: Mateo
Se completo la descarga y verificacion de los aprox. 90 archivos (paquetes base y parche) requeridos por el manual LFS 12.4. Este dia nos centramos en optimizar las descargas y la depuracion del entorno para asegurar que la "materia prima" del sistema sea exacta y no presente corrupciones

**Descargas y eficiencia aplicada**
- Para maximizar el tiempo, se utilizo una estrategia hibrida:
  - WinSCP: Se utilizo para trasferir los paquetes mas pesados (como gcc-13.2.0.tar.xz de 84 MB) desde el sistema anfitrion.
  Esto evito saturar la conexion de la maquina virtual y permitio usar gestores de descargas mas rapidos en Windows

  - Wget-list:Se automatizo la descarga de parches y paquetes ligeros mediante el uso de las listas oficiales wget-list y wget-list-patches directamente en la terminal de linux

**Gestion de permisos y seguridad**
- Tras las transferencias por WinSCP, se detecto que algunos archivos no pertenecian al usuario constructor. Se ejecuto:
    "chow -v lfs:lfs $LFS/sources?*" Esto garantiza que el usuario lfs tenga control total durante la fase de extraccion y compilacion en los capitulos siguientes

**Problemas encontrados y soluciones**
- Incompatibilidad de versiones (Version Drift)
  Debido a que algunos comandos wget apuntaron a repositorios "latest", se descargaron versiones excesivamente modernas como GCC 15 y Binutils 2.45. Estas versiones son incompatibles con las instrucciones y parches específicos de la receta LFS 12.4.
  *Soulcion*: Realizamos una auditoría de versiones y una purga manual de todos los paquetes excedentes. Esto asegura que el compilador no intente enlazar librerías de versiones distintas, lo que garantiza la estabilidad de la cadena de herramientas.

- Latencia en descargas de archivos grandes vía Terminal
  La descarga directa en la máquina virtual para paquetes de gran volumen (GCC, Python, Glibc) presentaba tiempos de espera ineficientes y riesgos de desconexión.
  *Solucion*: Implementamos una estrategia de transferencia híbrida utilizando WinSCP. Descargamos los paquetes pesados en el sistema anfitrión y los transferimos por SFTP, asegurando la propiedad de los archivos mediante chown lfs:lfs para evitar conflictos de permisos posteriores.


### 22 de Diciembre del 2025
### Avance: Vinculacion de entorno y preparacion para el cap 5
### Participante: Lucas
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
### Participante: Lucas
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

### 22 de enero del 2026
### Avance: Migracion a SSD, Glibc y utilerias base
### Participante: Mateo
El objetivo de hoy fue instalar la libreria central del sistema (Glibc) aprovechando la migracion de hardware a SSD (reduciendo el tiempo de compilacion) y dejar listas las herramientas fundamentales de compresion y procesamiento de archivos

**Libreria C (Glibc) y configuracion regional**
- Instalacion exitosa de Glibc aplicando parches FHS
- Configuracion de "Locales" (es_ES, en_EN), archivo nsswitch.conf y definicion de la zona horaria para Paraguay
- Se ejecuto el test critico verificando al estabilidad del toolchain

**Herramientas de archivos y compresion**
- Compilacion e instalacion del set completo de compresion: Zlib, Bzip2 (con parche shared), Xz y Zstd
- Instalacion de File (reconocimiento de archivos) y Readline (historial y navegacion en terminal)

**Utilidades de desarrollo**
- Intalacion de M4, BC y Flex
- Creacion del enlace simbolico vital ln -sv flex /usr//bin/lex para compatibilidad futura con el kernel

**Problemas y Soluciones**
- Interrupcion por Suspencion: El host entro en suspencion durante el make check de Glibc
  *Solucion*: Se remonto el entorno Chroot y se reanudaron las pruebas. Resultado: 1 fallo menor en threads (ignorable)

- Falso positivo en instalacion Glibc: Error "script doesn't work if installing not as primary" al final del make install
  *Solucion*: Se verifico manualmente /usr/lib/libc.so.8 el error era del script de testeo final, no de la instalacion

- Error de sintaxis en BC: Fallo de compilacion flaseUL undeclared debido a la rigurosidad de GCC 15 (C23 standard)
  *Solucion*: Se forzo el estandar antiguo en la configuracion mediante CC="gcc -std=c99" ./configure

- Archivos de zona horarias faltantes: Error zic: Can't open pacificnew al configurar el reloj
  *Solucion*: Se ignoró el error ya que esos archivos son obsoletos en IANA

### 23 de enero del 2026
### Avance: Diagnostico del capitulo 8, revision de fuentes y reset controlado 
### Participante: Mateo
El objetivo incial del dia fue avanzar y cerrar el capitulo 8 del libro. Sin embargo, multiples errores acumulados durante intentos previos dejaron en envidencia inconsistencias estructurales en el sistema construido. La jornada termino con una decision critica: reinciar la construccion desde el capitulo 5, priorizando coherencia y reproducibilidad

**Capitulo 8 y estado del sistema**
- Se intento continuar con la instalacion de paquetes del capitulo 8, encontrando errores recurrentes en configuraciones y builds
- GRUB 2.12 presento fallos de dependencias y comportamientos inconsistentes, especialmente luego de compilaciones paralelas y arboles de build contaminados
- Se detectaron ejecuciones de make sobre paquetes cuyo configure habia fallado o sido interrumpido previamente
- Se identifico mezcla de contextos entre host, chroot y permisos de usuarios, afectando la estabilidad general del entorno

**Audutoria de fuentes LFS 12.4**
- Se monto correctamente la particion LFS
- Se verifico el contenido de /mnt/lfs/sources contra wget-list-systemd
- Se validaron criptograficamente todas las fuentes mediante md5sum
- Se descargaron los archivos faltantes y se confirmo la integridad total de las fuentes

  *Resultado*:
  - Todas las fuentes quedaron alineadas al LFS 12,4 (systemd)

 **Dicision Tecnica: Reset del sistema construido**
 - Tras confirmar que las fuentes eran correctas, se decidio no continuar forzando el capitulo 8
 - Se realizo un reset controlado del sistema base para eliminar cualquier inconsistencia historica
 - se conservaron unicamente la estructura minima de la particion LFS y el directorio /sources

**Problemas y Soluciones**
- Acumulacion de errores en capitulo 8 debido a builds interrumpidos y reintentos sobre arboles sucios
  *Solucion*: Abandonar el estado actual del sistema y reiniciar desde el capitulo 5

- Confusion entre estado real del  sistema y estado de las fuentes
  *Solucion*: Auditoria completa de fuentes y verificacion criptografica previa a cualquier nueva compilacion

**Estado actual**
- Sistema LFS: limpio, sin toolchain ni sistema base instalado
- Fuentes: 100% verificadas y completas (LFS 12.4)
- Punto de reinicio: Capítulo 5 – Binutils Pass 1

### 24 y 25 de enero del 2026
### Avance: Reconstruccion completa del toolchain LFS (Capitulo 5 y 6)
### Participante: Mateo
Tras la decision de reiniciar la construccion desde el capitulo 5, se inicio una reconstruccion completa y controlada del sistema LFS, priorizando coherenciam, aislamiento del host y validacion en cada etapa

**Reinicio desde el capitulo 5 - Toolchain**
- Se comenzo nuevamente desde Binutils Pass 1, siguiendo estrictamente el libro LFS 12.4 y evitando reutilizar elementos de intentos previos
- Durante esta fase se establecieron correctamente las variables de entorno
  - LFS=/mnt/lfs
  - LFS_TGT=x86_64-lfs-linux-gnu
  - PATH=/mnt/lfs/tools/bin:/usr/bin
- Se verifico que:
  - El compilador del host (/usr/bin/gcc) no interfiriera
  - Todas las herramientas generadas apuntaran exclusivamente a /tools

**Capitulo 5 - Construccion del toolchain inicial**
- Se completaron exitosamente
  - Binutils Pass 1
  - GCC Pass 1
  - Linux API Headers
  - Glibc
  - Libstdc++
- Validaciones realizadas:
  - ld y gcc usados pertenecen a /tools
  - libc.so y ld-linux-x86-64.so.2 instalados en $LFS/usr/lib
  - El compilador cruzado genera binarios correctamente
- Se detectaron y corrigieron errores tipicos:
  - Builds interrumpidos
  - Falta de headers en el momento correcto
  - Errores de permisos al instalar glibc

**Capitulo 6 - Herramientas temporales**
- Se instalaron correctamente todas las herramientas temporales requeridas por el libro
  - m4
  - ncurses
  - bash
  - coreutils
  - diffutils
  - file
  - findutils
  - gawk
  - grep
  - gzip
  - make
  - patch
  - sed
  - tar
  - xz
  - expect
  - dejagnu
  - perl
  - python3
  - texinfo (texi2any)
  - gettext (xgettext)
  - bison
- Durante esta fase:
  - Se detecto un error en en Expect 5.45.4 debido a la ausencia de pty_.c
  - Se aplicó correctamente el parche expect-5.45.4-gcc15-1.patch, resolviendo el problema
  - Se evitó reinstalar paquetes ya presentes (ej. ncurses), verificando antes con binarios en /tools/bin

**Revision final del toolchain**
- Se realizo una verificacion exhaustiva del entorno /tools
  - Todos los binarios requeridos existen en /tools/bin
  - Las versiones coinciden con las esperadas por LFS 12.4
  - No hay dependencias faltantes
  - No se detecto contaminacion del host

**Estado actual del sistema**
- Capitulo 5 y 6 completados correctamente
- Toolchain temporal coherente, limpio y valido
- Fuentes verificadas criptograficamente
- Estructura LFS /mnt/lfs/{usr,etc,var,tools,sources} correcta
- Usuario acutal lfs, listo para pasar al chroot

### 28 de enero del 2026
### Avance: Entrada al Chroot, identidad del sistema y herramientas internas (Capitulo 7)
### Participante: Mateo
El objetivo del dia fue realizar el salto definitivo al entorno Chroot, estableciendo un sistema LFS funcional desde dentro de su propia particio. Se busco consolidar la identidad basica del sistema, crear su estructura estandar y compilar herramientas criticas ya no como entorno temporal, sino como parte del sistema en construccion

**Entrada al Chroot y entorno del sistema**
- Se abandono el usuario lfs y se tomo control total como root
- Se montaron correctamente los pseudo-sistemas necesarios (/dev, /prooc. /sys, /run) mediante bind mounts
- Se ejecuto exitosamente el comando chroot, pasando a operar completamente dentro de la particion LFS
- El sistema paso a depender exclusivamente de sus propias herramientas y librerias

**Estructura base e identidad del sistema**
- Se creo la jerarquia estandar de directorios Linux (/bin, /etc, /usr, /var, /lib, /sbin, etc)
- Se generaron los archivos fundamentales de identidad:
  - /etc/passwd
  - /etc/group
- Se eliminarion los mensajes tipo "I have no name", confirmando identidad valida del usuario root
- Se crearon los archivos de bitacora del sistema:
  - lastlog
  - wtmp
  - btmp
- El sistema quedo preparado para registrar accesos y eventos basicos

**Herramientas compiladas dentro del chroot**
- Se compilo e instalo un conjunto clave de herramientas desde dentro del sistema LFS, validando el correcto funcionamiento del toolchain final:
  - Gettext
  - Bison
  - Perl
  - Python
  - Texinfo
  - Util-linux
- Estas instalaciones confirmaron que el sistema ya puede autocompilar software complejo sin depender del host

**Limpieza y seguridad**
- Se eliminaron archivos temporales, documentacion innecesaria y residuos del proceso de build
- Se optimizo el espacio en disco dejando el sistema limpio y ordenado
- Se salio correctamente del entorno chroot
- Se desmontaron todos los pseudo-sistemas
- Se creo un backup completo del estado actual en el archivo
  - lfs-temp-tools-12.4.tar.xz
- Este respaldo permite volver a este punto estable en minutos ante cualquier fallo futuro

**Estado actual**
- Sistema LFS funcional dentro de chroot
- Toolchain final operativo
- Identidad y estructura del sistema definidas
- Herramientas esenciales instaladas
- Backup de seguridad creado

**Proximo objetivo**
- Capitulo 8 - instaldacion del sistema base completo

### 29 de enero del 2026
### Avance: Capitulo 8 - Construccion del sistema base hasta Coreutils
El objetivo del dia fue iniciar formalmente el capitulo 8 del libro LFS, comenzando la transicion desde un entorno chroot funcional hacia un sistema linux real, instalando los componentes fundamentales del userland. La jornada se centro en establecer las bases del sistema, las herramientas de compilacion definitivas y las utilidades esenciales de uso diario

**Base del sistema**
- Instalacion de Man-pages, proporcionando documentacion local para comandos y llamadas del sistemma
- Instalacion de Iana-Etc, establecienddo la base de archivos de servicios y protocolos de red
- Compilacion e instalacion de Glibc
  - Se verifico la correcta instalacion del enlazador dinamico (/lib/ld-linux-x86--64.so.2)
  - El sistema quedo habilitaddo para ejecutar binarios de manera autonoma
- Instalacion de las librerias de compresion fundamentales
  - Zlib
  - Bzip2
  - XZ
  - Zstd
  Estas librerias son criticas para el manejo de archivos comprimidos utilizados por multiples paquetes posteriores

**Herramientas esenciales de compilacion**
- Instalacion de File, para identificacion confiable de tipos de archivos
- Instalacion de Readline, habilitando edicion interactiva e historial en la terminal
- Instalacion de M4 y BC, herramientas utilizadas por sistemas de configuracion y build
- Instalacion de Binutils, proveyendo ensamblador, enlazador y utilidades binarias
- Instalacion de Flex y Bison, generadores lexicos y sintacticos requeridos por multiples proyectos del sistema

**Compilador definitivo del sistema**
- Compilacion e instalacion de GCC como compilador final
- Se verifico que el compilador:
  - Utiliza las librerias del sistema LFS
  - Enlaza correctamente contra Glibc instalada
- A partir de este punto, el sistema dejo de depender del compilador temporal del host

**Herramientas criticas de soporte y testing**
- Instalacion de Tcl, Expect y DejaGNU, habilitando la ejecucion de suites de pruebas
- Instalacion de Pkgconf (pkg-config), permitiendo la correcta deteccion de dependencias entre paquetes
- Instalacion de Ncurses, habilitando interfaces de texto avanzadas para aplicaciones en terminal
- Intalacion de Sed, herramienta clave para edicion de flujo y parcheo durante la construccion

**Infraestructura mooderna y utilidades basicas**
- Instalacion del ecosistema completo de Python
- Instalaciond de OpenSSL, proporcionando soporte criptografico
- Instalacion de Meson y Ninja, sistemas modernos de construccion
- Instalacion de Coreutils, incorporando los comandos esenciales del sistema (ls, cp, mv, rm, chmod, etc)

**Estado actual**
- Capitulo 8 iniciado correctamente
- Sistema base funcional dentro de chroot
- Toolchain definitivo operativo
- Userland esencial instalado hasta Coreutils
- El sistema es capaz de compilar, ejecutar y gestionar software sin dependencia del host

**Proximo objetivo**
- Continuar el capitulo 8 con las utilidades restantes y avanzar hacia la preparacion del Kernel

### 30 de enero del 2026
### Avance: Capítulos 8 (desde Coreutils hasta el final), 9, 10 y 11 – Sistema completo, Kernel, GRUB y primer boot exitoso
### Participante: Mateo
El objetivo del día fue cerrar completamente la construcción del sistema LFS, finalizando el Capítulo 8 (desde Coreutils hasta su cierre), realizando la configuración del sistema (Cap. 9), preparando el arranque (Cap. 10) y ejecutando la etapa final (Cap. 11) hasta lograr un arranque real del sistema con login funcional. La jornada incluyó un incidente crítico con GRUB que obligó a una recuperación completa del sistema anfitrión, dejando una lección fuerte sobre bootloaders y coexistencia de sistemas.

**Capítulo 8 – Construcción del sistema base (desde Coreutils hasta el cierre**
- Finalización del userland esencial
  - Continuación del sistema base posterior a Coreutils, incorporando herramientas restantes necesarias para un Linux usable y administrable
  - Instalacion de utilidades de sistema y mantenimiento:
    - Herramientas de procesos, administración, y utilidades de bajo nivel (suite base para operar y depurar el sistema).
    - Herramientas de archivos y manipulación de texto, completando el conjunto estándar de comandos
  - Instalacion de utilidades de red y diagnostico:
    - Componentes para manejo de interfaces, rutas y verificación de conectividad
  - Instalacion de herramientas de sistema y libreiras faltantes para completar dependencias del entorno final
- Usuarios, permisos y seguridad del sistema
  - Incorporacion y verificacion del init y componentes necesarios para el arranque tradicional del sistema (entorno no dependiente del host)
  - Ajustes de estructura del sistema y archivos criticos para el funcionamiento cotidiano
- Soporte de arranque e inicializacion dentro del sistema
  - Instalacion y verificacion del init y componentes necesarios para el arranque tradicional del sistema (entorno no dependiente del host)
  - Consolidacion del sistema para funcionar de forma autonoma (ya no como "entorno de build")
- Cierre del capitulo 8
  - Limpieza final del sistema
  - Validacion de que el sistema construido contiene lo necesario para continuar con configuracion, kernel y boot

**Capitulo 9 - Configuracion del sistema**
- Dispositivos, red y persistencia
  - Configuracion de reglas de Udev para nombres persistentes de interfaces de red
  - Confimacion del nombre de interfaz:
    - enp0s3
  - Ajustes para evitar conflictos de nombres alternativos y asegurar consistencia en el arranque
- Identidad del sistema
  - Definicion del hostname final del sistema:
    - lfs-SO1
  - Teclado, consola e idioma
    - Configuracion del teclado US internacional manteniendo caracteres especiales y acentos
    - Configuracion de la consola:
      - /etc/sysconfig/console usando us-acentos
    - Configuracion regional y locales:
      - Locale configurado en UTF-8 para entorno en español
      - Creacion de /etc/profile para exportacion corrrecta de LANG
    - Archivos base de interaccion
      - Creación de archivos necesarios para uso cómodo del sistema:
        - /etc/inputrc (Readline)
        - /etc/shells (shells válidas del sistema)

**Capitulo 10 - Preparacion del arranque (Kernel + fstab + GRUB)**
- Tbala de montajes
  - Creacion y ajuste de /etc/fstab con:
    - raíz en la partición LFS
    - montajes virtuales requeridos: /proc, /sys, /run, /dev, /dev/shm
    - cgroup2 habilitado
 - Kernel Linux 6.16.1
   - Compilacion completa del kernel con configuracion minima funcional para VM
   - Generacion del kernel final:
     - /boot/vmlinuz-6.16.1-lfs-12.4
   - Instalacion de modulos:
     - /lib/modules/6.16.1
   - Verificacion de que el kernel, modulos y estructura de boot quedaron presentes

 **Incidente critico: GRUB afectado al sistema anfitrion**
 - Fallo
   - La instalacion de GRUB desde el entorno de LFS sobreescribio el cargador de arranque del disco, causando:
     - Desaparicion del arranque normal de Rocky Linux
     - Entrada a prompt de GRUB (grub>) con errores de detección de disco/partición
   - Resultado inmediato:
     - El host quedo sin menu funcional y sin arranque directo al sistema principal
   - Recuperacion:
     - Uso del ISO de Rocky Linux como medio de recuperacion:
       - Arranque en modo Rescue
       - Montaje del sistema real en /mnt/sysimage
       - chroot al sistema anfitrion
       - Reinstalacion y regeneracion de GRUB del host
     - Restauracion del menu del host y vuelta del arranque normal
   - Solucion final
     - Agregado correcto de entrada para LFS dentro del GRUB del host.

**Capitulo 11 - Finalizacion y primer arranque real**
- Validacion final de archivos criticos
  - int
  - inittab
  - fstab
  - kernel y modulos
- Revision de consistencia del arranque y estructura del sistema
- Arranque exitoso del sistema LFS finalizado:
  - Aparicion del prompt esperado
    - lfs-SO1 login:

### 10 de febrero del 2026
### Avannce: Reconstruccion completa del LFS 12.4-systemd desde backup Cap.7 + Kernel/GRUB + primer boot exitoso
### Participantes: Mateo
El dia de hoy se trato de rehacer el sistema con systemd como PID, partiendo del backup del cap 7, y dejandolo booteable

**Contexto y decision tecnica**
- Detectamos que el LFS anterior quedo armado con SysVinit, pero el TP exige systemd
- Migrar un LFS ya terminado de SysVinit -> systemd no es "parche", cambia el modelo de init/servicios, unidades, presents, dependencias y flujo de arranque
- La decision fue volver al backup del cap 7 y rehacer desde ahi siguiendo la variante LFS 12.4-systemd hasta el boot final

**Seguridad antes de tocar boot: snapshot de VirtualBox**
- Antes de cambiar kernel/GRUB hicimos snapshot para poder volver atrás si rompíamos el arranque
  - Intentamos usar VBoxManage desde dentro del Linux guest y dio “orden no encontrada” (porque VBoxManage está en el host donde está instalado VirtualBox, no dentro del guest).
  - Solución: snapshot desde la GUI de VirtualBox (Instántaneas).

**Volver al chroot correctamente (montajes + entorno limpio)**
- Para compilar/instalar dentro de LFS desde el host Rocky, reentramos al chroot montando pseudo-filesystems. Esto es clave porque sin /dev/pts, /proc, /sys, /run, los builds y herramientas (sudo/pty, device nodes, etc.) se rompen o se comportan raro
- Identificación de discos (punto crítico):
  -  Usamos lsblk para no “adivinar”:
    - sda (40G) = Rocky Linux (host del proyecto dentro de la VM) con LVM (rl-root, rl-swap)
    - sdb (25G) = disco dedicado a LFS; sdb1 contiene LFS
- Comando clave:
  - lsblk -f / lsblk
- Montaje del sistema LFS y pseudo-filesystem
  - Pasos (en el host como Root):
    - export LFS=/mnt/lfs
    - mount -v /dev/sdb1 $LFS
    - mount --bind /dev $LFS/dev
    - mount --bind /dev/pts $LFS/dev/pts
    - mount -t proc proc $LFS/proc
    - mount -t sysfs sysfs $LFS/sys
    - mount -t tmpfs tmpfs $LFS/run
- Entrada al chroot
  - Entramos con entorno limpio (env -i) y PATH mínimo:
    chroot "$LFS" /usr/bin/env -i \
    HOME=/root \
    TERM="$TERM" \
    PS1='(lfs chroot) \u:\w\$ ' \
    PATH=/usr/bin:/usr/sbin \
    /bin/bash --login
  source /etc/profile
 - Chequeos dentro del chroot:
   - uname -a → muestra kernel del host (normal en chroot).
   - echo $PATH
   - ls / para ver la raíz de LFS.

**Capítulo 8 – Construcción del sistema base (variante systemd)**
- En esta reconstrucción, el Capítulo 8 fue muy similar al que ya habíamos hecho en la variante SysVinit: se compila e instala el userland base (toolchain final, utilidades, librerías y herramientas del sistema) siguiendo el mismo flujo general del libro.
- Diferencias claves respecto a SysVinit:
  - Se construyó e integró systemd como init del sistema (en vez de SysVinit), lo que cambia el modelo de arranque y servicios (unidades .service, .target, etc.).
  - Se instalaron componentes necesarios para el ecosistema systemd (por ejemplo D-Bus y la generación/uso de machine-id, que systemd usa para identificación del sistema).
  - En la etapa final se aplicaron presets de systemd (ej.: systemctl preset-all) para habilitar los servicios que el libro deja como defaults en un LFS mínimo.
  - Varios make check/tests tuvieron fallos puntuales (normal en chroot/VM). Se documentaron y se continuó, porque no bloqueaban el sistema base y el libro no exige 100% de passing en todos los paquetes.\
- Resultado del cap 8:
  - systemctl --version (ya dentro del chroot) mostrando la versión de systemd.
  - ls -l /sbin/init mostrando que apunta a systemd (o /lib/systemd/systemd según layout).
  - Un systemctl preset-all (si lo corriste) o una captura de ls -l /etc/systemd/system/*.wants/ mostrando enlaces creados.

**Capítulo 9 – Configuración del sistema (variante systemd)**
- En este capítulo dejamos el sistema listo para arrancar como un Linux real: identidad, consola/idioma, red básica y archivos de configuración esenciales. A diferencia del Cap. 8 (que es “instalar paquetes”), acá es donde el sistema empieza a tener comportamiento propio.
- Introducción: qué logramos en esta etapa
  - Definimos la identidad del sistema (hostname, hosts).
  - Dejamos configurado el entorno de consola (teclado/fuente/locale).
  - Dejamos la red preparada para que al boot el sistema pueda levantar interfaz (base mínima).
  - Dejamos los archivos estándar que el sistema necesita para uso normal.
- Identidad del sistema (hostname + hosts)
  - Qué hicimos
    - Definimos el hostname del LFS.
    - Creamos /etc/hosts para resolver el propio nombre local.
  - Comandos / archivos
    - echo "lfs" > /etc/hostname (o el nombre que elegiste)
    - Editar /etc/hosts (ejemplo típico):
      - 127.0.0.1 localhost
      - 127.0.1.1 <hostname>

- Configuración de red (mínimo para systemd)
  - En systemd, la red suele manejarse con systemd-networkd (o NetworkManager en escritorios, pero en LFS base se suele usar networkd).
  - Qué hicimos / verificamos
    - Identificamos el nombre real de la interfaz (ej. enp0s3 en VirtualBox).
    - Dejamos lista la config mínima para que al boot la interfaz tenga IP (DHCP).

- Configuración regional: locale, consola y teclado
  - Qué hicimos
    - Definimos variables regionales y de idioma.
    - En systemd, en chroot no siempre podés usar localectl/timedatectl, así que se deja por archivos.
  - Archivos típicos
    - /etc/locale.conf (ej: LANG=en_US.UTF-8 o C.UTF-8)
    - /etc/vconsole.conf (ej: KEYMAP=us y FONT=Lat2-Terminus16)
- Archivos base de interacción del usuario
  - Qué hicimos
    - Creamos/ajustamos archivos estándar para consola y shells:
      - /etc/inputrc
      - /etc/profile
      - /etc/shells

**Cap. 10.1: Kernel 6.16.1 (configuración y compilación)**
- En linux-6.16.1/:
  - make defconfig
  - make menuconfig
- Mensaje sobre cgroups y systemd (lo que vimos)
  - Apareció algo como:
  - CPU controller ---> [CGROUP_SCHED]
  - advertencia: Group scheduling for SCHED_RR/FIFO (RT_GROUP_SCHED) puede hacer que systemd falle en features.
- Qué hicimos y por qué:
  - Dejamos cgroups habilitado (systemd lo necesita).
  - Desactivamos RT_GROUP_SCHED porque el propio libro avisa que puede causar malfunciones con systemd.

- Opciones extra 64-bit (MSI / IRQ remap / x2APIC)
  - El libro recomienda habilitar en este orden si aparecen:
  - PCI_MSI
  - IRQ_REMAP
  - X86_X2APIC
- Qué pasó: revisamos y ya estaban activadas en tu config (lo verificaste en menuconfig).

- Guardar configuración
  - Al salir de menuconfig aparece el cuadro para guardar:
    - confirmamos guardado en .config

**Bootloader (GRUB) + el error más crítico: disco equivocado / disco desconectado**
- Confirmación de raíz LFS
  - Revisamos:
    - /etc/fstab (dentro del chroot)
    - /dev/sdb1  /  ext4  defaults  1  1
  - y verificamos discos con lsblk.
- Instalación de GRUB y config manual
  - Instalamos GRUB apuntando al disco donde está LFS:
    - grub-install /dev/sdb
  - Luego creamos grub.cfg manual:
set default=0
set timeout=5
insmod part_gpt
insmod ext2
set root=(hd0,1)

menuentry "LFS 6.16.1" {
    linux /boot/vmlinuz-6.16.1-lfs-12.4-systemd root=/dev/sdb1 ro
}

- Incidente: VirtualBox storage y pérdida del disco LFS (25GB)
  - En un momento, tocando “Almacenamiento” en VirtualBox:
    - se desconectó (detach) el disco de 25GB (el de LFS).
    - Resultado al boot: Kernel panic – unable to mount root fs (unknown-block...).
  - Por qué pasó (explicación para el diario):
    - el kernel intentó montar root=/dev/sdb1, pero el disco ya no estaba, o cambió el orden de discos → la raíz no existía con ese nombre.
    - En VMs, /dev/sda y /dev/sdb pueden cambiar si cambiás puertos/orden.
   - Cómo lo resolvimos:
     - Re-adjuntamos el disco correcto (25GB) al controlador SATA.
     - Verificamos de nuevo con lsblk que el disco y la partición estaban presentes.
     - Volvimos a chroot para corregir/confirmar GRUB si era necesario.

**Resultado final: boot Exitoso**
- Despues de la correccion del tema del disco y confirmar GRUB/kernel
  - Booteamos desde GRUB y entramos al sistema
  - Aparecio el login: esperado del LFS


### 11 de Febrero del 2026
### Avance: Configuracion de red para el LFS
### Participante: Mateo
Habilitar un servicio de red real en el LFS booteado: servidor SSH accesible desde otra máquina (Rocky host), con red automática al arranque, y usarlo para transferir e integrar código.

**Compilación e instalación de OpenSSH (servidor)**
- Problema
  - LFS viene “mínimo” y no teníamos manera cómoda de entrar remotamente.
- Qué hicimos
  - Descargamos/descomprimimos openssh-9.8p1.
  - Configuramos para que use /etc/ssh como directorio de configuración.
  - Compilamos e instalamos.
- Comandos principales (resumen)
tar -xf openssh-9.8p1.tar.gz
cd openssh-9.8p1
./configure --prefix=/usr --sysconfdir=/etc/ssh
make
make install

**Configuración de seguridad (usuario sshd + llaves + config)**
- Problema
  - sshd no inicia si no tiene un entorno seguro (usuario dedicado + llaves del host).
- Qué hicimos
  - Creamos grupo/usuario sshd con UID/GID 50.
  - Generamos llaves del servidor (host keys) con ssh-keygen -A.
  - Ajustamos /etc/ssh/sshd_config para permitir login de root (solo para el TP / entorno controlado).
- Comandos principales (resumen)
groupadd -g 50 sshd
useradd  -c "sshd privsep" -d /var/lib/sshd -g sshd -s /bin/false -u 50 sshd

mkdir -p /var/lib/sshd
chmod 700 /var/lib/sshd

ssh-keygen -A

- Cambio clave en config
  - En /etc/ssh/sshd_config:
PermitRootLogin yes

**Red con systemd**
- Problema
  - El servicio de red fallaba y sin red no había SSH.
- Qué hicimos
  - Creamos usuarios de sistema requeridos:
    - systemd-network
    - systemd-resolve
  - Configuramos systemd-networkd con un .network para enp0s3.
  - Habilitamos networkd y resolved.
  - Arreglamos DNS enlazando /etc/resolv.conf a systemd.

- Comandos / acciones (resumen)
  - Archivo:
/etc/systemd/network/10-static-enp0s3.network (o DHCP si usaron DHCP)
  - Enable:
systemctl enable systemd-networkd
systemctl enable systemd-resolved
  - DNS:
ln -sfv /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf

**Habilitar y levantar el servicio SSH con systemd**
- Qué hicimos
  - Activamos el servicio para que arranque solo.
  - Lo iniciamos y verificamos puerto abierto.
- Comandos principales
systemctl enable sshd
systemctl start sshd
systemctl status sshd --no-pager


**Integración del script como comando del sistema (myshell)**
- Objetivo
  - Que el script pase a ser un “comando real” del sistema.
- Qué hicimos
  - Movimos el archivo a /usr/bin/myshell
  - Agregamos shebang y permisos
  - Probamos ejecución global
- Comandos principales
mv /root/shell.py /usr/bin/myshell
chmod +x /usr/bin/myshell
sed -i '1i #!/usr/bin/python3' /usr/bin/myshell
myshell


### OBSERVACION:
### Todos los anexos de envidencia del desarrollo del LFS estan la carpeta de envidencias





  
