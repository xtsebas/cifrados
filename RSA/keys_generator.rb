require 'openssl'

# Genera un par de claves RSA del tamaño de bits indicado
def generate_rsa_keys(bits = 2048)
  key = OpenSSL::PKey::RSA.new(bits)

  {
    private_key: key,
    public_key:  key.public_key
  }
end

# Guarda las claves en archivos PEM
def save_keys(keys, private_path, public_path, passphrase)
  cipher = OpenSSL::Cipher.new('AES-256-CBC')
  encrypted_pem = keys[:private_key].to_pem(cipher, passphrase)

  File.write(private_path, encrypted_pem)
  File.write(public_path,  keys[:public_key].to_pem)

  puts "Clave privada guardada en: #{private_path}"
  puts "Clave publica  guardada en: #{public_path}"
end