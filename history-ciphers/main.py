import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cesar import cesar_cifrar, cesar_descifrar


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
    print(f"Mensaje descifrado: '{descifrado2}'")


if __name__ == "__main__":
    main()
