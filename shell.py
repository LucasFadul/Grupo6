#!/usr/bin/env python3

import os          # Para syscalls (chdir, listdir, fork, exec)... hablar con el kernel        
import datetime 
import readline   

# REGISTRO DE LOGS
LOG_DIR = "/var/log/shell" 
LOG_SHELL = f"{LOG_DIR}/shell.log"
LOG_ERROR = f"{LOG_DIR}/sistema_error.log"

def registrar_log(mensaje, es_error=False):
    # Aseguramos que la carpeta existe (importante para el LFS recién instalado)
    if not os.path.exists(LOG_DIR):
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
        except:
            return # Si no hay permisos, el shell sigue pero no loguea

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    archivo = LOG_ERROR if es_error else LOG_SHELL
    
    with open(archivo, "a") as f:
        f.write(f"[{timestamp}] {mensaje}\n")

#-------------------------------------------------------------------------------------------

# FUNCIONES DE COMANDOS 
def pwd(args):
    print(os.getcwd())
    registrar_log(f"Comando ejecutado: pwd")

def cd(args):
    try:
        ruta_destino = args[0] if args else os.path.expanduser("~")
        os.chdir(ruta_destino)
        registrar_log(f"Cambio de directorio a: {os.getcwd()}")
    except Exception as e:
        print(f"cd: {e}")
        registrar_log(f"Error en cd: {e}", es_error=True)

def ls(args):
    try:
        ruta = args[0] if args else "."
        contenido_total = os.listdir(ruta)
        contenido = sorted([item for item in contenido_total if not item.startswith(".")])
        
        for item in contenido:
            sufijo = "/" if os.path.isdir(os.path.join(ruta, item)) else ""
            print(f"{item}{sufijo}", end="  ")
        print()
        registrar_log(f"Comando ejecutado: ls en {ruta}")
    except Exception as e:
        print(f"ls: {e}")
        registrar_log(f"Error en ls: {e}", es_error=True)

def cp(args):
    if len(args) < 2:
        print("cp: faltan operandos (origen y destino)")
        return
    
    origen = args[0]
    destino = args[1]
    
    # 1. Verificar que el origen existe
    if not os.path.exists(origen):
        print(f"cp: no se puede encontrar '{origen}': No existe el archivo")
        return

    # 2. Impedir copiar directorios (el cp básico no lo hace sin -r)
    if os.path.isdir(origen):
        print(f"cp: -r no especificado; omitiendo directorio '{origen}'")
        return

    try:
        # 3. IMPLEMENTACIÓN MANUAL: Lectura y Escritura de buffers
        # Usamos 'rb' (read binary) y 'wb' (write binary) ... sirve con cualquier archivo
        with open(origen, 'rb') as f_origen:
            contenido = f_origen.read() # Leemos todo el contenido a memoria
            
        with open(destino, 'wb') as f_destino:
            f_destino.write(contenido) # Escribimos el contenido en el destino
            
        registrar_log(f"Copia manual exitosa: {origen} -> {destino}")
    
    except Exception as e:
        print(f"cp: error al copiar: {e}")
        registrar_log(f"Error en cp manual: {e}", es_error=True)

def rm(args):
    if not args:
        print("rm: falta un operando")
        return

    for nombre in args:
        if os.path.exists(nombre):
            try:
                # Verificamos si es un archivo (os.remove no borra carpetas)
                if os.path.isfile(nombre):
                    os.remove(nombre)  # Esta es la syscall manual para archivos
                    registrar_log(f"Archivo eliminado manualmente: {nombre}")
                
                # Si es una carpeta, usamos os.rmdir
                elif os.path.isdir(nombre):
                    os.rmdir(nombre)
                    registrar_log(f"Directorio eliminado manualmente: {nombre}")
            
            except Exception as e:
                print(f"rm: no se pudo borrar '{nombre}': {e}")
                registrar_log(f"Error al borrar {nombre}: {e}", es_error=True)
        else:
            print(f"rm: no se puede borrar '{nombre}': No existe el archivo o el directorio")

def mkdir(args):
    if not args:
        print("mkdir: falta un operando")
        return
    
    for nombre in args:
        try:
            os.mkdir(nombre)
            registrar_log(f"Directorio creado: {nombre}")
        except FileExistsError:
            print(f"mkdir: no se puede crear el directorio '{nombre}': El archivo ya existe")
        except FileNotFoundError:
            print(f"mkdir: no se puede crear el directorio '{nombre}': No existe el fichero o el directorio")
        except Exception as e:
            print(f"mkdir: error al crear '{nombre}': {e}")
            registrar_log(f"Error en mkdir ({nombre}): {e}", es_error=True)

def echo(args):
    resultado = " ".join(args)
    print(resultado)
    registrar_log(f"Comando echo ejecutado: {resultado}")   

def cat(args):
    if not args:
        print("cat: falta un nombre de archivo")
        registrar_log("ERROR cat: no se proporcionó archivo", es_error=True)
        return
    
    for nombre in args:
        # Verifica existencia
        if not os.path.exists(nombre):
            print(f"cat: {nombre}: No existe el archivo")
            registrar_log(f"ERROR cat: {nombre} no existe", es_error=True)
            continue
            
        # Verifica que no sea un directorio
        if os.path.isdir(nombre):
            print(f"cat: {nombre}: Es un directorio")
            registrar_log(f"ERROR cat: {nombre} es directorio", es_error=True)
            continue

        try:
            with open(nombre, 'r') as archivo:
                for linea in archivo:
                    # Usamos end="" para que no se repita el salto de linea
                    print(linea, end="")
            
            # Agregamos un salto de línea extra al final por si el archivo no termina en \n
            print() 
            registrar_log(f"Archivo visualizado: {nombre}")
            
        except Exception as e:
            print(f"cat: error al leer {nombre}: {e}")
            registrar_log(f"ERROR cat inesperado en {nombre}: {e}", es_error=True)

def grep(args):
    # grep necesita al menos 2 argumentos: la palabra y el archivo
    if len(args) < 2:
        print("grep: uso: grep <palabra> <archivo>")
        registrar_log("ERROR grep: faltan argumentos", es_error=True)
        return
    
    palabra_buscada = args[0]
    archivos = args[1:] # Pueden ser uno o varios archivos

    for nombre in archivos:
        if not os.path.exists(nombre):
            print(f"grep: {nombre}: No existe el archivo")
            continue
            
        if os.path.isdir(nombre):
            print(f"grep: {nombre}: Es un directorio")
            continue

        try:
            with open(nombre, 'r') as f:
                # Leemos línea por línea para cumplir con la eficiencia de memoria
                for n_linea, linea in enumerate(f, 1):
                    if palabra_buscada in linea:
                        # Si hay varios archivos, el grep real muestra el nombre
                        prefijo = f"{nombre}:" if len(archivos) > 1 else ""
                        # .strip() quita el salto de línea extra para que no se vea doble
                        print(f"{prefijo}{linea.strip()}")
            
            registrar_log(f"Búsqueda grep '{palabra_buscada}' en {nombre}")
            
        except Exception as e:
            print(f"grep: error al leer {nombre}: {e}")

def help_cmd(args):
    print("\n" + "="*60)
    print(" " * 20 + "SOPORTE DE EDUSHELL")
    print("="*60)
    
    comandos = {
        "pwd":   "Muestra la ruta del directorio de trabajo actual",
        "cd":    "Cambia el directorio actual. Si no se indica ruta, va a HOME",
        "ls":    "Lista archivos del directorio omitiendo ocultos",
        "cp":    "Copia archivos mediante flujo de bytes manual",
        "rm":    "Elimina archivos (os.remove) o directorios vacíos (os.rmdir).",
        "mkdir": "Crea un nuevo directorio (syscall pura os.mkdir).",
        "echo":  "Imprime los argumentos proporcionados en la salida estándar.",
        "cat":   "Muestra el contenido de archivos procesándolos línea por línea.",
        "grep":  "Busca una cadena de texto dentro de archivos (filtro manual).",
        "exit":  "Finaliza la sesión del EduShell y cierra el proceso actual.",
    }

    print("Comandos disponibles:")
    for cmd, desc in comandos.items():
        print(f"  \033[1;32m{cmd:10}\033[0m : {desc}")

    print("="*60 + "\n")
    registrar_log("Comando ejecutado: help")
#-------------------------------------------------------------------------------------------

def main():
    registrar_log("--- Sesión iniciada ---")
    
    while True:
        try:
            #Muestra la ruta actual
            ruta_actual = os.getcwd()
            prompt = f"\033[1;32mEduShell\033[0m:{ruta_actual}$ "
            
            linea = input(prompt).strip() #borra algun espacio al comienzo y al final
            if not linea: continue
                
            # Separar el comando de los argumentos
            partes = linea.split()
            comando = partes[0]
            argumentos = partes[1:]
            
            # exit
            if comando == "exit":
                registrar_log("--- Sesión finalizada ---")
                break
            # pwd
            elif comando == "pwd":
                pwd(argumentos)
            # cd
            elif comando == "cd":
                cd(argumentos)
            # ls
            elif comando == "ls":
                ls(argumentos)  
            # cp
            elif comando == "cp":
                cp(argumentos)
            # rm
            elif comando == "rm":
                rm(argumentos)
            # mkdir
            elif comando == "mkdir":
                mkdir(argumentos)
            # echo
            elif comando == "echo":
                echo(argumentos)
            # cat
            elif comando == "cat":
                cat(argumentos)
            # grep
            elif comando == "grep":
                grep(argumentos)
            # help
            elif comando == "help":
                help_cmd(argumentos)
            else:
                print(f"Comando '{comando}' no implementado.")
                
        except EOFError: # Captura Ctrl+D
            break
        except Exception as e:
            print(f"Error inesperado: {e}")
            registrar_log(f"ERROR: {str(e)}", es_error=True)

if __name__ == "__main__":
    main()