## Sebastian Huertas 22295

# Parte 2: Analisis de Seguridad (25 puntos)

## 2.1 Análisis de Tamaños de Clave. Pregunta: ¿Qué tamaño de clave está usando para DES, 3DES y AES?

### Tamaños de clave utilizados

| Algoritmo | Tamano nominal | Tamano efectivo | Bytes |
|-----------|---------------|-----------------|-------|
| DES       | 64 bits       | 56 bits         | 8     |
| 3DES (op. 2) | 128 bits   | 112 bits*       | 16    |
| 3DES (op. 3) | 192 bits   | 112 bits*       | 24    |
| AES       | 256 bits      | 256 bits        | 32    |

---

### DES — 64 bits nominales / 56 bits efectivos (8 bytes)

De los 64 bits de la clave DES, 8 bits son de paridad (uno por byte) y no participan en el cifrado. La clave funcional es de solo 56 bits.

**Por que DES se considera inseguro hoy?**

DES es inseguro porque su espacio de claves de solo 2^56 (~7.2 x 10^16 combinaciones) es demasiado pequeno para los estandares actuales; en 1998 la maquina EFF "Deep Crack" (USD 250,000) lo rompio en 56 horas evaluando ~9 x 10^10 claves/segundo, y en 2008 COPACOBANA lo logro en ~7 dias con USD 10,000 en FPGAs. Con hardware moderno (FPGA o GPU cluster) que evalua entre 10^12 y 10^13 claves/segundo, el espacio completo se recorre en aproximadamente 1 a 2 horas, haciendo a DES completamente inviable para uso real.

**Calculo de fuerza bruta con hardware moderno**

```
Espacio de claves : 2^56  = 7.2 x 10^16 claves
Velocidad estimada: 10^13 claves/segundo (FPGA/GPU cluster, 2024)

Tiempo maximo     : 7.2 x 10^16 / 10^13 = 7,200 segundos ~ 2 horas
Tiempo promedio   : ~1 hora  (se recorre la mitad del espacio en promedio)
```

---

### 3DES — 128 o 192 bits nominales / 112 bits efectivos

3DES aplica DES tres veces (Encrypt-Decrypt-Encrypt). Con 2 claves de 8 bytes (opcion 2) el espacio nominal es 2^128, pero el ataque meet-in-the-middle lo reduce a 2^112.

**Calculo de fuerza bruta**

```
Espacio efectivo  : 2^112 = 5.19 x 10^33 claves
Velocidad estimada: 10^18 claves/segundo (hipotetico supercomputador futuro)

Tiempo            : 5.19 x 10^33 / 10^18 = 5.19 x 10^15 segundos
                  ~ 164,000,000 anos (164 millones de anos)
```

---

### AES-256 — 256 bits efectivos (32 bytes)

**Calculo de fuerza bruta**

```
Espacio de claves : 2^256 = 1.16 x 10^77 claves
Velocidad estimada: 10^18 claves/segundo (hipotetico supercomputador futuro)

Tiempo            : 1.16 x 10^77 / 10^18 = 1.16 x 10^59 segundos
                  ~ 3.67 x 10^51 anos

Edad del universo : ~1.38 x 10^10 anos

Relacion          : el tiempo de ataque es ~2.66 x 10^41 veces la edad del universo
```

---

### Snippet de referencia — generacion de claves

El codigo que genera las claves para los tres algoritmos esta en un unico archivo:

```
src/utils/key_generator.rb
```

| Funcion            | Descripcion                                      |
|--------------------|--------------------------------------------------|
| `generate_des_key` | Genera 8 bytes aleatorios (clave DES)            |
| `generate_3des_key`| Genera 16 o 24 bytes segun `key_option` (3DES)   |
| `generate_aes_key` | Genera 32 bytes para AES-256 (`key_size: 256`)   |

![key_generator](image.png)


## 2.2 Comparación de Modos de Operación

### Modos implementados por algoritmo

| Algoritmo | Modo | Archivo |
|-----------|------|---------|
| DES       | ECB  | `src/des_ecb.rb` |
| 3DES      | CBC  | `src/des3_cbc.rb` |
| AES       | ECB y CBC | `src/aes_ecb.rb`, `src/aes_cbc.rb` |

---

### Diferencias fundamentales entre ECB y CBC

**ECB (Electronic Codebook)**
Cada bloque de 16 bytes del plaintext se cifra de forma completamente independiente con la misma clave. Esto significa que dos bloques con el mismo contenido siempre producen exactamente el mismo ciphertext, sin importar su posicion en el mensaje. No requiere IV.

**CBC (Cipher Block Chaining)**
Antes de cifrar cada bloque, se hace XOR con el bloque de ciphertext anterior. El primer bloque se combina con un IV aleatorio. Esto rompe cualquier dependencia entre bloques identicos: aunque dos bloques tengan el mismo plaintext, su ciphertext sera diferente porque el resultado previo es distinto en cada posicion.

| Caracteristica        | ECB                        | CBC                          |
|-----------------------|----------------------------|------------------------------|
| Bloques independientes| Si                         | No (encadenados)             |
| IV requerido          | No                         | Si (aleatorio)               |
| Determinista          | Si (misma clave = mismo CT)| No (IV distinto cada vez)    |
| Revela patrones       | Si                         | No                           |
| Parallelizable        | Si (cifrado y descifrado)  | Solo descifrado              |

---

### Se puede notar la diferencia en una imagen?

Si, y de forma muy evidente. La imagen de prueba tiene cuatro cuadrantes de color solido (rojo, verde, azul, blanco). Cada cuadrante contiene miles de pixeles identicos, lo que genera miles de bloques AES con el mismo contenido.

- **ECB**: bloques identicos → ciphertext identico → los cuadrantes siguen siendo
  visibles como regiones uniformes. La forma y estructura de la imagen original
  se preserva por completo en la imagen cifrada.

- **CBC**: cada bloque se mezcla con el anterior → aunque el plaintext se repita,
  el ciphertext es diferente en cada posicion. La imagen cifrada es indistinguible
  de ruido aleatorio.

### Imagenes de comparacion

| Original | Cifrada con ECB | Cifrada con CBC |
|----------|----------------|-----------------|
| ![original](images/demo_original.bmp) | ![ecb](images/demo_ecb.bmp) | ![cbc](images/demo_cbc.bmp) |

---

### Codigo exacto para generar las imagenes

El codigo esta repartido en dos archivos. Referencia de lineas:

**`src/image_cipher.rb` — funciones de cifrado de imagen**

| Funcion | Descripcion |
|---------|-------------|
| `encrypt_bmp_ecb` | Lee BMP, cifra pixeles con AES-ECB, escribe resultado |
| `encrypt_bmp_cbc` | Lee BMP, cifra pixeles con AES-CBC (IV incluido), escribe resultado |

![alt text](image-1.png)
![alt text](image-2.png)

**`tests/test_image_cipher.rb` — demo que genera los archivos**

![alt text](image-3.png)


## 2.3 Vulnerabilidad de ECB. Pregunta: ¿Por qué no debemos usar ECB en datos sensibles?

### Bloques identicos producen ciphertext identico

ECB cifra cada bloque de 16 bytes de forma totalmente independiente. Si dos bloques
del plaintext son iguales, sus ciphertexts seran exactamente iguales con la misma
clave. Esto rompe la confidencialidad porque un observador puede detectar patrones
en el ciphertext sin necesidad de conocer la clave.

Mensaje de prueba: `"ATAQUE!!ATAQUE!!"` repetido 3 veces (3 bloques identicos de 16 bytes).

```
Plaintext:
  Bloque 0: "ATAQUE!!ATAQUE!!"
  Bloque 1: "ATAQUE!!ATAQUE!!"   <- identico al bloque 0
  Bloque 2: "ATAQUE!!ATAQUE!!"   <- identico al bloque 0

ECB — ciphertext:
  Bloque 0: a3f8... [16 bytes]
  Bloque 1: a3f8... [16 bytes]   <- IGUAL que bloque 0
  Bloque 2: a3f8... [16 bytes]   <- IGUAL que bloque 0
  => Bloque 0 == Bloque 1 == Bloque 2: true
  => Un atacante sabe que el plaintext se repite, sin descifrar nada.

CBC — ciphertext:
  IV       : 9c2e... [16 bytes aleatorios]
  Bloque 0: d471... [16 bytes]
  Bloque 1: 08ba... [16 bytes]   <- diferente
  Bloque 2: f3c1... [16 bytes]   <- diferente
  => Bloque 0 == Bloque 1: false
  => No se puede inferir ninguna relacion entre bloques.
```

![alt text](image-4.png)

---

### Que informacion puede filtrar ECB en escenarios reales?

**Escenario 1 — transacciones bancarias**

Un sistema cifra registros de 16 bytes por transaccion con ECB. Dos transferencias
de $1000 producen exactamente el mismo bloque cifrado. Un atacante que intercepta
el trafico puede detectar que dos operaciones son identicas sin conocer su contenido,
contar cuantas veces se repite una operacion, y realizar un ataque de replay
reenviando un bloque cifrado de $1000 para duplicar la transaccion, porque el
servidor lo acepta como valido (ECB no tiene integridad ni dependencia de posicion).

**Escenario 2 — cifrado de contrasenas o tokens**

Si una base de datos cifra contrasenas con ECB y la misma clave, dos usuarios con
la misma contrasena tendran el mismo ciphertext. Un atacante con acceso a la BD
puede identificar usuarios con contrasenas identicas sin descifrarlas, y usar
tablas de bloques precomputados de forma similar a rainbow tables.

**Escenario 3 — imagenes y multimedia**

Como demuestra el demo visual (seccion 2.2), los patrones de la imagen original
siguen siendo visibles en la imagen cifrada con ECB. La estructura del contenido
queda expuesta aunque no se pueda reproducir directamente.

---
