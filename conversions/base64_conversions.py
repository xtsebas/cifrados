from utils.binary_utils import binaryToDecimal, decimalToBinary


def charToBase64Value(char):
    base64_map = {
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7,
        'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15,
        'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23,
        'Y': 24, 'Z': 25, 'a': 26, 'b': 27, 'c': 28, 'd': 29, 'e': 30, 'f': 31,
        'g': 32, 'h': 33, 'i': 34, 'j': 35, 'k': 36, 'l': 37, 'm': 38, 'n': 39,
        'o': 40, 'p': 41, 'q': 42, 'r': 43, 's': 44, 't': 45, 'u': 46, 'v': 47,
        'w': 48, 'x': 49, 'y': 50, 'z': 51, '0': 52, '1': 53, '2': 54, '3': 55,
        '4': 56, '5': 57, '6': 58, '7': 59, '8': 60, '9': 61, '+': 62, '/': 63
    }
    return base64_map.get(char, -1)


def base64ValueToChar(value):
    base64_chars = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
        'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
        'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
        'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w', 'x', 'y', 'z', '0', '1', '2', '3',
        '4', '5', '6', '7', '8', '9', '+', '/'
    ]
    if 0 <= value <= 63:
        return base64_chars[value]
    return ''


def base64ToBinary(base64_text):
    binary_result = ""
    for char in base64_text:
        if char == '=':
            continue
        base64_value = charToBase64Value(char)
        binary_result += decimalToBinary(base64_value, 6)
    return binary_result


def binaryToBase64(binary_str):
    if not binary_str:
        return ''

    binary_str = binary_str.replace(' ', '')

    remainder_6 = len(binary_str) % 6
    if remainder_6 != 0:
        padding_bits = 6 - remainder_6
        binary_str += '0' * padding_bits

    result = ''
    for i in range(0, len(binary_str), 6):
        sextet = binary_str[i:i+6]
        if len(sextet) == 6:
            decimal_value = binaryToDecimal(sextet)
            char = base64ValueToChar(decimal_value)
            result += char

    padding_chars = 0
    result_length = len(result)
    remainder_4 = result_length % 4
    if remainder_4 != 0:
        padding_chars = 4 - remainder_4
        result += '=' * padding_chars

    return result
