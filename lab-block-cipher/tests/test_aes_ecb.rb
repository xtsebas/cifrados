require 'minitest/autorun'
require_relative '../src/aes_ecb'
require_relative '../src/utils/key_generator'

class TestAesEcb < Minitest::Test

  def setup
    @key = generate_aes_key(key_size: 256)
  end

  # ── Key generation ───────────────────────────────────────────────────────

  def test_key_length
    assert_equal 32, @key.bytesize
  end

  def test_key_is_random
    k1 = generate_aes_key(key_size: 256)
    k2 = generate_aes_key(key_size: 256)
    refute_equal k1, k2
  end

  # ── Ciphertext properties ─────────────────────────────────────────────────

  def test_ciphertext_differs_from_plaintext
    ct = aes_ecb_encrypt("HELLO WORLD".b, @key)
    refute_equal "HELLO WORLD".b, ct
  end

  def test_ciphertext_is_multiple_of_16
    [1, 7, 15, 16, 17, 32, 100].each do |n|
      ct = aes_ecb_encrypt(("A" * n).b, @key)
      assert_equal 0, ct.bytesize % 16, "Ciphertext not multiple of 16 for #{n}-byte input"
    end
  end

  # ── Roundtrip ─────────────────────────────────────────────────────────────

  def test_roundtrip_short
    pt = "HOLA".b
    assert_equal pt, aes_ecb_decrypt(aes_ecb_encrypt(pt, @key), @key)
  end

  def test_roundtrip_exact_block
    pt = ("A" * 16).b
    assert_equal pt, aes_ecb_decrypt(aes_ecb_encrypt(pt, @key), @key)
  end

  def test_roundtrip_multiple_blocks
    pt = ("Hello, AES ECB! " * 4).b
    assert_equal pt, aes_ecb_decrypt(aes_ecb_encrypt(pt, @key), @key)
  end

  def test_roundtrip_varios_tamanios
    (1..64).each do |n|
      pt = (0...n).map { rand(256).chr }.join.b
      assert_equal pt, aes_ecb_decrypt(aes_ecb_encrypt(pt, @key), @key),
                   "Roundtrip failed for #{n}-byte input"
    end
  end

  # ── ECB properties ────────────────────────────────────────────────────────

  def test_determinista
    pt  = "ECB is deterministic".b
    ct1 = aes_ecb_encrypt(pt, @key)
    ct2 = aes_ecb_encrypt(pt, @key)
    assert_equal ct1, ct2
  end

  # Core ECB weakness: identical plaintext blocks → identical ciphertext blocks.
  # This is what makes structure visible when encrypting images with ECB.
  def test_identical_blocks_produce_identical_ciphertext
    block = "AAAAAAAAAAAAAAAA"   # 16 bytes = one AES block
    pt    = (block * 4).b
    ct    = aes_ecb_encrypt(pt, @key)

    blocks = (0...4).map { |i| ct[i * 16, 16] }
    assert_equal 1, blocks.uniq.size,
                 "All identical plaintext blocks must produce identical ciphertext blocks"
  end

  def test_diferente_clave_diferente_ciphertext
    key2 = generate_aes_key(key_size: 256)
    pt   = "Same plaintext".b
    refute_equal aes_ecb_encrypt(pt, @key), aes_ecb_encrypt(pt, key2)
  end

end

# ── Demo ─────────────────────────────────────────────────────────────────────
puts "\n=== AES-256-ECB Demo ==="
key = generate_aes_key(key_size: 256)
puts "Key (hex): #{key.unpack1('H*')}"

[
  "HOLA MUNDO",
  "Bloque exacto!!!",    # exactly 16 bytes
  "Texto mas largo que un bloque AES"
].each do |msg|
  ct = aes_ecb_encrypt(msg.b, key)
  pt = aes_ecb_decrypt(ct, key)
  puts "\nPlaintext : #{msg}"
  puts "Ciphertext: #{ct.unpack1('H*')}"
  puts "Decrypted : #{pt}"
end

puts "\n--- ECB Weakness: identical plaintext blocks ---"
block = "AAAAAAAAAAAAAAAA"
ct    = aes_ecb_encrypt((block * 3).b, key)
(0...3).each { |i| puts "  Block #{i}: #{ct[i * 16, 16].unpack1('H*')}" }
puts "(all three blocks are identical => structure is visible)"
