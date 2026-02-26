# CIFRADOS 2025
<a id="readme-top"></a>

## 📜 Descripción

Repositorio del curso **Cifrados 2025** — Sebastian Huertas (22295). Contiene implementaciones de algoritmos criptográficos clásicos y modernos, utilidades de conversión, cifrados basados en llaves, un laboratorio de cifrado por bloques y una serie de desafíos CTF resueltos.

## 📂 Estructura del Proyecto

```
cifrados/
├── history-ciphers/        # Cifrados históricos/clásicos
├── criptografia/           # Biblioteca de utilidades criptográficas
├── criptografia_keys/      # Cifrados basados en llaves dinámicas
├── keycipher/              # Laboratorio de Stream Cipher (Keystream)
├── lab-block-cipher/       # Laboratorio de cifrado por bloques (DES-ECB)
└── CTF_lab/                # Desafíos Capture The Flag resueltos
```

<p align="right">(<a href="#readme-top">Ir al inicio</a>)</p>

---

## 🔐 Módulos

### 1. `history-ciphers/` — Cifrados Históricos

Implementaciones en Python de los cifrados clásicos más conocidos.

| Archivo | Descripción |
|---|---|
| `cesar.py` | Cifrado César: encriptación y desencriptación por desplazamiento ASCII |
| `vigenere.py` | Cifrado Vigenère: cifrado polialfabético con llave de texto |
| `ROT13.py` | ROT13: caso especial del cifrado César con desplazamiento 13 |
| `frequency.py` | Análisis de frecuencia para atacar cifrados de sustitución |
| `main.py` | Punto de entrada para ejecutar los ejemplos |

**Uso rápido:**
```python
from cesar import cesar_cifrar, cesar_descifrar
cifrado = cesar_cifrar("HOLA", 3)   # "KROD"
original = cesar_descifrar(cifrado, 3)  # "HOLA"

from vigenere import vigenere_cifrar, vigenere_descifrar
cifrado = vigenere_cifrar("HOLA", "CLAVE")
original = vigenere_descifrar(cifrado, "CLAVE")
```

---

### 2. `criptografia/` — Utilidades Criptográficas

Biblioteca de utilidades y funciones auxiliares usadas por los demás módulos.

```
criptografia/
├── ascii_dict.py              # Diccionario de valores ASCII
├── codigos.py                 # Códigos y constantes
├── main.py                    # Ejemplos de uso
├── conversions/
│   ├── ascii_conversions.py   # Conversiones entre caracteres, ASCII y binario
│   └── base64_conversions.py  # Codificación y decodificación Base64
├── investigation/
│   └── cipher/
│       └── xor_operations.py  # Operaciones XOR a nivel de texto y binario
└── utils/
```

---

### 3. `criptografia_keys/` — Cifrados con Llaves Dinámicas

Implementaciones de cifrado que utilizan llaves generadas dinámicamente.

| Archivo | Descripción |
|---|---|
| `dynamics_keys.py` | Generador de llaves aleatorias (alfanuméricas, etc.) |
| `dynamic_key_cipher.py` | Cifrador con llave dinámica: XOR, estilo-Vigenère, stream y polialfabético |
| `fixed_key_cipher.py` | Cifrador con llave fija |
| `custom_utilities.py` | Utilidades complementarias |
| `main.py` | Ejemplos y punto de entrada |

**Métodos disponibles en `DynamicKeyCipher`:**
- `encrypt_xor` / `decrypt_xor` — cifrado XOR directo
- `encrypt_vigenere_style` / `decrypt_vigenere_style` — cifrado estilo Vigenère
- `encrypt_stream_cipher` / `decrypt_stream_cipher` — cifrado de flujo
- `encrypt_polyalphabetic` / `decrypt_polyalphabetic` — cifrado polialfabético

---

### 4. `keycipher/` — Stream Cipher (Keystream)

Laboratorio de cifrado de flujo basado en generación de keystream mediante PRNG.

| Archivo | Descripción |
|---|---|
| `keystream.py` | Generador de keystream y funciones `encrypt`/`decrypt` usando XOR |
| `keystrea_test.py` | Pruebas unitarias (determinismo, diferentes llaves, longitudes) |
| `examples.py` | Ejemplos de cifrado con llaves de distintas longitudes |
| `README.md` | Análisis de seguridad: reutilización del keystream, longitud, PRNG vs CSPRNG |

**Uso rápido:**
```python
from keystream import encrypt, decrypt
encrypted = encrypt("Hello, World!", "my_secret_key")
decrypted = decrypt(encrypted, "my_secret_key")  # "Hello, World!"
```

---

### 5. `lab-block-cipher/` — Cifrado por Bloques (DES-ECB)

Laboratorio de cifrado por bloques usando DES en modo ECB implementado en Ruby con OpenSSL.

```
lab-block-cipher/
├── Gemfile             # Dependencias Ruby (openssl)
├── Gemfile.lock
└── src/
    ├── des_ecb.rb      # Cifrado/descifrado DES-ECB con padding PKCS#7 manual
    └── utils/
        ├── manual_padding.rb   # Implementación manual de padding PKCS#7
        └── key_generator.rb    # Generador de llaves DES
```

**Instalación y uso:**
```bash
cd lab-block-cipher
bundle install
ruby src/des_ecb.rb
```

---

### 6. `CTF_lab/` — Desafíos CTF

Documentación de los desafíos Capture The Flag completados, con desarrollo, análisis y conclusiones.

| Desafío | Tema | Flag |
|---|---|---|
| `Challenge1.md` | Exploración de archivos Linux y escalada de privilegios | `FLAG{LINUX_BASICS}` |
| `Challenge2.md` | Decodificación Base64 | `FLAG{BASE64_DESCIFRADO}` |
| `Challenge3.md` | Cifrado César y ROT13 | `FLAG{CESAR_CIFRADO}` / `FLAG{SECRET_FLAG_ROOT13}` |
| `Challenge4.md` | Análisis de frecuencia | `FLAG{CRYPTO_ANALYSIS}` |

---

## 🚀 Requisitos

- **Python 3.8+** — para los módulos `history-ciphers`, `criptografia`, `criptografia_keys` y `keycipher`
- **Ruby 3.x** + **Bundler** — para el módulo `lab-block-cipher`

## ⚙️ Instalación

```bash
# Clonar el repositorio
git clone https://github.com/xtsebas/cifrados.git
cd cifrados

# Instalar dependencias Ruby (para lab-block-cipher)
cd lab-block-cipher
bundle install
cd ..
```

No se requiere instalación adicional para los módulos Python; todas las dependencias son de la biblioteca estándar.

<p align="right">(<a href="#readme-top">Ir al inicio</a>)</p>

---

## 👤 Autor

**Sebastian Huertas** — Carné 22295

<!-- MARKDOWN LINKS & IMAGES -->
[Python]: https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[GitHub]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white
