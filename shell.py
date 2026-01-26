#!/usr/bin/env python3

import os          # Para syscalls (chdir, listdir, fork, exec)... hablar con el kernel
import sys         # Para stdin, stdout y argumentos... salir del programa y manejar lo que escribe el usuario
import datetime    

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
    pass

def rm(args):
    pass

def mkdir(args):
    pass

def echo(args):
    pass

def cp(args):
    pass

def cat(args):
    pass

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
            
            else:
                print(f"Comando '{comando}' no implementado aún.")
                
        except EOFError: # Captura Ctrl+D
            break
        except Exception as e:
            print(f"Error inesperado: {e}")
            registrar_log(f"ERROR: {str(e)}", es_error=True)

if __name__ == "__main__":
    main()