import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cesar import cesar_cifrar, cesar_descifrar
from ROT13 import rot13, rot13_descifrar


def main():
    print("=" * 60)
    print("EJEMPLOS DE CIFRADO Y DESCIFRADO CÉSAR")
    print("=" * 60)
    
    print("\n--- Desplazamiento 5 ---")
    mensaje2 = "Hola Mundo"
    desplazamiento2 = 5
    cifrado2 = cesar_cifrar(mensaje2, desplazamiento2)
    descifrado2 = cesar_descifrar(cifrado2, desplazamiento2)
    
    print(f"Mensaje original:  '{mensaje2}'")
    print(f"Desplazamiento:    {desplazamiento2}")
    print(f"Mensaje cifrado:   '{cifrado2}'")
    print(f"Mensaje descifrado: '{descifrado2}'\n")

    print("=" * 60)
    print("EJEMPLOS DE CIFRADO ROT13")
    print("=" * 60)
    
    print("\n--- ROT13 (Desplazamiento 13) ---")
    mensaje = "Hola Mundo"
    cifrado = rot13(mensaje)
    descifrado = rot13_descifrar(cifrado) 
    
    print(f"Mensaje original:  '{mensaje}'")
    print(f"Mensaje cifrado:   '{cifrado}'")
    print(f"Mensaje descifrado: '{descifrado}'")


if __name__ == "__main__":
    main()
