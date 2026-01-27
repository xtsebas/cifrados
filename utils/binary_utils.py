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


def decimalToBinary(decimal_value, bit_length):
    if decimal_value == 0:
        return '0' * bit_length

    binary = ''
    temp = decimal_value

    while temp > 0:
        residuo = temp % 2
        binary = str(residuo) + binary
        temp = temp // 2

    while len(binary) < bit_length:
        binary = '0' + binary

    return binary
