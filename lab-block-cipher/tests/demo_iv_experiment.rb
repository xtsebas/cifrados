require 'openssl'
require_relative '../src/utils/key_generator'

# Funcion auxiliar: CBC con IV controlado externamente (para el experimento).
# Nuestra aes_cbc_encrypt genera el IV internamente (correcto para produccion),
# pero aqui necesitamos fijar el IV para demostrar que pasa cuando se reutiliza.
def cbc_encrypt_fixed_iv(plaintext, key, iv)
  cipher = OpenSSL::Cipher.new('AES-256-CBC')
  cipher.encrypt
  cipher.key = key
  cipher.iv  = iv
  cipher.update(plaintext.b) + cipher.final
end

key = generate_aes_key(key_size: 256)
msg = "Mensaje secreto!!"   # 18 bytes

puts "Clave AES-256 (hex): #{key.unpack1('H*')}"
puts "Mensaje             : \"#{msg}\""

# ── Experimento 1: mismo IV dos veces ────────────────────────────────────────
puts "\n" + "=" * 60
puts "EXPERIMENTO 1 — mismo IV, mismo mensaje, misma clave"
puts "=" * 60

iv_fijo = generate_iv(block_size: 16)
ct_a = cbc_encrypt_fixed_iv(msg, key, iv_fijo)
ct_b = cbc_encrypt_fixed_iv(msg, key, iv_fijo)

puts "\nIV fijo : #{iv_fijo.unpack1('H*')}"
puts "CT_A    : #{ct_a.unpack1('H*')}"
puts "CT_B    : #{ct_b.unpack1('H*')}"
puts "CT_A == CT_B: #{ct_a == ct_b}"
puts "=> IDENTICOS: reutilizar IV hace CBC tan determinista como ECB."
puts "   Un atacante que ve CT_A == CT_B sabe que el plaintext es el mismo."

# ── Experimento 2: IVs diferentes ────────────────────────────────────────────
puts "\n" + "=" * 60
puts "EXPERIMENTO 2 — IVs distintos, mismo mensaje, misma clave"
puts "=" * 60

iv1 = generate_iv(block_size: 16)
iv2 = generate_iv(block_size: 16)
ct1 = cbc_encrypt_fixed_iv(msg, key, iv1)
ct2 = cbc_encrypt_fixed_iv(msg, key, iv2)

puts "\nIV1 : #{iv1.unpack1('H*')}"
puts "IV2 : #{iv2.unpack1('H*')}"
puts "CT1 : #{ct1.unpack1('H*')}"
puts "CT2 : #{ct2.unpack1('H*')}"
puts "CT1 == CT2: #{ct1 == ct2}"
puts "=> DIFERENTES: IVs aleatorios garantizan ciphertexts distintos"
puts "   aunque el plaintext y la clave sean identicos."

# ── Experimento 3: ataque por IV compartido ───────────────────────────────────
puts "\n" + "=" * 60
puts "EXPERIMENTO 3 — IV reuse: deteccion de mensajes identicos"
puts "=" * 60

# Simulacion: el servidor cifra las sesiones de tres usuarios con el mismo IV fijo.
# Un atacante que intercepta el trafico puede comparar ciphertexts.
iv_reused = generate_iv(block_size: 16)
sesiones = {
  "Alice" => "LOGIN: ADMIN!!!",    # 15 chars -> padded to 16
  "Bob"   => "LOGIN: ADMIN!!!",    # mismo plaintext que Alice
  "Carol" => "LOGIN: GUEST!!!"     # diferente
}

puts "\nCiphertexts interceptados (IV reutilizado = #{iv_reused.unpack1('H*')}):"
cifrados = {}
sesiones.each do |usuario, datos|
  ct = cbc_encrypt_fixed_iv(datos, key, iv_reused)
  cifrados[usuario] = ct
  puts "  #{usuario.ljust(6)}: #{ct.unpack1('H*')}"
end

puts "\nComparaciones:"
puts "  Alice == Bob  : #{cifrados['Alice'] == cifrados['Bob']}"
puts "  Alice == Carol: #{cifrados['Alice'] == cifrados['Carol']}"
puts ""
puts "=> Un atacante puede deducir que Alice y Bob tienen el mismo token/login"
puts "   sin conocer la clave ni el contenido del mensaje."
puts ""
puts "=> Con IVs aleatorios unicos (comportamiento correcto de aes_cbc_encrypt):"
ct_alice_correcto = "Alice tiene IV distinto cada vez"
iv_a = generate_iv(block_size: 16)
iv_b = generate_iv(block_size: 16)
ct_correcto_a = cbc_encrypt_fixed_iv(sesiones['Alice'], key, iv_a)
ct_correcto_b = cbc_encrypt_fixed_iv(sesiones['Bob'],   key, iv_b)
puts "  Alice (IV aleatorio): #{ct_correcto_a.unpack1('H*')}"
puts "  Bob   (IV aleatorio): #{ct_correcto_b.unpack1('H*')}"
puts "  Alice == Bob        : #{ct_correcto_a == ct_correcto_b}"
puts "=> Aunque el plaintext es identico, los ciphertexts son distintos."
