require 'openssl'
require_relative 'utils/manual_padding'
require_relative 'utils/key_generator'

begin
  OpenSSL::Provider.load('legacy')
rescue OpenSSL::Provider::ProviderError
end

# Cifra un mensaje usando DES en modo ECB.
def des_ecb_encrypt(plaintext, key)
  padded = pkcs7_pad(plaintext.b, block_size: 8)

  cipher = OpenSSL::Cipher.new('DES-ECB')
  cipher.encrypt
  cipher.key     = key
  cipher.padding = 0 

  cipher.update(padded) + cipher.final
end

# Descifra un ciphertext DES-ECB y elimina el padding PKCS#7
def des_ecb_decrypt(ciphertext, key)
  cipher = OpenSSL::Cipher.new('DES-ECB')
  cipher.decrypt
  cipher.key     = key
  cipher.padding = 0

  padded = cipher.update(ciphertext) + cipher.final
  pkcs7_unpad(padded)
end
