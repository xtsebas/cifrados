require 'openssl'
require_relative 'utils/key_generator'

# Encrypts plaintext with AES-256-ECB.
#
# Padding: OpenSSL uses PKCS#7 by default (cipher.padding = 1).
# This satisfies the lab requirement of using the library's own padding.
#
# WARNING: ECB is deterministic — identical 16-byte plaintext blocks always
# produce identical ciphertext blocks. Structure is preserved in the output,
# making ECB unsuitable for encrypting data with repeating patterns (e.g. images).
#
# Parameters:
#   plaintext: data to encrypt (String)
#   key:       32-byte AES-256 key
#
# Returns: ciphertext (binary String, length is a multiple of 16)
def aes_ecb_encrypt(plaintext, key)
  cipher = OpenSSL::Cipher.new('AES-256-ECB')
  cipher.encrypt
  cipher.key = key
  cipher.update(plaintext.b) + cipher.final
end

# Decrypts ciphertext produced by aes_ecb_encrypt.
# OpenSSL automatically verifies and removes PKCS#7 padding.
#
# Parameters:
#   ciphertext: data to decrypt (binary String, must be a multiple of 16 bytes)
#   key:        32-byte AES-256 key (same as used for encryption)
#
# Returns: original plaintext (binary String)
def aes_ecb_decrypt(ciphertext, key)
  cipher = OpenSSL::Cipher.new('AES-256-ECB')
  cipher.decrypt
  cipher.key = key
  cipher.update(ciphertext) + cipher.final
end
