import sys
sys.path.insert(0, '..')

from custom_utilities import (
    get_ascii_letters, get_ascii_digits, get_ascii_uppercase,
    get_ascii_lowercase, get_ascii_symbols, choice_from_string,
    simple_hash_string, get_timestamp_millis
)


class DynamicKeyGenerator:
    def __init__(self):
        self.charset_letters = get_ascii_letters() 
        self.charset_digits = get_ascii_digits()  
        self.charset_symbols = get_ascii_symbols()  
        self.charset_all = self.charset_letters + self.charset_digits + self.charset_symbols
        self.charset_uppercase = get_ascii_uppercase()
        self.charset_lowercase = get_ascii_lowercase()

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

        key = ""
        for _ in range(length):
            key += choice_from_string(chars)
        return key

    def generate_key_from_seed(self, seed, length=16, charset='all'):
        seed_hash = simple_hash_string(seed)
        key = ""
        
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
        
        for i in range(length):
            index = (seed_hash + i) % len(chars)
            key += chars[index]
        
        return key

    def generate_key_from_hash(self, data, length=16, charset='all'):
        hash_value = simple_hash_string(data)
        hash_hex = hex(hash_value)[2:]  
        
        return self.generate_key_from_seed(hash_hex, length, charset)

    def generate_time_based_key(self, length=16, charset='all'):
        timestamp = str(get_timestamp_millis())
        key = self.generate_key_from_seed(timestamp, length, charset)
        return key, timestamp

    def generate_multiple_keys(self, count=5, length=16, charset='all'):
        keys = []
        for _ in range(count):
            keys.append(self.generate_random_key(length, charset))
        return keys

    def generate_key_with_pattern(self, pattern, length=16):
        key = ""
        pattern_map = {
            'L': self.charset_uppercase,
            'l': self.charset_lowercase,
            'd': self.charset_digits,
            's': self.charset_symbols,
            'a': self.charset_letters + self.charset_digits,
            '*': self.charset_all
        }

        if pattern:
            for char in pattern:
                if char in pattern_map:
                    key += choice_from_string(pattern_map[char])
                else:
                    key += char
        else:
            key = self.generate_random_key(length)

        return key