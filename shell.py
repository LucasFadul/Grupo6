#!/usr/bin/env python3

import os          # Para syscalls (chdir, listdir, fork, exec)... hablar con el kernel
import sys         # Para stdin, stdout y argumentos... salir del programa y manejar lo que escribe el usuario
import datetime    # Para el horario de los logs 

#-------------------------------------------------------------------------------------------

#REGISTRO DE LOGS

LOG_DIR = "/var/log/shell"                      #Direccion de la carpeta donde se guardan los logs
LOG_SHELL = f"{LOG_DIR}/shell.log"
LOG_ERROR = f"{LOG_DIR}/sistema_error.log"

def registrar_log(mensaje, es_error=False):
    """Registra eventos con timestamp. Requisito obligatorio."""
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

def main():
    registrar_log("--- Sesión iniciada ---")
    
    while True:
        try:
            #Muestra la ruta actual
            ruta_actual = os.getcwd()
            prompt = f"\033[1;32mEduShell\033[0m:{ruta_actual}$ "
            
            linea = input(prompt).strip()
            
            if not linea:
                continue
                
            # Separar el comando de los argumentos
            partes = linea.split()
            comando = partes[0]
            argumentos = partes[1:]
            
            #Exit
            if comando == "exit":
                registrar_log("--- Sesión finalizada ---")
                break
            
            #pwd
            elif comando == "pwd":
                # Lógica propia: no puedes usar os.system("pwd")
                print(os.getcwd())
                registrar_log(f"Comando ejecutado: pwd")
                
            else:
                # Aquí irá la lógica para comandos externos y otros builtins
                print(f"Comando '{comando}' no implementado aún.")
                
        except EOFError: # Captura Ctrl+D
            break
        except Exception as e:
            print(f"Error inesperado: {e}")
            registrar_log(f"ERROR: {str(e)}", es_error=True)

if __name__ == "__main__":
    main()