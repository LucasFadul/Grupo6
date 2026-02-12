# Grupo6
#LFS & Shell 

Este repositorio documenta el trabajo realizado para la cátedra de **Sistemas Operativos**. Incluye el proceso de construcción de una distribución Linux desde las fuentes (**LFS**) y el desarrollo de un Shell con fines educativos (**EduShell**).

---

## Linux From Scratch (LFS)

En esta etapa, se construyó un sistema operativo completo compilando cada componente. El objetivo fue comprender la arquitectura interna del sistema y el flujo de ejecución desde el encendido hasta el prompt.

### 🧩 Componentes Clave
* **Toolchain:** Compilación de `binutils`, `gcc` y `glibc`.
* **Kernel:** Configuración y compilación del núcleo Linux optimizado para el hardware objetivo.
* **Gestión de Arranque:** Configuración de `GRUB` y diseño de scripts de inicio (init).
* **Estándar FHS:** Organización de la estructura de directorios (`/bin`, `/etc`, `/var`, etc.) siguiendo el estándar jerárquico de Linux.

---

## EduShell (Shell Educativa)

**EduShell** es una terminal interactiva desarrollada en Python. A diferencia de las shells comunes, su arquitectura está diseñada para **enseñar** mientras se utiliza.

### 🌟 Funcionalidades Destacadas
* **Ayuda Técnica Dinámica:** El comando `help <comando>` desglosa la utilidad del comando, su **syscall** asociada y un ejemplo de uso real.
* **Sistema de Retos:** Comando `reto` que asigna tareas técnicas aleatorias al usuario.


### 📊 Comandos Implementados

| Comando | Función Educativa | Concepto Técnico (Syscall/Lib) |
| :--- | :--- | :--- |
| `ls` | Lista el contenido del directorio actual. | `os.listdir()` |
| `cd` | Cambia el directorio de trabajo del proceso. | `os.chdir()` |
| `pwd` | Muestra la ruta absoluta del directorio actual. | `os.getcwd()` |
| `mkdir` | Crea nuevos directorios en la jerarquía. | `os.mkdir()` |
| `rm` | Elimina archivos o directorios permanentemente. | `os.remove()` / `os.rmdir()` |
| `cp` | Copia archivos garantizando integridad de datos. | `shutil.copy()` / `open.read()` |
| `cat` | Lee y concatena el contenido de archivos. | `file.read()` |
| `echo` | Imprime texto o lo redirige a un archivo (`>`). | `sys.stdout` / `file.write()` |
| `grep` | Filtra contenido mediante búsqueda de patrones. | Lectura secuencial y `re` (regex) |
| `help` | Manual dinámico con enfoque en Syscalls. | Diccionario de metadatos |
| `reto` | Generador de desafíos técnicos aleatorios. | Gamificación de terminal |
| `exit` | Finaliza la sesión de la EduShell de forma segura. | `sys.exit()` / Terminación de proceso |


---

## 📂 Estructura del Repositorio

```bash
.
├── README.md                # Documentación principal del proyecto
├── diario.md                # Bitácora general del trabajo (LFS)
├── diarioShell.md           # Bitácora específica del desarrollo de EduShell
├── src/                     # Código fuente de la aplicación
│   └── shell.py             # Intérprete de comandos (REPL) y lógica de retos
├── docs/                    # Capturas de pantalla y evidencias del sistema
│   └── *.png                # Capturas de la instalación de LFS y pruebas de Shell
└── tests/                   # Archivos de prueba para validación de comandos
