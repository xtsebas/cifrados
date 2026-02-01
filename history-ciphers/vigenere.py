import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from criptografia.conversions.ascii_conversions import charToAscii, asciiValueToChar, stringToUppercase


def vigenere_cifrar(mensaje, clave):
    if not clave:
        raise ValueError("La clave no puede estar vacía")
    
    mensaje_cifrado = ""
    clave_mayuscula = stringToUppercase(clave)
    clave_index = 0
    
    for char in mensaje:
        char_clave = clave_mayuscula[clave_index % len(clave_mayuscula)]
        desplazamiento = charToAscii(char_clave) - charToAscii('A')
        
        ascii_value = charToAscii(char)
        nuevo_ascii = ascii_value + desplazamiento
        char_cifrado = asciiValueToChar(nuevo_ascii)
        mensaje_cifrado += char_cifrado
        
        clave_index += 1
    
    return mensaje_cifrado


def vigenere_descifrar(mensaje, clave):
    if not clave:
        raise ValueError("La clave no puede estar vacía")
    
    mensaje_descifrado = ""
    clave_mayuscula = stringToUppercase(clave)
    clave_index = 0
    
    for char in mensaje:
        char_clave = clave_mayuscula[clave_index % len(clave_mayuscula)]
        desplazamiento = charToAscii(char_clave) - charToAscii('A')
        
        ascii_value = charToAscii(char)
        nuevo_ascii = ascii_value - desplazamiento
        char_descifrado = asciiValueToChar(nuevo_ascii)
        mensaje_descifrado += char_descifrado
        
        clave_index += 1
    
    return mensaje_descifrado