from conversions.ascii_conversions import asciiToBinary, binaryToAscii
from conversions.base64_conversions import base64ToBinary, binaryToBase64, base64ToAscii
from investigation.cipher.xor_operations import xorBit, xorBinary, xorBinaryWithKey, xorTextWithKey, xorTextComplete


def print_separator():
    print("\n" + "=" * 60 + "\n")


def test_ascii_conversions():
    print("PRUEBAS DE CONVERSIONES ASCII <-> BINARIO")
    print_separator()

    # Prueba 1: ASCII to Binary
    text1 = "Hello"
    binary1 = asciiToBinary(text1)
    print(f"Texto: '{text1}'")
    print(f"Binario: {binary1}")

    # Prueba 2: Binary to ASCII
    back_to_text1 = binaryToAscii(binary1)
    print(f"De vuelta a texto: '{back_to_text1}'")
    print(f"Conversion correcta: {text1 == back_to_text1}")

    print_separator()

    # Prueba 3: Frase más larga
    text2 = "The quick brown fox"
    binary2 = asciiToBinary(text2)
    print(f"Texto: '{text2}'")
    print(f"Binario: {binary2}")

    back_to_text2 = binaryToAscii(binary2)
    print(f"De vuelta a texto: '{back_to_text2}'")
    print(f"Conversion correcta: {text2 == back_to_text2}")


def test_base64_conversions():
    print_separator()
    print("PRUEBAS DE CONVERSIONES BASE64 <-> BINARIO")
    print_separator()

    # Prueba 1: Base64 to Binary
    base64_text1 = "SGVsbG8="
    binary1 = base64ToBinary(base64_text1)
    print(f"Base64: {base64_text1}")
    print(f"Binario: {binary1}")

    # Prueba 2: Binary to Base64
    back_to_base64_1 = binaryToBase64(binary1)
    print(f"De vuelta a Base64: {back_to_base64_1}")
    print(f"Conversion correcta: {base64_text1 == back_to_base64_1}")

    print_separator()

    # Prueba 3: Texto más largo
    base64_text2 = "VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wcyBvdmVyIDEzIGxhenkgZG9ncy4="
    binary2 = base64ToBinary(base64_text2)
    print(f"Base64: {base64_text2}")
    print(f"Binario (primeros 100 chars): {binary2[:100]}...")

    back_to_base64_2 = binaryToBase64(binary2)
    print(f"De vuelta a Base64: {back_to_base64_2}")
    print(f"Conversion correcta: {base64_text2 == back_to_base64_2}")


def test_base64_to_ascii_direct():
    print_separator()
    print("PRUEBAS DE BASE64 -> ASCII (DIRECTO)")
    print_separator()

    # Prueba 1: Texto simple
    base64_1 = "RkxBR3tCQVNFNjRfREVTQ0lGUkFET30K"
    print(f"Base64: {base64_1}")
    ascii_1 = base64ToAscii(base64_1)
    print(f"ASCII: '{ascii_1}'")
    print(f"(Pasa por binario internamente)")

    # print_separator()

    # # Prueba 2: Texto más largo
    # base64_2 = "VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wcyBvdmVyIDEzIGxhenkgZG9ncy4="
    # print(f"Base64: {base64_2}")
    # ascii_2 = base64ToAscii(base64_2)
    # print(f"ASCII: '{ascii_2}'")

    # print_separator()

    # # Prueba 3: Palabra simple
    # base64_3 = "UHl0aG9u"
    # print(f"Base64: {base64_3}")
    # ascii_3 = base64ToAscii(base64_3)
    # print(f"ASCII: '{ascii_3}'")


def test_combined_conversions():
    print_separator()
    print("PRUEBAS DE CONVERSIONES COMBINADAS")
    print_separator()

    # ASCII -> Binary -> Base64 -> Binary -> ASCII
    original_text = "Python"
    print(f"Texto original: '{original_text}'")

    # ASCII to Binary
    binary_from_ascii = asciiToBinary(original_text)
    print(f"1. ASCII -> Binario: {binary_from_ascii}")

    # Binary to Base64
    base64_result = binaryToBase64(binary_from_ascii)
    print(f"2. Binario -> Base64: {base64_result}")

    # Base64 to Binary
    binary_from_base64 = base64ToBinary(base64_result)
    print(f"3. Base64 -> Binario: {binary_from_base64}")

    # Binary to ASCII
    final_text = binaryToAscii(binary_from_base64)
    print(f"4. Binario -> ASCII: '{final_text}'")

    print(f"\nConversion completa correcta: {original_text == final_text}")


def test_xor_operations():
    print_separator()
    print("PRUEBAS DE OPERACIONES XOR")
    print_separator()

    # Prueba 1: XOR bit a bit
    print("1. XOR Bit a Bit:")
    print(f"   0 XOR 0 = {xorBit('0', '0')}")
    print(f"   0 XOR 1 = {xorBit('0', '1')}")
    print(f"   1 XOR 0 = {xorBit('1', '0')}")
    print(f"   1 XOR 1 = {xorBit('1', '1')}")

    print_separator()

    # Prueba 2: XOR entre binarios
    print("2. XOR entre dos binarios:")
    binary1 = "10101010"
    binary2 = "11110000"
    result = xorBinary(binary1, binary2)
    print(f"   Binario 1: {binary1}")
    print(f"   Binario 2: {binary2}")
    print(f"   XOR:       {result}")

    print_separator()

    # Prueba 3: XOR con clave repetitiva
    print("3. XOR con clave (se repite si es necesario):")
    binary = "1100110011001100"
    key = "1010"
    result = xorBinaryWithKey(binary, key)
    print(f"   Binario: {binary}")
    print(f"   Clave:   {key} (se repite)")
    print(f"   XOR:     {result}")

    print_separator()

    # Prueba 4: Cifrado y descifrado de texto
    print("4. Cifrado y descifrado de texto con XOR:")
    original_text = "HELLO"
    key_text = "KEY"
    print(f"   Texto original: '{original_text}'")
    print(f"   Clave: '{key_text}'")

    # Convertir a binario
    binary_text = asciiToBinary(original_text)
    binary_key = asciiToBinary(key_text)
    print(f"   Texto (binario): {binary_text}")

    # Cifrar (mantener en binario)
    encrypted_binary = xorBinaryWithKey(binary_text, binary_key)
    print(f"   Cifrado (binario): {encrypted_binary}")

    # Descifrar (XOR es simétrico)
    decrypted_binary = xorBinaryWithKey(encrypted_binary, binary_key)
    decrypted = binaryToAscii(decrypted_binary)
    print(f"   Descifrado (binario): {decrypted_binary}")
    print(f"   Texto descifrado: '{decrypted}'")
    print(f"   Verificación: {original_text == decrypted}")


def test_xor_properties():
    print_separator()
    print("PROPIEDADES DEL XOR")
    print_separator()

    binary = "11110000"
    key = "10101010"

    # Propiedad 1: A XOR B XOR B = A
    xor1 = xorBinary(binary, key)
    xor2 = xorBinary(xor1, key)

    print("1. Propiedad: A XOR B XOR B = A")
    print(f"   A:           {binary}")
    print(f"   B:           {key}")
    print(f"   A XOR B:     {xor1}")
    print(f"   (A XOR B) XOR B: {xor2}")
    print(f"   Verificación: {binary == xor2}")

    print_separator()

    # Propiedad 2: A XOR A = 0
    xor_same = xorBinary(binary, binary)
    print("2. Propiedad: A XOR A = 0")
    print(f"   A:       {binary}")
    print(f"   A XOR A: {xor_same}")
    print(f"   Todo ceros: {xor_same == '00000000'}")


def test_xor_with_conversions():
    print_separator()
    print("CIFRADO XOR COMPLETO (BINARIO + BASE64)")
    print_separator()

    original_text = "Python"
    key = "XOR"

    print(f"Texto original: '{original_text}'")
    print(f"Clave: '{key}'")

    # Paso 1: Convertir texto a binario
    binary_text = asciiToBinary(original_text)
    print(f"\n1. Texto -> Binario: {binary_text}")

    # Paso 2: Cifrar con XOR
    encrypted_binary = xorTextWithKey(original_text, key)
    print(f"2. XOR cifrado: {encrypted_binary}")

    # Paso 3: Convertir a Base64 para transporte
    encrypted_base64 = binaryToBase64(encrypted_binary)
    print(f"3. Cifrado -> Base64: {encrypted_base64}")

    # Paso 4: Recibir y convertir de Base64 a binario
    received_binary = base64ToBinary(encrypted_base64)
    print(f"\n4. Base64 -> Binario: {received_binary}")

    # Paso 5: Descifrar con XOR
    binary_key = asciiToBinary(key)
    decrypted_binary = xorBinaryWithKey(received_binary, binary_key)
    print(f"5. XOR descifrado: {decrypted_binary}")

    # Paso 6: Convertir a texto
    decrypted_text = binaryToAscii(decrypted_binary)
    print(f"6. Binario -> Texto: '{decrypted_text}'")

    print(f"\nVerificación: {original_text == decrypted_text}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" SISTEMA DE CONVERSIONES Y CIFRADO MANUAL")
    print("=" * 60)

    # test_ascii_conversions()
    # test_base64_conversions()
    # test_base64_to_ascii_direct()
    # test_combined_conversions()
    # test_xor_operations()
    # test_xor_properties()
    # test_xor_with_conversions()
