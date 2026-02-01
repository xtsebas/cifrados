import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from criptografia.conversions.ascii_conversions import charToAscii, asciiValueToChar


def cesar_cifrar(mensaje, desplazamiento):
    mensaje_cifrado = ""
    
    for char in mensaje:
        ascii_value = charToAscii(char)
        
        nuevo_ascii = ascii_value + desplazamiento
        
        char_cifrado = asciiValueToChar(nuevo_ascii)
        mensaje_cifrado += char_cifrado
    
    return mensaje_cifrado


def cesar_descifrar(mensaje, desplazamiento):
    mensaje_descifrado = ""
    
    for char in mensaje:
        ascii_value = charToAscii(char)
        
        nuevo_ascii = ascii_value - desplazamiento
        
        char_descifrado = asciiValueToChar(nuevo_ascii)
        mensaje_descifrado += char_descifrado
    
    return mensaje_descifrado
