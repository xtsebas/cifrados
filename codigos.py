from ascii_dict import ASCII_TO_BINARY


def asciiToBinary(text):
    text = text.lower()
    binary_result = ""
    for char in text:
        if char in ASCII_TO_BINARY:
            binary_result += ASCII_TO_BINARY[char]
    return binary_result

def base64ToBinary():
    pass

def binaryToAscii():
    pass

def binaryToBase64():
    pass


text = "Hello World"
binary_output = asciiToBinary(text)
print(binary_output)  