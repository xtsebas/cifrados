# Utilities for reading, writing, and creating BMP image files.
# Only the pixel data section is modified during encryption;
# the BMP header is always preserved so files remain viewable.

# Reads a BMP file and separates the header from raw pixel data.
#
# BMP file layout:
#   Bytes  0-1:  "BM" signature
#   Bytes  2-5:  File size (uint32, little-endian)
#   Bytes  6-9:  Reserved
#   Bytes 10-13: Pixel data offset (uint32, little-endian)
#   Bytes 14+:   DIB header + optional color table + pixel data
#
# Returns: { header: String(binary), pixel_data: String(binary) }
def bmp_read(path)
  raw = File.binread(path)
  raise ArgumentError, "Not a BMP file: missing 'BM' signature" unless raw[0, 2] == "BM".b

  pixel_offset = raw[10, 4].unpack1('V')
  {
    header:     raw[0, pixel_offset].b,
    pixel_data: raw[pixel_offset..].b
  }
end

# Writes a BMP file from a header and (possibly modified) pixel data.
# Updates the file-size field in the header to reflect the new total size.
def bmp_write(path, header, pixel_data)
  hdr = header.dup.b
  hdr[2, 4] = [hdr.bytesize + pixel_data.bytesize].pack('V')
  File.binwrite(path, hdr + pixel_data.b)
end

# Creates a 128x128, 24-bit BMP with four solid-color quadrants.
#
# Quadrant layout:
#   Top-left  = Red    | Top-right  = Green
#   Bot-left  = Blue   | Bot-right  = White
#
# Alignment guarantee (important for the ECB visual demo):
#   - Row byte count = 128 x 3 = 384 = 24 x 16  (multiple of AES block size)
#   - Left/right boundary falls at byte 192 = 12 x 16 within each row,
#     so no AES block straddles the color boundary between quadrants.
#   - This makes ECB's pattern-preservation clearly visible.
#
# Parameters:
#   path:   output file path
#   width:  image width in pixels (default 128)
#   height: image height in pixels (default 128)
def bmp_create_test(path, width: 128, height: 128)
  bpp      = 24
  row_size = (((bpp * width) + 31) / 32) * 4   # pad rows to 4-byte boundary
  px_size  = row_size * height
  fsize    = 54 + px_size

  # All pack() calls return ASCII-8BIT (binary), so every piece is binary from the start.

  # File header (14 bytes)
  fhdr = [66, 77].pack('CC')     +  # "BM" as bytes — avoids UTF-8 literal
         [fsize].pack('V')       +  # total file size
         [0].pack('V')           +  # reserved
         [54].pack('V')             # pixel data offset

  # DIB header / BITMAPINFOHEADER (40 bytes)
  # Negative height => top-down row order (row 0 = top of displayed image)
  dhdr = [40].pack('V')           +
         [width].pack('l<')       +
         [-height].pack('l<')     +
         [1].pack('v')            +  # color planes
         [bpp].pack('v')          +  # bits per pixel
         [0].pack('V')            +  # BI_RGB: no compression
         [px_size].pack('V')      +
         [2835].pack('V')         +  # ~72 dpi X
         [2835].pack('V')         +  # ~72 dpi Y
         [0].pack('V')            +  # colors in table
         [0].pack('V')               # important colors

  header = fhdr + dhdr   # both are already binary from pack()

  half_h = height / 2
  half_w = width  / 2

  # Pixel colors in BGR byte order — local variables, all binary from pack()
  red   = [0x00, 0x00, 0xFF].pack('C3')
  green = [0x00, 0xFF, 0x00].pack('C3')
  blue  = [0xFF, 0x00, 0x00].pack('C3')
  white = [0xFF, 0xFF, 0xFF].pack('C3')

  pixels = "".b
  height.times do |y|
    row = "".b
    width.times do |x|
      row += if    x < half_w && y < half_h  then red
               elsif x >= half_w && y < half_h then green
               elsif x < half_w               then blue
               else                                white
               end
    end
    # Pad each row to a 4-byte boundary (BMP requirement)
    pad_len = (4 - row.bytesize % 4) % 4
    row += [0].pack('C') * pad_len
    pixels += row
  end

  File.binwrite(path, header + pixels)
  { header: header, pixel_data: pixels }
end
