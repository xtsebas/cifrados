### Sebastian Huertas 22295

# Ejercicio STEAM

## Parte 2: Análisis de Seguridad (20 puntos)

### 2.1 Variación de la Clave (5 puntos)
    - ¿Qué sucede cuando cambia la clave utilizada para generar el keystream? Demuestre con un ejemplo concreto.
    ![code](image.png)
    ![output](image-1.png)

### 2.2 Reutilización del Keystream (5 puntos)
    - ¿Qué riesgos de seguridad existen si reutiliza el mismo keystream para cifrar dos mensajes diferentes? Implemente un ejemplo que demuestre esta vulnerabilidad.
    - Sugerencia: Cifre dos mensajes con la misma clave y analice qué información puede extraer un atacante que intercepte ambos textos cifrados.

### 2.3 Longitud del Keystream (5 puntos)
    -¿Cómo afecta la longitud del keystream a la seguridad del cifrado? Considere tanto keystreams más cortos como más largos que el mensaje.

### 2.4 Consideraciones Prácticas (5 puntos)
    - ¿Qué consideraciones debe tener al generar un keystream en un entorno de producción real?Mencione al menos 3 aspectos críticos