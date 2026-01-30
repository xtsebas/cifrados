def xorBit(bit1, bit2):
    if bit1 == bit2:
        return '0'
    else:
        return '1'


def xorBinary(binary1, binary2):
    binary1 = binary1.replace(' ', '')
    binary2 = binary2.replace(' ', '')

    if len(binary1) != len(binary2):
        return 'Error: Los binarios deben tener la misma longitud'

    result = ''

    for i in range(len(binary1)):
        result += xorBit(binary1[i], binary2[i])

    return result


def xorBinaryWithKey(binary, key):
    binary = binary.replace(' ', '')
    key = key.replace(' ', '')

    if not key:
        return 'Error: La clave no puede estar vacía'

    result = ''
    key_length = len(key)

    for i in range(len(binary)):
        key_index = i % key_length 
        result += xorBit(binary[i], key[key_index])

    return result


def xorTextWithKey(text, key):
    from criptografia.conversions.ascii_conversions import asciiToBinary

    binary_text = asciiToBinary(text)
    binary_key = asciiToBinary(key)

    result = xorBinaryWithKey(binary_text, binary_key)

    return result


def xorTextComplete(text, key):
    from criptografia.conversions.ascii_conversions import asciiToBinary, binaryToAscii

    binary_text = asciiToBinary(text)
    binary_key = asciiToBinary(key)

    binary_result = xorBinaryWithKey(binary_text, binary_key)

    text_result = binaryToAscii(binary_result)

    return text_result
