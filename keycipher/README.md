### Sebastian Huertas 22295

# Ejercicio STEAM

## Parte 2: Análisis de Seguridad (20 puntos)

### 2.1 Variación de la Clave (5 puntos)
- ¿Qué sucede cuando cambia la clave utilizada para generar el keystream? Demuestre con un ejemplo concreto.

![code](image.png)
![output](image-1.png)

Cuando se cambia la llave para desencriptar, genera un keystream diferente al que se uso para encriptar, porque el generador depende directamente de la seed. Como el cifrado funciona aplicando XOR, solo se puede revertir correctamente si se uso exactamente la misma secuencia de numeros. Al usarse otra llave, el XOR no recupero el texto original sino bytes aleatorios. Esos bytes no corresponden a caracteres validos, por eso aparece el error de codificacion al intentar imprimirlos


### 2.2 Reutilización del Keystream (5 puntos)
- ¿Qué riesgos de seguridad existen si reutiliza el mismo keystream para cifrar dos mensajes diferentes? Implemente un ejemplo que demuestre esta vulnerabilidad.
- Sugerencia: Cifre dos mensajes con la misma clave y analice qué información puede extraer un atacante que intercepte ambos textos cifrados.

![security](image-2.png)

Cuando se reutilizo el mismo keystream para cifrar dos mensajes distintos, se esta creando una vulnerabilidad grave porque en un cifrado tipo stream con XOR, si un atacante obtiene ambos textos cifrados puede hacer XOR entre ellos y eliminar el keystream, quedandose con el XOR de los dos mensajes originales, lo que permite recuperar informacion si conoce o adivina parte de uno de los mensajes. Por ejemplo, si hago C1 = M1 XOR K y C2 = M2 XOR K, entonces C1 XOR C2 = M1 XOR M2, y si el atacante sabe que M1 es "Hello World!", puede hacer (C1 XOR C2) XOR M1 y recuperar M2, demostrando que reutilizar la misma clave compromete completamente la confidencialidad


### 2.3 Longitud del Keystream (5 puntos)
    -¿Cómo afecta la longitud del keystream a la seguridad del cifrado? Considere tanto keystreams más cortos como más largos que el mensaje.

### 2.4 Consideraciones Prácticas (5 puntos)
    - ¿Qué consideraciones debe tener al generar un keystream en un entorno de producción real?Mencione al menos 3 aspectos críticos