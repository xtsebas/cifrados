def charToAscii(char):
    ascii_map = {
        ' ': 32, '!': 33, '"': 34, '#': 35, '$': 36, '%': 37, '&': 38, "'": 39,
        '(': 40, ')': 41, '*': 42, '+': 43, ',': 44, '-': 45, '.': 46, '/': 47,
        '0': 48, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54, '7': 55,
        '8': 56, '9': 57, ':': 58, ';': 59, '<': 60, '=': 61, '>': 62, '?': 63,
        '@': 64, 'a': 97, 'b': 98, 'c': 99, 'd': 100, 'e': 101, 'f': 102, 'g': 103,
        'h': 104, 'i': 105, 'j': 106, 'k': 107, 'l': 108, 'm': 109, 'n': 110, 'o': 111,
        'p': 112, 'q': 113, 'r': 114, 's': 115, 't': 116, 'u': 117, 'v': 118, 'w': 119,
        'x': 120, 'y': 121, 'z': 122, '[': 91, '\\': 92, ']': 93, '^': 94, '_': 95,
        '`': 96, '{': 123, '|': 124, '}': 125, '~': 126
    }
    return ascii_map.get(char, 0)


def asciiToBinary(ascii_value):
    if ascii_value == 0:
        return '00000000'

    binary = ''
    temp = ascii_value

    while temp > 0:
        residuo = temp % 2
        binary = str(residuo) + binary
        temp = temp // 2

    while len(binary) < 8:
        binary = '0' + binary

    return binary


def textToBinary(text):
    text = text.lower()
    binary_result = ""
    for char in text:
        ascii_value = charToAscii(char)
        binary_result += asciiToBinary(ascii_value)
    return binary_result

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


def base64ValueToBinary(value):
    if value < 0:
        return ''

    if value == 0:
        return '000000'

    binary = ''
    temp = value

    while temp > 0:
        residuo = temp % 2
        binary = str(residuo) + binary
        temp = temp // 2

    while len(binary) < 6:
        binary = '0' + binary

    return binary


def base64ToBinary(base64_text):
    binary_result = ""
    for char in base64_text:
        if char == '=':  
            continue
        base64_value = charToBase64Value(char)
        binary_result += base64ValueToBinary(base64_value)
    return binary_result

def binaryToDecimal(binary_str):
    if not binary_str:
        return 0

    decimal = 0
    power = 0

    for i in range(len(binary_str) - 1, -1, -1):
        if binary_str[i] == '1':
            value = 1
            for _ in range(power):
                value = value * 2
            decimal += value
        power += 1

    return decimal


def asciiValueToChar(ascii_value):
    char_map = {
        32: ' ', 33: '!', 34: '"', 35: '#', 36: '$', 37: '%', 38: '&', 39: "'",
        40: '(', 41: ')', 42: '*', 43: '+', 44: ',', 45: '-', 46: '.', 47: '/',
        48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7',
        56: '8', 57: '9', 58: ':', 59: ';', 60: '<', 61: '=', 62: '>', 63: '?',
        64: '@', 65: 'A', 66: 'B', 67: 'C', 68: 'D', 69: 'E', 70: 'F', 71: 'G',
        72: 'H', 73: 'I', 74: 'J', 75: 'K', 76: 'L', 77: 'M', 78: 'N', 79: 'O',
        80: 'P', 81: 'Q', 82: 'R', 83: 'S', 84: 'T', 85: 'U', 86: 'V', 87: 'W',
        88: 'X', 89: 'Y', 90: 'Z', 91: '[', 92: '\\', 93: ']', 94: '^', 95: '_',
        96: '`', 97: 'a', 98: 'b', 99: 'c', 100: 'd', 101: 'e', 102: 'f', 103: 'g',
        104: 'h', 105: 'i', 106: 'j', 107: 'k', 108: 'l', 109: 'm', 110: 'n', 111: 'o',
        112: 'p', 113: 'q', 114: 'r', 115: 's', 116: 't', 117: 'u', 118: 'v', 119: 'w',
        120: 'x', 121: 'y', 122: 'z', 123: '{', 124: '|', 125: '}', 126: '~'
    }
    return char_map.get(ascii_value, '?')


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

def binaryToBase64(binary_str):
    """Convierte un string binario a Base64"""
    if not binary_str:
        return ''

    binary_str = binary_str.replace(' ', '')

    remainder = len(binary_str) % 6

    if remainder != 0:
        padding_bits = 6 - remainder
        binary_str += '0' * padding_bits

    result = ''
    padding_chars = 0

    original_length = len(binary_str) - (padding_bits if remainder != 0 else 0)

    if remainder != 0:
        bytes_remainder = original_length % 24
        if bytes_remainder == 8:  
            padding_chars = 2
        elif bytes_remainder == 16:  
            padding_chars = 1

    for i in range(0, len(binary_str), 6):
        sextet = binary_str[i:i+6]
        if len(sextet) == 6:
            decimal_value = binaryToDecimal(sextet)
            char = base64ValueToChar(decimal_value)
            result += char

    result += '=' * padding_chars

    return result