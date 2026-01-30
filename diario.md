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

### 22 de enero del 2026
### Avance: Migracion a SSD, Glibc y utilerias base
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

