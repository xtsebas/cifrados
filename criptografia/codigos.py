from conversions.ascii_conversions import (
    charToAscii, asciiValueToChar, asciiToBinary, binaryToAscii
)
from conversions.base64_conversions import (
    charToBase64Value, base64ValueToChar, base64ToBinary, binaryToBase64
)
from .utils.binary_utils import binaryToDecimal, decimalToBinary

def textToBinary(text):
    return asciiToBinary(text)

def base64ValueToBinary(value):
    return decimalToBinary(value, 6)
