# Generador de claves criptográficamente seguras.

require 'securerandom'

def generate_des_key
  # Genera una clave DES aleatoria de 8 bytes (64 bits).
  # Nota: DES usa efectivamente 56 bits (los otros 8 son de paridad),
  # pero la clave es de 8 bytes.
  
  return true
end

def generate_3des_key(key_option: 2)
  # Genera una clave 3DES aleatoria.
  
  return true
end

def generate_aes_key(key_size: 256)
  # TODO: Implementar
  # Convertir bits a bytes: key_size // 8
end

def generate_iv(block_size: 8)
  # TODO: Implementar
end