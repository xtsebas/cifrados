import sys
sys.path.insert(0, '..')

from criptografia.conversions.ascii_conversions import charToAscii, asciiValueToChar


def get_ascii_letters():
    letters = ""
    for i in range(97, 123):
        letters += asciiValueToChar(i)
    for i in range(65, 91):
        letters += asciiValueToChar(i)
    return letters


def get_ascii_digits():
    digits = ""
    for i in range(48, 58):
        digits += asciiValueToChar(i)
    return digits


def get_ascii_uppercase():
    uppercase = ""
    for i in range(65, 91):
        uppercase += asciiValueToChar(i)
    return uppercase


def get_ascii_lowercase():
    lowercase = ""
    for i in range(97, 123):
        lowercase += asciiValueToChar(i)
    return lowercase


def get_ascii_symbols():
    symbols = ""
    for i in range(33, 48):
        symbols += asciiValueToChar(i)
    for i in range(58, 65):
        symbols += asciiValueToChar(i)
    for i in range(91, 97):
        symbols += asciiValueToChar(i)
    for i in range(123, 127):
        symbols += asciiValueToChar(i)
    return symbols


def simple_random_int(seed=None):
    if seed is None:
        import time
        seed = int(time.time() * 1000) % (2**31)
    
    a = 1103515245
    c = 12345
    m = 2**31
    
    state = seed
    
    def next_random():
        nonlocal state
        state = (a * state + c) % m
        return state // (m // 100)  
    
    return next_random


def choice_from_string(chars):
    if not chars:
        return ''
    
    random_gen = simple_random_int()
    index = random_gen() % len(chars)
    return chars[index]


def simple_hash_string(text):
    hash_value = 0
    for char in text:
        ascii_val = charToAscii(char)
        hash_value = (hash_value * 31 + ascii_val) % (2**32)
    return hash_value


def get_timestamp_millis():
    import time
    return int(time.time() * 1000)


def xor_bytes(byte1, byte2):
    val1 = charToAscii(byte1)
    val2 = charToAscii(byte2)
    result = val1 ^ val2
    return asciiValueToChar(result)