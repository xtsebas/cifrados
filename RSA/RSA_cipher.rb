require 'openssl'
require 'base64'

# Cifra un mensaje usando RSA-OAEP 
def rsa_cipher(message, public_key_pem)
  public_key = OpenSSL::PKey::RSA.new(public_key_pem)
  ciphertext = public_key.public_encrypt(message, OpenSSL::PKey::RSA::PKCS1_OAEP_PADDING)
  Base64.strict_encode64(ciphertext)
end

# Descifra RSA con padding OAEP
def rsa_decipher(ciphertext_b64, private_key_pem, passphrase = nil)
  private_key = OpenSSL::PKey::RSA.new(private_key_pem, passphrase)
  ciphertext  = Base64.strict_decode64(ciphertext_b64)
  private_key.private_decrypt(ciphertext, OpenSSL::PKey::RSA::PKCS1_OAEP_PADDING)
end

# Cifrado hibrido RSA-OAEP + AES-GCM
def encrypt_document(document, recipient_public_key_pem)
  aes_key = OpenSSL::Random.random_bytes(32)

  # Cifrar el documento con AES-GCM
  cipher = OpenSSL::Cipher.new('AES-256-GCM')
  cipher.encrypt
  nonce = cipher.random_iv          # 12 bytes
  cipher.key = aes_key
  ciphertext = cipher.update(document) + cipher.final
  tag = cipher.auth_tag             # 16 bytes

  # Cifrar la clave AES con RSA-OAEP
  public_key     = OpenSSL::PKey::RSA.new(recipient_public_key_pem)
  encrypted_key  = public_key.public_encrypt(aes_key, OpenSSL::PKey::RSA::PKCS1_OAEP_PADDING)

  # Empaquetar: longitud(4B) + clave_cifrada + nonce + tag + ciphertext
  [encrypted_key.bytesize].pack('N') + encrypted_key + nonce + tag + ciphertext
end

def decrypt_document(pkg, recipient_private_key_pem, passphrase = nil)
  # Desempaquetar
  key_len       = pkg[0, 4].unpack1('N')
  encrypted_key = pkg[4, key_len]
  nonce         = pkg[4 + key_len, 12]
  tag           = pkg[4 + key_len + 12, 16]
  ciphertext    = pkg[4 + key_len + 28..]

  # Descifrar la clave AES con RSA-OAEP
  private_key = OpenSSL::PKey::RSA.new(recipient_private_key_pem, passphrase)
  aes_key     = private_key.private_decrypt(encrypted_key, OpenSSL::PKey::RSA::PKCS1_OAEP_PADDING)

  # Descifrar el documento con AES-GCM
  decipher = OpenSSL::Cipher.new('AES-256-GCM')
  decipher.decrypt
  decipher.iv       = nonce
  decipher.key      = aes_key
  decipher.auth_tag = tag
  decipher.update(ciphertext) + decipher.final
end