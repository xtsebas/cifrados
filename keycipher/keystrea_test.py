import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from keystream import encrypt, decrypt


class TestStreamCipher(unittest.TestCase):
    def _assert_with_status(self, label, assert_fn):
        try:
            assert_fn()
        except AssertionError:
            print(f"{label}: FALLIDO")
            raise
        else:
            print(f"{label}: OK")

    def test_encrypt_decrypt(self):
        print("\nTEST 1: Encrypt -> Decrypt recupera el mensaje original")
        message = "Hello World!"
        key = "testkey"
        encrypted = encrypt(message, key)
        decrypted = decrypt(encrypted, key)

        print("Mensaje original:", message)
        print("Clave:", key)
        print("Cifrado (hex):", encrypted.hex())
        print("Descifrado:", decrypted)

        self._assert_with_status("TEST 1", lambda: self.assertEqual(message, decrypted))

    def test_different_keys(self):
        print("\nTEST 2: Diferentes claves producen diferentes cifrados")
        message = "Hello World!"
        encrypted1 = encrypt(message, "key1")
        encrypted2 = encrypt(message, "key2")

        print("Mensaje:", message)
        print("Clave 1: key1 ->", encrypted1.hex())
        print("Clave 2: key2 ->", encrypted2.hex())

        self._assert_with_status("TEST 2", lambda: self.assertNotEqual(encrypted1, encrypted2))

    def test_same_key_determinism(self):
        print("\nTEST 3: Misma clave produce mismo cifrado (determinismo)")
        message = "Deterministic Test"
        key = "samekey"
        encrypted1 = encrypt(message, key)
        encrypted2 = encrypt(message, key)

        print("Mensaje:", message)
        print("Clave:", key)
        print("Cifrado 1:", encrypted1.hex())
        print("Cifrado 2:", encrypted2.hex())

        self._assert_with_status("TEST 3", lambda: self.assertEqual(encrypted1, encrypted2))

    def test_different_lengths(self):
        print("\nTEST 4: Manejo de diferentes longitudes de mensaje")
        key = "lengthkey"
        messages = ["A", "Short", "This is a longer message for testing"]

        def _assert_loop():
            for msg in messages:
                encrypted = encrypt(msg, key)
                decrypted = decrypt(encrypted, key)

                print("\nMensaje:", msg)
                print("Longitud:", len(msg))
                print("Cifrado (hex):", encrypted.hex())
                print("Descifrado:", decrypted)

                self.assertEqual(msg, decrypted)

        self._assert_with_status("TEST 4", _assert_loop)


if __name__ == "__main__":
    unittest.main()
