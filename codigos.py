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

def base64ToBinary():
    pass

def binaryToAscii():
    pass

def binaryToBase64():
    pass


text = "Hello World"
binary_output = textToBinary(text)
print(binary_output)  