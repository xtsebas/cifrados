require_relative 'keys_generator'
require_relative 'RSA_cipher'

PASSPHRASE   = 'lab04uvg'
PRIVATE_PATH = 'private_key.pem'
PUBLIC_PATH  = 'public_key.pem'

puts "=" * 50
puts "  Laboratorio RSA"
puts "=" * 50

puts "\nGenerando par de claves RSA de 2048 bits..."
keys = generate_rsa_keys(2048)
puts "    Claves generadas correctamente."

puts "\nExportando claves en formato PEM..."
save_keys(keys, PRIVATE_PATH, PUBLIC_PATH, PASSPHRASE)

puts "\nVerificando archivos generados..."
[PRIVATE_PATH, PUBLIC_PATH].each do |path|
  if File.exist?(path)
    puts "    [OK] #{path} (#{File.size(path)} bytes)"
  else
    puts "    [ERROR] #{path} no fue creado"
  end
end

puts "\nClave publica generada:"
puts keys[:public_key].to_pem

puts "Verificando que la clave privada se puede leer con la passphrase..."
begin
  loaded_private = OpenSSL::PKey::RSA.new(File.read(PRIVATE_PATH), PASSPHRASE)
  puts "    [OK] Clave privada cargada correctamente desde #{PRIVATE_PATH}"
  puts "    Tamanio: #{loaded_private.n.num_bits} bits"
rescue => e
  puts "    [ERROR] #{e.message}"
end

puts "\n" + "=" * 50
puts "  Cifrado/Descifrado RSA-OAEP"
puts "=" * 50

mensaje   = "Contrato confidencial - Firma Legal Guatemala"
pub_pem   = File.read(PUBLIC_PATH)
priv_pem  = File.read(PRIVATE_PATH)

puts "\nMensaje original : #{mensaje}"

cifrado = rsa_cipher(mensaje, pub_pem)
puts "Texto cifrado    : #{cifrado}"

descifrado = rsa_decipher(cifrado, priv_pem, PASSPHRASE)
puts "Texto descifrado : #{descifrado}"

cifrado2 = rsa_cipher(mensaje, pub_pem)
puts "\nCifrado 2       : #{cifrado2}"

decifrado2 = rsa_decipher(cifrado2, priv_pem, PASSPHRASE)
puts "Descifrado 2     : #{decifrado2}"

puts "\n[OK] Cifrado y descifrado RSA-OAEP exitoso." if mensaje == descifrado


puts "\n" + "=" * 50
puts "  Cifrado Hibrido RSA-OAEP + AES-GCM"
puts "=" * 50

pub_pem  = File.read(PUBLIC_PATH)
priv_pem = File.read(PRIVATE_PATH)

documento = "Contrato de confidencialidad No. 2025-GT-001"
puts "\nDocumento original : #{documento}"

paquete = encrypt_document(documento, pub_pem)
puts "Paquete cifrado    : #{paquete.bytesize} bytes (clave RSA + nonce + tag + ciphertext)"

recuperado = decrypt_document(paquete, priv_pem, PASSPHRASE)
puts "Documento recuperado: #{recuperado}"

puts "\n[OK] Cifrado hibrido exitoso." if documento == recuperado

