ENV['MT_NO_PLUGINS'] = '1'
require 'minitest/autorun'
require_relative '../src/des_ecb'

class TestDESECB < Minitest::Test

  def setup
    @key = generate_des_key
  end

  # Clave tiene exactamente 8 bytes
  def test_key_length
    assert_equal 8, @key.bytesize
  end

  # Cada clave generada es distinta
  def test_key_is_random
    refute_equal generate_des_key, generate_des_key
  end

  # El ciphertext tiene longitud múltiplo de 8
  def test_ciphertext_length_multiple_of_8
    ["A", "HOLA", "12345678", "mensaje largo de prueba"].each do |msg|
      ct = des_ecb_encrypt(msg.b, @key)
      assert_equal 0, ct.bytesize % 8, "'#{msg}' produce ciphertext no alineado"
    end
  end

  # El ciphertext no es igual al plaintext
  def test_ciphertext_differs_from_plaintext
    plaintext = "HOLA".b
    ct = des_ecb_encrypt(plaintext, @key)
    refute_equal plaintext, ct
  end

  # decrypt(encrypt(m)) == m
  def test_roundtrip_mensaje_corto
    msg = "HOLA".b
    assert_equal msg, des_ecb_decrypt(des_ecb_encrypt(msg, @key), @key)
  end

  def test_roundtrip_mensaje_exacto_bloque
    msg = "12345678".b
    assert_equal msg, des_ecb_decrypt(des_ecb_encrypt(msg, @key), @key)
  end

  def test_roundtrip_mensaje_largo
    msg = "Este es un mensaje mas largo que un bloque DES.".b
    assert_equal msg, des_ecb_decrypt(des_ecb_encrypt(msg, @key), @key)
  end

  def test_roundtrip_varios_tamanios
    (1..32).each do |len|
      msg = ("X" * len).b
      assert_equal msg, des_ecb_decrypt(des_ecb_encrypt(msg, @key), @key),
                   "roundtrip falló para longitud #{len}"
    end
  end

  # Misma clave produce el mismo ciphertext
  def test_determinista
    msg = "HOLA".b
    assert_equal des_ecb_encrypt(msg, @key), des_ecb_encrypt(msg, @key)
  end

  # Claves distintas producen ciphertexts distintos
  def test_diferente_clave_diferente_ciphertext
    msg = "HOLA".b
    key2 = generate_des_key
    refute_equal des_ecb_encrypt(msg, @key), des_ecb_encrypt(msg, key2)
  end

end

puts "\n=== DEMO DES-ECB ==="
key = generate_des_key
puts "  Clave (hex): #{key.unpack1('H*')}"

mensajes = ["HOLA", "12345678", "Mensaje secreto largo"]
mensajes.each do |msg|
  ct = des_ecb_encrypt(msg.b, key)
  pt = des_ecb_decrypt(ct, key)
  puts "  '#{msg}'"
  puts "    => cifrado:    #{ct.unpack1('H*')}"
  puts "    => descifrado: #{pt}"
end
