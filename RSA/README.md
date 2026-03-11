# Laboratorio 4

## Sebastian Huertas 22295

### 1. El sistema usa RSA como mecanismo de intercambio de clave, protegiendo una clave AES que cifra el documento real.
a. ¿Explique por qué no cifrar el documento directamente con RSA?

RSA solo puede cifrar datos de tamaño menor al de la clave (ej. 245 bytes con una clave de 2048 bits). Los documentos legales superan ese limite. Además, RSA es ordenes de magnitud mas lento que AES. Por eso es mejor usar cifrado hibrido: AES cifra el documento y RSA cifra unicamente la clave AES
