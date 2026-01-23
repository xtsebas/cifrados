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

def binaryToAscii(number):
    
    pass

def binaryToBase64():
    pass


text = "VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wcyBvdmVyIDEzIGxhenkgZG9ncy4="
binary_output = base64ToBinary(text)
print(binary_output)  