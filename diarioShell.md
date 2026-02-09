Fecha: 25/01/2026

(Registros de logs)

- Problema: En mi MacBook, el Shell no creaba los archivos de log en /var/log/shell.

- Causa: Entendí que /var/log es una zona protegida del Sistema Operativo. Mi usuario no tiene permisos de escritura ahí.

- Solución para pruebas: Se cambio temporalmente la ruta a ./logs para hacer las pruebas y luego se dejo /var/log/shell para el LFS.

Fecha: 26/01/2026

- Problema: Se mostraban archivos ocultos al usar ls (como .git).

- Solucion: Se cambio 'contenido = os.listdir(ruta_a_listar)' por 'contenido_total = os.listdir(ruta_a_listar)' y 'contenido = [item for item in contenido_total if not item.startswith(".")]'. Ignorando asi los archivos que empiecen con '.'

Fecha: 28/01/2026

- Se crearon las funciones de los comandos cp, rm y mkdir.

Fecha: 29/01/2026

- Se crearon las funciones de los comandos echo y cat.

- echo: unimos la lista de argumentos que se habia creado en el main con " ".join().

- cat: hacemos un for de los argumentos ingresados. Verificamos si existe, si es un directorio y luego hacemos print del archivo linea por linea.


Fecha: 09/02/2026

- Se crearon las funciones de los comandos grep y help.

- grep: el programa lee una linea a la vez hasta encontrar la palabra deseada, en caso de buscar en mas de un archivo se guarda el nombre del archivo en 'prefijo' y se imprime el nombre del archivo con la linea en la que se encuantra la palabra.

- help: muestra una lista de todos los comandos que programamos y explica para qué sirve cada uno. El programa recorre el diccionario mediante un bucle for, imprimiendo cada par comando-explicación de manera organizada.

- Problema: comando "help" no contaba con ejemplos para casos epsecificos.

- Solucion: Aplicamos la funciónalidad de explicar cada comando de manera especifica mediante help <comando>. Se añadieron los valores 'uso' y 'ejemplo' para cada llave para dar una explicación mas detallada del comando.

- Implementacion del comando 'reto': lanza un desafío al azar para que el usuario practique el uso de los comandos.
