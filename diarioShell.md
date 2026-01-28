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


