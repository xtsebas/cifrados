require 'minitest/autorun'
require_relative '../src/aes_cbc'
require_relative '../src/utils/key_generator'

class TestAesCbc < Minitest::Test

  def setup
    @key = generate_aes_key(key_size: 256)
  end

  # ── Key and IV generation ─────────────────────────────────────────────────

  def test_key_length
    assert_equal 32, @key.bytesize
  end

  def test_iv_length
    iv = generate_iv(block_size: 16)
    assert_equal 16, iv.bytesize
  end

  def test_iv_is_random
    iv1 = generate_iv(block_size: 16)
    iv2 = generate_iv(block_size: 16)
    refute_equal iv1, iv2
  end

  # ── Output format ─────────────────────────────────────────────────────────

  def test_output_starts_with_iv
    # Output must contain at least IV (16 bytes) + one encrypted block (16 bytes)
    out = aes_cbc_encrypt("HOLA".b, @key)
    assert out.bytesize >= 32
  end

  def test_ciphertext_multiple_of_16_after_iv
    [1, 15, 16, 17, 32, 100].each do |n|
      out = aes_cbc_encrypt(("A" * n).b, @key)
      ct  = out[16..]   # strip IV
      assert_equal 0, ct.bytesize % 16,
                   "Ciphertext (after IV) not a multiple of 16 for #{n}-byte input"
    end
  end

  def test_iv_distinto_por_cifrado
    pt  = "Mismo texto".b
    iv1 = aes_cbc_encrypt(pt, @key)[0, 16]
    iv2 = aes_cbc_encrypt(pt, @key)[0, 16]
    refute_equal iv1, iv2
  end

  # ── CBC non-determinism ───────────────────────────────────────────────────

  def test_no_determinista
    # Each call generates a different IV => different ciphertext
    pt  = "CBC es no determinista".b
    ct1 = aes_cbc_encrypt(pt, @key)
    ct2 = aes_cbc_encrypt(pt, @key)
    refute_equal ct1, ct2
  end

  # ── Roundtrip ─────────────────────────────────────────────────────────────

  def test_roundtrip_short
    pt = "HOLA".b
    assert_equal pt, aes_cbc_decrypt(aes_cbc_encrypt(pt, @key), @key)
  end

  def test_roundtrip_exact_block
    pt = ("B" * 16).b
    assert_equal pt, aes_cbc_decrypt(aes_cbc_encrypt(pt, @key), @key)
  end

  def test_roundtrip_multiple_blocks
    pt = ("Hello AES-CBC!! " * 4).b
    assert_equal pt, aes_cbc_decrypt(aes_cbc_encrypt(pt, @key), @key)
  end

  def test_roundtrip_varios_tamanios
    (1..64).each do |n|
      pt = (0...n).map { rand(256).chr }.join.b
      assert_equal pt, aes_cbc_decrypt(aes_cbc_encrypt(pt, @key), @key),
                   "Roundtrip failed for #{n}-byte input"
    end
  end

  # ── CBC security properties ───────────────────────────────────────────────

  # CBC chains blocks: identical plaintext blocks produce different ciphertext.
  # This is why CBC hides patterns when encrypting images.
  def test_identical_blocks_produce_different_ciphertext
    block = "AAAAAAAAAAAAAAAA"   # 16 bytes = one AES block
    pt    = (block * 4).b
    out   = aes_cbc_encrypt(pt, @key)
    ct    = out[16..]   # strip IV

    blocks = (0...4).map { |i| ct[i * 16, 16] }
    assert_equal 4, blocks.uniq.size,
                 "CBC must produce different ciphertext for identical plaintext blocks"
  end

  def test_wrong_key_does_not_decrypt
    pt  = "Secreto secreto!".b
    out = aes_cbc_encrypt(pt, @key)
    bad = generate_aes_key(key_size: 256)

    begin
      result = aes_cbc_decrypt(out, bad)
      refute_equal pt, result, "Decrypting with wrong key must not recover original plaintext"
    rescue OpenSSL::Cipher::CipherError
      pass   # padding error with wrong key is the expected common case
    end
  end

end

# ── Demo ─────────────────────────────────────────────────────────────────────
puts "\n=== AES-256-CBC Demo ==="
key = generate_aes_key(key_size: 256)
puts "Key (hex): #{key.unpack1('H*')}"

[
  "HOLA MUNDO",
  "Bloque exacto!!!",    # exactly 16 bytes
  "Texto mas largo que un bloque AES"
].each do |msg|
  out = aes_cbc_encrypt(msg.b, key)
  iv  = out[0, 16]
  ct  = out[16..]
  pt  = aes_cbc_decrypt(out, key)
  puts "\nPlaintext : #{msg}"
  puts "IV        : #{iv.unpack1('H*')}"
  puts "Ciphertext: #{ct.unpack1('H*')}"
  puts "Decrypted : #{pt}"
end

puts "\n--- CBC vs ECB: identical plaintext blocks ---"
block = "AAAAAAAAAAAAAAAA"
out   = aes_cbc_encrypt((block * 3).b, key)
ct    = out[16..]
(0...3).each { |i| puts "  Block #{i}: #{ct[i * 16, 16].unpack1('H*')}" }
puts "(all three blocks differ => CBC hides patterns)"
