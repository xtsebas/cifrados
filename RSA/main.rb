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

puts "\n[OK] Cifrado y descifrado RSA-OAEP exitoso." if mensaje == descifrado
