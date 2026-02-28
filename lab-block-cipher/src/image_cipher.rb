require_relative 'aes_ecb'
require_relative 'aes_cbc'
require_relative 'utils/bmp_utils'

# Encrypts the pixel data of a BMP image with AES-256-ECB.
#
# The BMP header is kept intact so the output file is still openable by image
# viewers. Because ECB is deterministic, identical 16-byte pixel blocks produce
# identical ciphertext blocks — large uniform color areas remain visually uniform
# in the encrypted image, making the original structure clearly visible.
#
# Output layout: original header | ECB-encrypted pixel data
#
# Parameters:
#   input_path:  path to the source BMP file
#   output_path: path for the encrypted BMP file
#   key:         32-byte AES-256 key
def encrypt_bmp_ecb(input_path, output_path, key)
  bmp = bmp_read(input_path)
  encrypted_pixels = aes_ecb_encrypt(bmp[:pixel_data], key)
  bmp_write(output_path, bmp[:header], encrypted_pixels)
end

# Decrypts a BMP image previously encrypted with encrypt_bmp_ecb.
#
# Parameters:
#   input_path:  path to the ECB-encrypted BMP file
#   output_path: path for the recovered BMP file
#   key:         32-byte AES-256 key (same as used for encryption)
def decrypt_bmp_ecb(input_path, output_path, key)
  bmp = bmp_read(input_path)
  decrypted_pixels = aes_ecb_decrypt(bmp[:pixel_data], key)
  bmp_write(output_path, bmp[:header], decrypted_pixels)
end

# Encrypts the pixel data of a BMP image with AES-256-CBC using a random IV.
#
# The BMP header is kept intact. The random IV is prepended to the ciphertext
# and stored as part of the pixel data section. Because CBC chains each block
# with the previous ciphertext (starting from the random IV), even identical
# pixel blocks produce different ciphertext — the image looks like random noise.
#
# Output layout: original header | IV (16 bytes) | CBC-encrypted pixel data
#
# Parameters:
#   input_path:  path to the source BMP file
#   output_path: path for the encrypted BMP file
#   key:         32-byte AES-256 key
def encrypt_bmp_cbc(input_path, output_path, key)
  bmp = bmp_read(input_path)
  encrypted_pixels = aes_cbc_encrypt(bmp[:pixel_data], key)  # IV prepended inside
  bmp_write(output_path, bmp[:header], encrypted_pixels)
end

# Decrypts a BMP image previously encrypted with encrypt_bmp_cbc.
# Extracts the IV from the first 16 bytes of the pixel data section.
#
# Parameters:
#   input_path:  path to the CBC-encrypted BMP file
#   output_path: path for the recovered BMP file
#   key:         32-byte AES-256 key (same as used for encryption)
def decrypt_bmp_cbc(input_path, output_path, key)
  bmp = bmp_read(input_path)
  decrypted_pixels = aes_cbc_decrypt(bmp[:pixel_data], key)
  bmp_write(output_path, bmp[:header], decrypted_pixels)
end
