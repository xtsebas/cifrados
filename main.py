from conversions.ascii_conversions import asciiToBinary, binaryToAscii
from conversions.base64_conversions import base64ToBinary, binaryToBase64


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


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" SISTEMA DE CONVERSIONES MANUAL")
    print("=" * 60)

    test_ascii_conversions()
    test_base64_conversions()
    test_combined_conversions()
