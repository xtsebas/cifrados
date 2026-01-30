import sys
sys.path.append('..')

from criptografia.investigation.cipher.xor_operations import xorTextComplete, xorBinaryWithKey
from criptografia.conversions.ascii_conversions import charToAscii, asciiValueToChar, asciiToBinary, binaryToAscii
from dynamics_keys import DynamicKeyGenerator


class DynamicKeyCipher:
    def __init__(self):
        self.key_generator = DynamicKeyGenerator()
        self.current_key = None

    def generate_dynamic_key(self, length, charset='alphanumeric'):
        self.current_key = self.key_generator.generate_random_key(length, charset)
        return self.current_key

    def set_key(self, key):
        self.current_key = key

    def expand_key(self, message_length):
        if not self.current_key:
            return None

        expanded_key = ""
        key_index = 0

        for i in range(message_length):
            expanded_key += self.current_key[key_index]
            key_index = (key_index + 1) % len(self.current_key)

        return expanded_key

    def encrypt_xor(self, message):
        if not self.current_key:
            return "Error: No hay llave establecida"

        encrypted = xorTextComplete(message, self.current_key)

        return encrypted

    def decrypt_xor(self, encrypted_message):
        if not self.current_key:
            return "Error: No hay llave establecida"

        decrypted = xorTextComplete(encrypted_message, self.current_key)

        return decrypted

    def encrypt_vigenere_style(self, message):
        if not self.current_key:
            return "Error: No hay llave establecida"

        encrypted = ""
        key_index = 0

        for i in range(len(message)):
            msg_ascii = charToAscii(message[i])
            key_ascii = charToAscii(self.current_key[key_index])

            encrypted_ascii = (msg_ascii + key_ascii) % 127

            if encrypted_ascii < 32:
                encrypted_ascii += 32

            encrypted += asciiValueToChar(encrypted_ascii)

            key_index = (key_index + 1) % len(self.current_key)

        return encrypted

    def decrypt_vigenere_style(self, encrypted_message):
        if not self.current_key:
            return "Error: No hay llave establecida"

        decrypted = ""
        key_index = 0

        for i in range(len(encrypted_message)):
            enc_ascii = charToAscii(encrypted_message[i])
            key_ascii = charToAscii(self.current_key[key_index])

            decrypted_ascii = (enc_ascii - key_ascii) % 127

            if decrypted_ascii < 32:
                decrypted_ascii += 95

            decrypted += asciiValueToChar(decrypted_ascii)

            key_index = (key_index + 1) % len(self.current_key)

        return decrypted

    def encrypt_stream_cipher(self, message):
        if not self.current_key:
            return "Error: No hay llave establecida"

        expanded_key = self.expand_key(len(message))
        encrypted = ""

        for i in range(len(message)):
            msg_ascii = charToAscii(message[i])
            key_ascii = charToAscii(expanded_key[i])

            encrypted_value = ((msg_ascii ^ key_ascii) + key_ascii) % 95 + 32

            encrypted += asciiValueToChar(encrypted_value)

        return encrypted

    def decrypt_stream_cipher(self, encrypted_message):
        if not self.current_key:
            return "Error: No hay llave establecida"

        expanded_key = self.expand_key(len(encrypted_message))
        decrypted = ""

        for i in range(len(encrypted_message)):
            enc_ascii = charToAscii(encrypted_message[i])
            key_ascii = charToAscii(expanded_key[i])

            enc_value = enc_ascii - 32
            decrypted_value = ((enc_value - key_ascii) % 95) ^ key_ascii

            if decrypted_value < 32:
                decrypted_value += 32
            elif decrypted_value > 126:
                decrypted_value = decrypted_value % 95 + 32

            decrypted += asciiValueToChar(decrypted_value)

        return decrypted

    def encrypt_polyalphabetic(self, message):
        if not self.current_key:
            return "Error: No hay llave establecida"

        encrypted = ""
        key_index = 0

        for i in range(len(message)):
            msg_ascii = charToAscii(message[i])
            key_ascii = charToAscii(self.current_key[key_index])

            if i % 3 == 0:
                result = (msg_ascii + key_ascii) % 95 + 32
            elif i % 3 == 1:
                result = (msg_ascii ^ key_ascii) % 95 + 32
            else:
                result = ((msg_ascii * 2) + key_ascii) % 95 + 32

            encrypted += asciiValueToChar(result)
            key_index = (key_index + 1) % len(self.current_key)

        return encrypted

    def decrypt_polyalphabetic(self, encrypted_message):
        if not self.current_key:
            return "Error: No hay llave establecida"

        decrypted = ""
        key_index = 0

        for i in range(len(encrypted_message)):
            enc_ascii = charToAscii(encrypted_message[i])
            key_ascii = charToAscii(self.current_key[key_index])

            enc_value = enc_ascii - 32

            if i % 3 == 0:
                result = (enc_value - key_ascii) % 95 + 32
            elif i % 3 == 1:
                result = (enc_value ^ key_ascii) % 95 + 32
            else:
                for test in range(32, 127):
                    if ((test * 2 + key_ascii) % 95 + 32) == enc_ascii:
                        result = test
                        break
                else:
                    result = 63

            decrypted += asciiValueToChar(result)
            key_index = (key_index + 1) % len(self.current_key)

        return decrypted