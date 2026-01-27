"""
Demo de operaciones XOR sobre binarios
Todas las operaciones son implementadas manualmente sin usar funciones nativas de Python
"""

from cipher.xor_operations import xorBit, xorBinary, xorBinaryWithKey, xorTextWithKey, xorTextComplete
from conversions.ascii_conversions import asciiToBinary, binaryToAscii


def print_separator():
    print("\n" + "=" * 70 + "\n")


def test_xor_bit():
    print("1. PRUEBA DE XOR BIT A BIT")
    print_separator()
    print("Tabla de verdad XOR:")
    print(f"0 XOR 0 = {xorBit('0', '0')}")
    print(f"0 XOR 1 = {xorBit('0', '1')}")
    print(f"1 XOR 0 = {xorBit('1', '0')}")
    print(f"1 XOR 1 = {xorBit('1', '1')}")


def test_xor_binary():
    print_separator()
    print("2. PRUEBA DE XOR ENTRE DOS BINARIOS")
    print_separator()

    binary1 = "10101010"
    binary2 = "11110000"
    result = xorBinary(binary1, binary2)

    print(f"Binario 1: {binary1}")
    print(f"Binario 2: {binary2}")
    print(f"XOR:       {result}")
    print("\nVerificación manual:")
    print("1 XOR 1 = 0, 0 XOR 1 = 1, 1 XOR 1 = 0, 0 XOR 1 = 1,")
    print("1 XOR 0 = 1, 0 XOR 0 = 0, 1 XOR 0 = 1, 0 XOR 0 = 0")
    print(f"Esperado:  01011010")


def test_xor_with_key():
    print_separator()
    print("3. PRUEBA DE XOR CON CLAVE (CLAVE MÁS CORTA)")
    print_separator()

    binary = "1100110011001100"
    key = "1010"

    result = xorBinaryWithKey(binary, key)

    print(f"Binario:   {binary}")
    print(f"Clave:     {key} (se repite)")
    print(f"Resultado: {result}")
    print("\nLa clave '1010' se repite: 1010101010101010")
    print("1100110011001100 XOR 1010101010101010 = 0110011001100110")


def test_xor_text_encryption():
    print_separator()
    print("4. CIFRADO Y DESCIFRADO DE TEXTO CON XOR")
    print_separator()

    original_text = "HELLO"
    key = "KEY"

    print(f"Texto original: '{original_text}'")
    print(f"Clave: '{key}'")

    # Convertir a binario para mostrar
    binary_text = asciiToBinary(original_text)
    binary_key = asciiToBinary(key)

    print(f"\nTexto en binario: {binary_text}")
    print(f"Clave en binario: {binary_key}")

    # Cifrar
    encrypted_binary = xorTextWithKey(original_text, key)
    print(f"\nTexto cifrado (binario): {encrypted_binary}")

    # Convertir cifrado a texto para ver caracteres (puede no ser legible)
    encrypted_text = binaryToAscii(encrypted_binary)
    print(f"Texto cifrado (ASCII): {repr(encrypted_text)}")

    # Descifrar (aplicar XOR nuevamente con la misma clave)
    decrypted_binary = xorBinaryWithKey(encrypted_binary, binary_key)
    decrypted_text = binaryToAscii(decrypted_binary)

    print(f"\nTexto descifrado (binario): {decrypted_binary}")
    print(f"Texto descifrado: '{decrypted_text}'")

    print(f"\nVerificación: {original_text == decrypted_text}")


def test_xor_text_complete():
    print_separator()
    print("5. CIFRADO Y DESCIFRADO COMPLETO (FUNCIÓN DIRECTA)")
    print_separator()

    original_text = "Secret Message"
    key = "PASS"

    print(f"Texto original: '{original_text}'")
    print(f"Clave: '{key}'")

    # Cifrar
    encrypted_text = xorTextComplete(original_text, key)
    print(f"\nTexto cifrado: {repr(encrypted_text)}")

    # Descifrar (aplicar XOR nuevamente con la misma clave)
    decrypted_text = xorTextComplete(encrypted_text, key)
    print(f"Texto descifrado: '{decrypted_text}'")

    print(f"\nVerificación: {original_text == decrypted_text}")


def test_xor_properties():
    print_separator()
    print("6. PROPIEDADES DEL XOR")
    print_separator()

    binary = "11110000"
    key = "10101010"

    # Propiedad 1: A XOR B XOR B = A
    xor1 = xorBinary(binary, key)
    xor2 = xorBinary(xor1, key)

    print("Propiedad: A XOR B XOR B = A")
    print(f"A:         {binary}")
    print(f"B:         {key}")
    print(f"A XOR B:   {xor1}")
    print(f"(A XOR B) XOR B: {xor2}")
    print(f"Verificación: {binary == xor2}")

    print_separator()

    # Propiedad 2: A XOR A = 0
    xor_same = xorBinary(binary, binary)
    print("Propiedad: A XOR A = 0")
    print(f"A:       {binary}")
    print(f"A XOR A: {xor_same}")
    print(f"Todo ceros: {xor_same == '00000000'}")


def test_xor_with_base64():
    print_separator()
    print("7. CIFRADO XOR Y CONVERSIÓN A BASE64")
    print_separator()

    from conversions.base64_conversions import binaryToBase64, base64ToAscii

    original_text = "Python"
    key = "XOR"

    print(f"Texto original: '{original_text}'")
    print(f"Clave: '{key}'")

    # Cifrar con XOR
    encrypted_binary = xorTextWithKey(original_text, key)
    print(f"\nCifrado (binario): {encrypted_binary}")

    # Convertir a Base64 para transporte
    encrypted_base64 = binaryToBase64(encrypted_binary)
    print(f"Cifrado (Base64): {encrypted_base64}")

    # Simular transmisión: recibimos el Base64 y lo desciframos
    from conversions.base64_conversions import base64ToBinary

    received_binary = base64ToBinary(encrypted_base64)
    print(f"\nRecibido (binario): {received_binary}")

    # Descifrar
    binary_key = asciiToBinary(key)
    decrypted_binary = xorBinaryWithKey(received_binary, binary_key)
    decrypted_text = binaryToAscii(decrypted_binary)

    print(f"Descifrado: '{decrypted_text}'")
    print(f"\nVerificación: {original_text == decrypted_text}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print(" DEMOSTRACIÓN DE OPERACIONES XOR EN BINARIO")
    print(" Implementación manual sin funciones nativas de Python")
    print("=" * 70)

    test_xor_bit()
    test_xor_binary()
    test_xor_with_key()
    test_xor_text_encryption()
    test_xor_text_complete()
    test_xor_properties()
    test_xor_with_base64()

    print_separator()
    print("Todas las pruebas completadas!")
    print_separator()
