require 'openssl'
require_relative 'utils/key_generator'

begin
  OpenSSL::Provider.load('legacy')
rescue OpenSSL::Provider::ProviderError
end

# Selecciona el nombre del cipher segun el tamano de clave
def cipher_name_for(key)
  key.bytesize == 16 ? 'DES-EDE-CBC' : 'DES-EDE3-CBC'
end

# Cifra plaintext con 3DES-CBC
def des3_cbc_encrypt(plaintext, key)
  iv = generate_iv(block_size: 8)

  cipher = OpenSSL::Cipher.new(cipher_name_for(key))
  cipher.encrypt
  cipher.key = key
  cipher.iv  = iv

  ciphertext = cipher.update(plaintext.b) + cipher.final
  iv + ciphertext
end

# Descifra un dato producido por des3_cbc_encrypt
def des3_cbc_decrypt(data, key)
  iv         = data[0, 8]
  ciphertext = data[8..]

  cipher = OpenSSL::Cipher.new(cipher_name_for(key))
  cipher.decrypt
  cipher.key = key
  cipher.iv  = iv

  cipher.update(ciphertext) + cipher.final
end
