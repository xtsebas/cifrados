require 'openssl'
require_relative 'utils/key_generator'

# Encrypts plaintext with AES-256-CBC using a random IV.
#
# Padding: OpenSSL uses PKCS#7 by default (cipher.padding = 1).
# This satisfies the lab requirement of using the library's own padding.
#
# The IV is prepended to the ciphertext so that decryption only needs the key.
# Output format: IV (16 bytes) | ciphertext
#
# CBC chains each plaintext block with the previous ciphertext block (starting
# from the random IV), so identical plaintext blocks produce different ciphertext
# blocks. This hides structure and makes CBC safe for encrypting images.
#
# Parameters:
#   plaintext: data to encrypt (String)
#   key:       32-byte AES-256 key
#
# Returns: IV + ciphertext (binary String)
def aes_cbc_encrypt(plaintext, key)
  iv = generate_iv(block_size: 16)

  cipher = OpenSSL::Cipher.new('AES-256-CBC')
  cipher.encrypt
  cipher.key = key
  cipher.iv  = iv

  ciphertext = cipher.update(plaintext.b) + cipher.final
  iv + ciphertext
end

# Decrypts data produced by aes_cbc_encrypt.
# Extracts the IV from the first 16 bytes, then decrypts the remainder.
# OpenSSL automatically verifies and removes PKCS#7 padding.
#
# Parameters:
#   data: IV (16 bytes) + ciphertext (binary String)
#   key:  32-byte AES-256 key (same as used for encryption)
#
# Returns: original plaintext (binary String)
def aes_cbc_decrypt(data, key)
  iv         = data[0, 16]
  ciphertext = data[16..]

  cipher = OpenSSL::Cipher.new('AES-256-CBC')
  cipher.decrypt
  cipher.key = key
  cipher.iv  = iv

  cipher.update(ciphertext) + cipher.final
end
