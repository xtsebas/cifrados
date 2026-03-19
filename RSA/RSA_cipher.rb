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