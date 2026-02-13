import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from keycipher.keystream import decrypt, encrypt


examples = [
    ("Hello World!", "key123"),
    ("Criptografia", "segura456"),
    ("Stream Cipher Test", "clave789")
]

for i, (message, key) in enumerate(examples, 1):
    print(f"\nEJEMPLO {i}")
    print(f"Clave utilizada: {key}")
    print(f"Texto plano original: {message}")

    encrypted = encrypt(message, key)
    print(f"Texto cifrado (hex): {encrypted.hex()}")
    
    decrypted = decrypt(encrypted, key)
    print(f"Texto descifrado: {decrypted}")