ENV['MT_NO_PLUGINS'] = '1'
require 'minitest/autorun'
require_relative '../src/utils/manual_padding'

class TestPKCS7Pad < Minitest::Test

   # --- pkcs7_pad --- 
    def test_pad_partial_block
        assert_equal '484f4c4104040404', pkcs7_pad("HOLA".b, block_size: 8).unpack1('H*')
    end

    def test_pad_full_block_adds_extra_block
        assert_equal '31323334353637380808080808080808', pkcs7_pad("12345678".b, block_size: 8).unpack1('H*')
    end

    def test_pad_one_byte_message
        result = pkcs7_pad("\x41".b, block_size: 8)
        assert_equal 8, result.bytesize
        assert_equal "\x07" * 7, result[1..].b
    end

    def test_pad_block_size_16
        data = "HOLA".b
        result = pkcs7_pad(data, block_size: 16)
        assert_equal 16, result.bytesize
        assert_equal "\x0c" * 12, result[4..].b
    end

    def test_pad_output_length_is_multiple_of_block_size
        (1..20).each do |len|
        data = ("A" * len).b
        result = pkcs7_pad(data, block_size: 8)
        assert_equal 0, result.bytesize % 8, "longitud #{len} no produce múltiplo de 8"
        end
    end

    # --- pkcs7_unpad ---
    def test_unpad_restores_original
        original = "HOLA".b
        assert_equal original, pkcs7_unpad(pkcs7_pad(original, block_size: 8))
    end

    def test_unpad_full_block_padding
        original = "12345678".b
        assert_equal original, pkcs7_unpad(pkcs7_pad(original, block_size: 8))
    end

    def test_roundtrip_varios_tamanios
        (1..24).each do |len|
        data = ("B" * len).b
        assert_equal data, pkcs7_unpad(pkcs7_pad(data, block_size: 8)),
                    "roundtrip falló para longitud #{len}"
        end
    end

    def test_roundtrip_block_size_16
        data = "secreto".b
        assert_equal data, pkcs7_unpad(pkcs7_pad(data, block_size: 16))
    end
end

puts "\n=== DEMO pkcs7_pad ==="

ejemplos = ["A", "HOLA", "12345678", "SECRETO!", "MENSAJELARGO"]
ejemplos.each do |msg|
  padded = pkcs7_pad(msg.b, block_size: 8)
  puts "  '#{msg}' (#{msg.bytesize}B) => hex: #{padded.unpack1('H*')} (#{padded.bytesize}B)"
end

puts "\n=== DEMO pkcs7_unpad ==="
ejemplos.each do |msg|
  padded   = pkcs7_pad(msg.b, block_size: 8)
  unpadded = pkcs7_unpad(padded)
  puts "  hex: #{padded.unpack1('H*')} => '#{unpadded}'"
end
