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

            # Comando cd
            elif comando == "cd":
                try:
                    # Si no hay argumentos, vamos a 'home'
                    if not argumentos:
                        ruta_destino = os.path.expanduser("~")
                    else:
                        # Tomamos el primer argumento (la ruta)
                        ruta_destino = argumentos[0]
                    
                    # La syscall mágica para cambiar de directorio
                    os.chdir(ruta_destino)
                    registrar_log(f"Cambio de directorio a: {os.getcwd()}")
                
                except FileNotFoundError:
                    mensaje = f"cd: No existe el directorio: {ruta_destino}"
                    print(mensaje)
                    registrar_log(mensaje, es_error=True)
                except NotADirectoryError:
                    mensaje = f"cd: {ruta_destino} no es un directorio"
                    print(mensaje)
                    registrar_log(mensaje, es_error=True)
                except PermissionError:
                    mensaje = f"cd: Permiso denegado: {ruta_destino}"
                    print(mensaje)
                    registrar_log(mensaje, es_error=True)
            
            # Comando ls
            elif comando == "ls":
                try:
                    # Si no hay argumentos, listamos la ruta actual (.)
                    # Si hay argumentos, intentamos listar la primera ruta que nos den
                    ruta_a_listar = argumentos[0] if argumentos else "."
                    
                    # 1. Obtenemos todo
                    contenido_total = os.listdir(ruta_a_listar)
                    
                    # 2. Filtramos: Solo nos quedamos con lo que NO empieza con "."
                    contenido = [item for item in contenido_total if not item.startswith(".")]
                    
                    contenido.sort()
                    
                    for item in contenido:
                        # Un pequeño toque: poner '/' al final si es una carpeta
                        if os.path.isdir(os.path.join(ruta_a_listar, item)):
                            print(f"{item}/", end="  ")
                        else:
                            print(item, end="  ")
                    print() # Salto de línea al final
                    
                    registrar_log(f"Comando ejecutado: ls en {ruta_a_listar}")
                
                except Exception as e:
                    mensaje = f"ls: {e}"
                    print(mensaje)
                    registrar_log(mensaje, es_error=True)

            #Comando no implementado    
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