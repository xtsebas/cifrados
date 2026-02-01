import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cesar import cesar_cifrar, cesar_descifrar


def rot13(mensaje):
    return cesar_cifrar(mensaje, 13)

def rot13_descifrar(mensaje):
    return cesar_descifrar(mensaje, 13)