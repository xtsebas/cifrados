import random

def keystream_generator(seed, length):
    random.seed(seed)
    return [random.randint(0, 255) for _ in range(length)]

def encrypt(text, key):
    keystream = keystream_generator(key, len(text))
    encrypted_bytes = []

    for i, char in enumerate(text):
        char_byte = ord(char)
        keystream_byte = keystream[i]
        xor_result = char_byte ^ keystream_byte
        encrypted_bytes.append(xor_result)

    return bytes(encrypted_bytes)

def decrypt(encrypted, key):
    keystream = keystream_generator(key, len(encrypted))
    decrypted_chars = []

    for i, byte in enumerate(encrypted):
        keystream_byte = keystream[i]
        xor_result = byte ^ keystream_byte
        decrypted_chars.append(chr(xor_result))

    return ''.join(decrypted_chars)

if __name__ == "__main__":
    key = "my_secret_key"
    message1 = "Hello, World!"
    message2 = "Bye, World!"
    print(f"First Message: {message1}")
    encrypted = encrypt(message1, key)
    print(f"Encrypted: {encrypted}")

    print(f"Second Message: {message2}")
    encrypted2 = encrypt(message2, key)
    print(f"Encrypted: {encrypted2}")

    decrypted = decrypt(encrypted, key)
    print(f"Decrypted : {decrypted}")

    decrypted2 = decrypt(encrypted2, key)
    print(f"Decrypted : {decrypted2}")