ENV['MT_NO_PLUGINS'] = '1'
require 'minitest/autorun'
require_relative '../src/des3_cbc'

class TestDES3CBC < Minitest::Test

  def setup
    @key2 = generate_3des_key(key_option: 2)  # 16 bytes
    @key3 = generate_3des_key(key_option: 3)  # 24 bytes
  end

  # --- Claves ---
  def test_key2_length
    assert_equal 16, @key2.bytesize
  end

  def test_key3_length
    assert_equal 24, @key3.bytesize
  end

  def test_keys_are_random
    refute_equal generate_3des_key(key_option: 2), generate_3des_key(key_option: 2)
    refute_equal generate_3des_key(key_option: 3), generate_3des_key(key_option: 3)
  end

  def test_key_option_invalido
    assert_raises(ArgumentError) { generate_3des_key(key_option: 1) }
  end

  # --- IV ---
  def test_iv_length
    assert_equal 8, generate_iv.bytesize
  end

  def test_iv_is_random
    refute_equal generate_iv, generate_iv
  end

  # --- IV diferente por cada cifrado ---
  def test_iv_distinto_por_cifrado
    msg = "HOLA".b
    enc1 = des3_cbc_encrypt(msg, @key2)
    enc2 = des3_cbc_encrypt(msg, @key2)
    # Los primeros 8 bytes son el IV — deben ser distintos
    refute_equal enc1[0, 8], enc2[0, 8]
    # Y por tanto el ciphertext completo también difiere
    refute_equal enc1, enc2
  end

  # --- Formato de salida: [IV (8B) | ciphertext] ---
  def test_output_includes_iv_prefix
    msg = "HOLA".b
    enc = des3_cbc_encrypt(msg, @key2)
    assert enc.bytesize > 8, "la salida debe incluir IV + ciphertext"
  end

  def test_ciphertext_length_multiple_of_8
    ["A", "HOLA", "12345678", "mensaje largo"].each do |msg|
      enc = des3_cbc_encrypt(msg.b, @key2)
      # sin IV, el ciphertext debe ser múltiplo de 8
      assert_equal 0, enc[8..].bytesize % 8
    end
  end

  # --- Roundtrip con clave de 2 opciones ---
  def test_roundtrip_key2_corto
    msg = "HOLA".b
    assert_equal msg, des3_cbc_decrypt(des3_cbc_encrypt(msg, @key2), @key2)
  end

  def test_roundtrip_key2_bloque_exacto
    msg = "12345678".b
    assert_equal msg, des3_cbc_decrypt(des3_cbc_encrypt(msg, @key2), @key2)
  end

  def test_roundtrip_key2_largo
    msg = "Este mensaje es mas largo que un bloque de 8 bytes.".b
    assert_equal msg, des3_cbc_decrypt(des3_cbc_encrypt(msg, @key2), @key2)
  end

  def test_roundtrip_varios_tamanios_key2
    (1..32).each do |len|
      msg = ("A" * len).b
      assert_equal msg, des3_cbc_decrypt(des3_cbc_encrypt(msg, @key2), @key2),
                   "roundtrip key2 falló para longitud #{len}"
    end
  end

  # --- Roundtrip con clave de 3 opciones ---
  def test_roundtrip_key3_corto
    msg = "HOLA".b
    assert_equal msg, des3_cbc_decrypt(des3_cbc_encrypt(msg, @key3), @key3)
  end

  def test_roundtrip_varios_tamanios_key3
    (1..32).each do |len|
      msg = ("B" * len).b
      assert_equal msg, des3_cbc_decrypt(des3_cbc_encrypt(msg, @key3), @key3),
                   "roundtrip key3 falló para longitud #{len}"
    end
  end

  # --- Clave incorrecta falla el descifrado ---
  def test_wrong_key_raises_or_returns_garbage
    msg = "HOLA".b
    enc = des3_cbc_encrypt(msg, @key2)
    wrong_key = generate_3des_key(key_option: 2)
    result = des3_cbc_decrypt(enc, wrong_key) rescue nil
    refute_equal msg, result
  end

end

# --- Demo visual ---
puts "\n=== DEMO 3DES-CBC ==="

[2, 3].each do |opt|
  key = generate_3des_key(key_option: opt)
  puts "\n  key_option=#{opt} (#{key.bytesize} bytes):"
  puts "  Clave (hex): #{key.unpack1('H*')}"

  mensajes = ["HOLA", "12345678", "Mensaje secreto con 3DES-CBC"]
  mensajes.each do |msg|
    enc = des3_cbc_encrypt(msg.b, key)
    iv  = enc[0, 8].unpack1('H*')
    ct  = enc[8..].unpack1('H*')
    pt  = des3_cbc_decrypt(enc, key)
    puts "  '#{msg}'"
    puts "    IV:         #{iv}"
    puts "    ciphertext: #{ct}"
    puts "    descifrado: #{pt}"
  end
end
