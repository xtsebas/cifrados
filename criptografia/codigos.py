from criptografia.conversions.ascii_conversions import (
    charToAscii, asciiValueToChar, asciiToBinary, binaryToAscii
)
from criptografia.conversions.base64_conversions import (
    charToBase64Value, base64ValueToChar, base64ToBinary, binaryToBase64
)
from criptografia.utils.binary_utils import binaryToDecimal, decimalToBinary

def textToBinary(text):
    return asciiToBinary(text)

def base64ValueToBinary(value):
    return decimalToBinary(value, 6)
