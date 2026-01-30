import random
import string
import hashlib
import time


class DynamicKeyGenerator:
    def __init__(self):
        self.charset_letters = string.ascii_letters  # a-z, A-Z
        self.charset_digits = string.digits  # 0-9
        self.charset_symbols = string.punctuation  # !@#$%^&*()...
        self.charset_all = string.ascii_letters + string.digits + string.punctuation
        self.charset_printable = string.printable.strip()  # Todos los caracteres imprimibles

    def generate_random_key(self, length=16, charset='all'):
        if charset == 'letters':
            chars = self.charset_letters
        elif charset == 'digits':
            chars = self.charset_digits
        elif charset == 'symbols':
            chars = self.charset_symbols
        elif charset == 'alphanumeric':
            chars = self.charset_letters + self.charset_digits
        else:  
            chars = self.charset_all

        key = ''.join(random.choice(chars) for _ in range(length))
        return key

    def generate_key_from_seed(self, seed, length=16, charset='all'):
        random.seed(seed)
        key = self.generate_random_key(length, charset)
        random.seed()
        return key

    def generate_key_from_hash(self, data, length=16, charset='all'):
        hash_object = hashlib.sha256(data.encode())
        hash_hex = hash_object.hexdigest()

        return self.generate_key_from_seed(hash_hex, length, charset)

    def generate_time_based_key(self, length=16, charset='all'):
        timestamp = str(time.time())
        key = self.generate_key_from_seed(timestamp, length, charset)
        return key, timestamp

    def generate_multiple_keys(self, count=5, length=16, charset='all'):
        return [self.generate_random_key(length, charset) for _ in range(count)]

    def generate_key_with_pattern(self, pattern, length=16):
        key = []
        pattern_map = {
            'L': string.ascii_uppercase,
            'l': string.ascii_lowercase,
            'd': string.digits,
            's': string.punctuation,
            'a': string.ascii_letters + string.digits,
            '*': self.charset_all
        }

        if pattern:
            for char in pattern:
                if char in pattern_map:
                    key.append(random.choice(pattern_map[char]))
                else:
                    key.append(char)
        else:
            key = list(self.generate_random_key(length))

        return ''.join(key)