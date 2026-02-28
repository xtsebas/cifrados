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


