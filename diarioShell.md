Fecha: 25/01/2026

1er problema (Registros de logs)

- Problema: En mi MacBook, el Shell no creaba los archivos de log en /var/log/shell.

- Causa: Entendí que /var/log es una zona protegida del Sistema Operativo. Mi usuario no tiene permisos de escritura ahí.

- Solución para pruebas: Se cambio temporalmente la ruta a ./logs para hacer las pruebas y luego se dejo /var/log/shell para el LFS.

