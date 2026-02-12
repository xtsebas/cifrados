import random

def keystream_generator(seed, length):
    random.seed(seed)
    return [random.randint(0, 255) for _ in range(length)]

def encrypt(text, key):
    keystream = keystream_generator(key, len(text))
    encrypted = bytes(ord(char) ^ keystream_byte for char, keystream_byte in zip(text, keystream))
    return encrypted


def decrypt(encrypted, key):
    keystream = keystream_generator(key, len(encrypted))
    decrypted = ''.join(chr(byte ^ keystream_byte) for byte, keystream_byte in zip(encrypted, keystream))
    return decrypted

if __name__ == "__main__":
    key = "my_secret_key"
    plaintext = "Hello, World!"
    encrypted = encrypt(plaintext, key)
    print(f"Encrypted: {encrypted}")
    decrypted = decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}")