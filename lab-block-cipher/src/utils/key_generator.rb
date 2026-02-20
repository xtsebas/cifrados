# Generador de claves criptográficamente seguras.

require 'securerandom'

def generate_des_key
  # Genera una clave DES aleatoria de 8 bytes (64 bits).
  # Nota: DES usa efectivamente 56 bits (los otros 8 son de paridad),
  # pero la clave es de 8 bytes.
  SecureRandom.bytes(8)
end

def generate_3des_key(key_option: 2)
  # Genera una clave 3DES aleatoria.
  
  case key_option
    when 2 then SecureRandom.bytes(16)
    when 3 then SecureRandom.bytes(24)
    else raise ArgumentError, "key_option debe ser 2 o 3"
  end
end

def generate_aes_key(key_size: 256)
  # TODO: Implementar
  # Convertir bits a bytes: key_size // 8
  
  raise ArgumentError, "key_size debe ser 128, 192 o 256" unless [128, 192, 256].include?(key_size)
  SecureRandom.bytes(key_size / 8)
end

def generate_iv(block_size: 8)
  # Genera un IV aleatorio criptograficamente seguro

  SecureRandom.bytes(block_size)
end