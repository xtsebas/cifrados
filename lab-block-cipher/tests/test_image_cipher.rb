require 'minitest/autorun'
require 'fileutils'
require_relative '../src/image_cipher'
require_relative '../src/utils/key_generator'

IMAGES_DIR = File.expand_path('../images', __dir__)
FileUtils.mkdir_p(IMAGES_DIR)

class TestImageCipher < Minitest::Test

  def setup
    @key      = generate_aes_key(key_size: 256)
    @original = File.join(IMAGES_DIR, 'test_original.bmp')
    @ecb_out  = File.join(IMAGES_DIR, 'test_ecb.bmp')
    @cbc_out  = File.join(IMAGES_DIR, 'test_cbc.bmp')
    @dec_ecb  = File.join(IMAGES_DIR, 'test_dec_ecb.bmp')
    @dec_cbc  = File.join(IMAGES_DIR, 'test_dec_cbc.bmp')

    bmp_create_test(@original)
  end

  def teardown
    [@ecb_out, @cbc_out, @dec_ecb, @dec_cbc].each do |f|
      File.delete(f) if File.exist?(f)
    end
    File.delete(@original) if File.exist?(@original)
  end

  # ── bmp_read / bmp_write ──────────────────────────────────────────────────

  def test_bmp_signature
    bmp = bmp_read(@original)
    assert_equal "BM", bmp[:header][0, 2]
  end

  def test_bmp_pixel_offset_is_54
    bmp = bmp_read(@original)
    assert_equal 54, bmp[:header][10, 4].unpack1('V')
  end

  def test_bmp_pixel_data_size
    bmp = bmp_read(@original)
    # 128x128 image, 24bpp, row padded to 4 bytes => row = 384 bytes
    expected = 384 * 128
    assert_equal expected, bmp[:pixel_data].bytesize
  end

  def test_pixel_data_multiple_of_16
    bmp = bmp_read(@original)
    assert_equal 0, bmp[:pixel_data].bytesize % 16,
                 "Pixel data must be a multiple of 16 for clean AES block alignment"
  end

  def test_roundtrip_write_read
    bmp = bmp_read(@original)
    tmp = File.join(IMAGES_DIR, 'tmp_roundtrip.bmp')
    bmp_write(tmp, bmp[:header], bmp[:pixel_data])
    bmp2 = bmp_read(tmp)
    assert_equal bmp[:pixel_data], bmp2[:pixel_data]
  ensure
    File.delete(tmp) if File.exist?(tmp)
  end

  # ── ECB image encryption ──────────────────────────────────────────────────

  def test_ecb_creates_output_file
    encrypt_bmp_ecb(@original, @ecb_out, @key)
    assert File.exist?(@ecb_out)
  end

  def test_ecb_output_is_valid_bmp
    encrypt_bmp_ecb(@original, @ecb_out, @key)
    assert_equal "BM", File.binread(@ecb_out, 2)
  end

  def test_ecb_pixel_data_differs_from_original
    encrypt_bmp_ecb(@original, @ecb_out, @key)
    orig = bmp_read(@original)[:pixel_data]
    encr = bmp_read(@ecb_out)[:pixel_data]
    refute_equal orig, encr
  end

  def test_ecb_roundtrip
    encrypt_bmp_ecb(@original, @ecb_out, @key)
    decrypt_bmp_ecb(@ecb_out, @dec_ecb, @key)
    orig_pixels = bmp_read(@original)[:pixel_data]
    dec_pixels  = bmp_read(@dec_ecb)[:pixel_data]
    assert_equal orig_pixels, dec_pixels
  end

  # ECB weakness: identical plaintext blocks => identical ciphertext blocks.
  # In a uniform color region, the RGB byte pattern repeats every 48 bytes
  # (= 16 pixels = 3 AES blocks), because LCM(3, 16) = 48.
  # Block 0 and block 3 (offset 48) contain identical bytes => same ciphertext.
  def test_ecb_shows_block_patterns
    encrypt_bmp_ecb(@original, @ecb_out, @key)
    ecb_pixels = bmp_read(@ecb_out)[:pixel_data]

    block0 = ecb_pixels[0,  16]
    block3 = ecb_pixels[48, 16]
    block6 = ecb_pixels[96, 16]

    assert_equal block0, block3,
                 "ECB: identical plaintext blocks must produce identical ciphertext"
    assert_equal block0, block6,
                 "ECB: periodic pattern must repeat every 3 blocks for 24bpp data"
  end

  # ── CBC image encryption ──────────────────────────────────────────────────

  def test_cbc_creates_output_file
    encrypt_bmp_cbc(@original, @cbc_out, @key)
    assert File.exist?(@cbc_out)
  end

  def test_cbc_output_is_valid_bmp
    encrypt_bmp_cbc(@original, @cbc_out, @key)
    assert_equal "BM", File.binread(@cbc_out, 2)
  end

  def test_cbc_different_output_each_time
    tmp = File.join(IMAGES_DIR, 'tmp_cbc2.bmp')
    encrypt_bmp_cbc(@original, @cbc_out, @key)
    encrypt_bmp_cbc(@original, tmp,      @key)
    refute_equal File.binread(@cbc_out), File.binread(tmp)
  ensure
    File.delete(tmp) if File.exist?(tmp)
  end

  def test_cbc_roundtrip
    encrypt_bmp_cbc(@original, @cbc_out, @key)
    decrypt_bmp_cbc(@cbc_out, @dec_cbc, @key)
    orig_pixels = bmp_read(@original)[:pixel_data]
    dec_pixels  = bmp_read(@dec_cbc)[:pixel_data]
    assert_equal orig_pixels, dec_pixels
  end

  # CBC hides patterns: identical plaintext blocks produce different ciphertext.
  # The stored pixel data is: IV (16 bytes) | ciphertext.
  # Even blocks that had identical plaintext (as shown in test_ecb_shows_block_patterns)
  # will differ in CBC output.
  def test_cbc_hides_block_patterns
    encrypt_bmp_cbc(@original, @cbc_out, @key)
    cbc_pixels = bmp_read(@cbc_out)[:pixel_data]

    # Skip the IV (first 16 bytes); compare ciphertext blocks at the same
    # offsets that were identical under ECB
    ct_start = 16
    block0 = cbc_pixels[ct_start,      16]
    block3 = cbc_pixels[ct_start + 48, 16]
    block6 = cbc_pixels[ct_start + 96, 16]

    refute_equal block0, block3,
                 "CBC must produce different ciphertext even for identical plaintext blocks"
    refute_equal block0, block6
  end

end

# ── Visual Demo ───────────────────────────────────────────────────────────────
# Run this file directly to generate the comparison images in lab-block-cipher/images/.
# Open the three .bmp files side by side to see the ECB vs CBC difference visually.
puts "\n=== AES Image Cipher: ECB vs CBC Visual Demo ==="

key      = generate_aes_key(key_size: 256)
original = File.join(IMAGES_DIR, 'demo_original.bmp')
ecb_out  = File.join(IMAGES_DIR, 'demo_ecb.bmp')
cbc_out  = File.join(IMAGES_DIR, 'demo_cbc.bmp')
dec_ecb  = File.join(IMAGES_DIR, 'demo_dec_ecb.bmp')
dec_cbc  = File.join(IMAGES_DIR, 'demo_dec_cbc.bmp')

bmp_create_test(original)
puts "Original image   : #{original}"
puts "  (4 solid-color quadrants: Red | Green / Blue | White)"

encrypt_bmp_ecb(original, ecb_out, key)
puts "\nECB encrypted    : #{ecb_out}"
puts "  => Open this file: color blocks are still visible — ECB leaks structure!"

encrypt_bmp_cbc(original, cbc_out, key)
puts "\nCBC encrypted    : #{cbc_out}"
puts "  => Open this file: looks like random noise — CBC hides all structure."

decrypt_bmp_ecb(ecb_out, dec_ecb, key)
puts "\nECB decrypted    : #{dec_ecb}  (should match original)"

decrypt_bmp_cbc(cbc_out, dec_cbc, key)
puts "CBC decrypted    : #{dec_cbc}  (should match original)"

puts "\nKey (hex): #{key.unpack1('H*')}"
