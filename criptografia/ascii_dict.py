from conversions.ascii_conversions import asciiValueToChar

ASCII_TO_BINARY = {}
for i in range(128):
    char = asciiValueToChar(i)
    binary = ""
    temp = i
    for _ in range(8):
        binary = str(temp % 2) + binary
        temp = temp // 2
    ASCII_TO_BINARY[char] = binary

