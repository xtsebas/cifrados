from criptografia.utils.binary_utils import binaryToDecimal, decimalToBinary

def charToAscii(char):
    # Use Python's built-in ord() to handle all ASCII values (0-255)
    return ord(char)


def asciiValueToChar(ascii_value):
    # Use Python's built-in chr() to handle all ASCII values (0-255)
    # Clamp to valid range to avoid errors
    if 0 <= ascii_value <= 255:
        return chr(ascii_value)
    return '?'


def asciiToBinary(text):
    binary_result = ""
    for char in text:
        ascii_value = charToAscii(char)
        binary_result += decimalToBinary(ascii_value, 8)
    return binary_result


def binaryToAscii(binary_str):
    if not binary_str:
        return ''

    binary_str = binary_str.replace(' ', '')

    if len(binary_str) % 8 != 0:
        return 'Error: El binario debe ser múltiplo de 8 bits'

    result = ''

    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        decimal_value = binaryToDecimal(byte)
        char = asciiValueToChar(decimal_value)
        result += char

    return result
