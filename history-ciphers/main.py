import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cesar import cesar_cifrar, cesar_descifrar
from ROT13 import rot13, rot13_descifrar
from vigenere import vigenere_cifrar, vigenere_descifrar
from frequency import analisis_frecuencia
from criptografia.conversions.ascii_conversions import charToAscii


def main():
    print("=" * 60)
    print("EJEMPLO DE CIFRADO Y DESCIFRADO CESAR")
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
    print("EJEMPLO DE CIFRADO ROT13")
    print("=" * 60)
    
    print("\n--- ROT13 (Desplazamiento 13) ---")
    mensaje = "Hola Mundo"
    cifrado = rot13(mensaje)
    descifrado = rot13_descifrar(cifrado) 
    
    print(f"Mensaje original:  '{mensaje}'")
    print(f"Mensaje cifrado:   '{cifrado}'")
    print(f"Mensaje descifrado: '{descifrado}'\n")

    print("=" * 60)
    print("EJEMPLO DE CIFRADO Y DESCIFRADO VIGENERE")
    print("=" * 60)
    
    print("\n--- Clave: 'SECRETO' ---")
    mensaje2 = "Python es un lenguaje de programacion"
    clave2 = "SECRETO"
    cifrado2 = vigenere_cifrar(mensaje2, clave2)
    descifrado2 = vigenere_descifrar(cifrado2, clave2)
    
    print(f"Mensaje original:   '{mensaje2}'")
    print(f"Clave:              '{clave2}'")
    print(f"Mensaje cifrado:    '{cifrado2}'")
    print(f"Mensaje descifrado: '{descifrado2}'\n")

    print("=" * 60)
    print("ANALISIS DE FRECUENCIAS DE CARACTERES")
    print("=" * 60)
    
    print("\n--- Ejemplo 1: Texto simple ---")
    mensaje1 = "Hola Mundo"
    analisis_frecuencia(mensaje1, "Frecuencias: 'Hola Mundo'")
    
    print("\n--- Ejemplo 2: Texto cifrado (Cesar) ---")
    mensaje2_original = "Los cifrados son divertidos"
    mensaje2_cifrado = ""
    for char in mensaje2_original:
        ascii_val = charToAscii(char)
        nuevo_ascii = ascii_val + 5
        from criptografia.conversions.ascii_conversions import asciiValueToChar
        mensaje2_cifrado += asciiValueToChar(nuevo_ascii)
    
    print(f"Mensaje original:  '{mensaje2_original}'")
    print(f"Mensaje cifrado:   '{mensaje2_cifrado}'")
    analisis_frecuencia(mensaje2_cifrado, "Frecuencias: Texto cifrado con CCesar (desplazamiento 5)")
    
    print("\n--- Ejemplo 3: Texto largo ---")
    mensaje3 = """El analisis de frecuencias es una tecnica criptografica que 
    analiza la frecuencia de aparicion de caracteres en un texto. 
    Esta tecnica es util para romper cifrados de sustitucion simple."""
    
    analisis_frecuencia(mensaje3, "Frecuencias: Texto largo")


if __name__ == "__main__":
    main()
