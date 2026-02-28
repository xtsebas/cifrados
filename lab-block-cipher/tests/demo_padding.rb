require_relative '../src/utils/manual_padding'

BLOCK = 8   # DES block size

def show_padding(label, msg, block_size: BLOCK)
  original = msg.b
  padded   = pkcs7_pad(original, block_size: block_size)
  pad_len  = padded.bytesize - original.bytesize
  pad_val  = "0x#{pad_len.to_s(16).rjust(2, '0')}"

  orig_bytes = original.bytes.map { |b| b.to_s(16).rjust(2, '0') }.join(' ')
  pad_bytes  = ([pad_len.to_s(16).rjust(2, '0')] * pad_len).join(' ')

  recovered  = pkcs7_unpad(padded)

  puts "\n#{label}"
  puts "  Original (texto) : \"#{msg}\""
  puts "  Original (hex)   : #{orig_bytes}"
  puts "  Tamano original  : #{original.bytesize} bytes"
  puts "  Block size       : #{block_size} bytes"
  puts "  Bytes faltantes  : #{block_size} - (#{original.bytesize} % #{block_size})" \
       " = #{pad_len} => agregar #{pad_len} bytes de valor #{pad_val}"
  puts "  Padded   (hex)   : #{padded.unpack1('H*')}"
  puts "  Desglose         : [#{orig_bytes}] + [#{pad_bytes}]"
  puts "  Tamano padded    : #{padded.bytesize} bytes (multiplo de #{block_size})"
  puts "  unpad == original: #{recovered == original}"
end

puts "=" * 60
puts "PKCS#7 Padding — Demostracion con bloque DES (8 bytes)"
puts "=" * 60
puts "\nRegla PKCS#7: si faltan N bytes para completar el bloque,"
puts "agregar N bytes, cada uno con el valor N."
puts "Caso especial: si el mensaje ya es multiplo exacto del"
puts "bloque, agregar un bloque completo de padding."

show_padding("Mensaje de 5 bytes: \"HELLO\"",    "HELLO")
show_padding("Mensaje de 8 bytes: \"12345678\"", "12345678")
show_padding("Mensaje de 10 bytes: \"HOLA MUNDO\"", "HOLA MUNDO")

puts "\n" + "=" * 60
puts "RESUMEN — cuantos bytes se agregan"
puts "=" * 60
puts "\n  Tamano | Bytes padding | Valor padding | Tamano final"
puts "  -------|---------------|---------------|-------------"
[5, 8, 10].each do |n|
  msg      = ("A" * n).b
  padded   = pkcs7_pad(msg, block_size: BLOCK)
  pad_len  = padded.bytesize - n
  pad_val  = pad_len
  puts "  #{n.to_s.rjust(6)} | #{pad_len.to_s.rjust(13)} | " \
       "#{("0x" + pad_val.to_s(16).rjust(2,'0')).rjust(13)} | #{padded.bytesize}"
end

puts "\n" + "=" * 60
puts "ROUNDTRIP — pkcs7_pad + pkcs7_unpad"
puts "=" * 60
["HELLO", "12345678", "HOLA MUNDO"].each do |msg|
  padded    = pkcs7_pad(msg.b, block_size: BLOCK)
  recovered = pkcs7_unpad(padded)
  puts "\n  pad -> unpad(\"#{msg}\") => \"#{recovered}\"  [OK: #{recovered == msg.b}]"
end
