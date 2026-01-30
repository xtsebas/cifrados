import sys
sys.path.append('..')

from criptografia.investigation.cipher.xor_operations import xorTextComplete
from criptografia.conversions.ascii_conversions import charToAscii, asciiValueToChar
from dynamics_keys import DynamicKeyGenerator


class FixedKeyCipher:
    def __init__(self, key_length):
        self.key_length = key_length
        self.key_generator = DynamicKeyGenerator()
        self.current_key = None

    def generate_fixed_key(self, charset='alphanumeric'):
        self.current_key = self.key_generator.generate_random_key(self.key_length, charset)
        return self.current_key

    def set_key(self, key):
        if len(key) != self.key_length:
            return False
        self.current_key = key
        return True

    def adjust_message_length(self, message):
        if len(message) < self.key_length:
            while len(message) < self.key_length:
                message += ' '
        elif len(message) > self.key_length:
            message = message[:self.key_length]

        return message

    def encrypt_xor(self, message):
        if not self.current_key:
            return "Error: No hay llave establecida"

        adjusted_message = self.adjust_message_length(message)

        encrypted = xorTextComplete(adjusted_message, self.current_key)

        return encrypted

    def decrypt_xor(self, encrypted_message):
        if not self.current_key:
            return "Error: No hay llave establecida"

        decrypted = xorTextComplete(encrypted_message, self.current_key)

        return decrypted

    def encrypt_caesar_shift(self, message):
        if not self.current_key:
            return "Error: No hay llave establecida"

        adjusted_message = self.adjust_message_length(message)
        encrypted = ""

        for i in range(len(adjusted_message)):
            msg_ascii = charToAscii(adjusted_message[i])
            key_ascii = charToAscii(self.current_key[i])

            encrypted_ascii = (msg_ascii + key_ascii) % 127

            if encrypted_ascii < 32:
                encrypted_ascii += 32

            encrypted += asciiValueToChar(encrypted_ascii)

        return encrypted

    def decrypt_caesar_shift(self, encrypted_message):
        if not self.current_key:
            return "Error: No hay llave establecida"

        decrypted = ""

        for i in range(len(encrypted_message)):
            enc_ascii = charToAscii(encrypted_message[i])
            key_ascii = charToAscii(self.current_key[i])

            decrypted_ascii = (enc_ascii - key_ascii) % 127

            if decrypted_ascii < 32:
                decrypted_ascii += 95

            decrypted += asciiValueToChar(decrypted_ascii)

        return decrypted

    def encrypt_substitution(self, message):
        if not self.current_key:
            return "Error: No hay llave establecida"

        adjusted_message = self.adjust_message_length(message)
        encrypted = ""

        for i in range(len(adjusted_message)):
            msg_ascii = charToAscii(adjusted_message[i])
            key_ascii = charToAscii(self.current_key[i])

            new_ascii = ((msg_ascii * key_ascii) % 95) + 32

            encrypted += asciiValueToChar(new_ascii)

        return encrypted

    def decrypt_substitution(self, encrypted_message):
        if not self.current_key:
            return "Error: No hay llave establecida"

        decrypted = ""

        for i in range(len(encrypted_message)):
            enc_ascii = charToAscii(encrypted_message[i])
            key_ascii = charToAscii(self.current_key[i])

            enc_value = enc_ascii - 32

            for original in range(95):
                if ((original * key_ascii) % 95) == enc_value:
                    decrypted += asciiValueToChar(original + 32)
                    break
            else:
                decrypted += '?'

        return decrypted