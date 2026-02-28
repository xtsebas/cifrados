# Módulo de padding PKCS#7 para cifrados de bloque.
# Implementación manual sin usar bibliotecas externas.

# Implementa padding PKCS#7 según RFC 5652.
# Regla: Si faltan N bytes para completar el bloque, agregar N bytes,
# cada uno con el valor N (recuerden seguir la regla de pkcs#7).
# Importante: Si el mensaje es múltiplo exacto del tamaño de bloque,
# se agrega un bloque completo de padding.
# Examples:
#   pkcs7_pad("HOLA".b, 8).unpack1('H*') => '484f4c4104040404'
#   pkcs7_pad("12345678".b, 8).unpack1('H*') => '31323334353637380808080808080808'
def pkcs7_pad(data, block_size: 8)
  pad_len = block_size - (data.bytesize % block_size)
  data + (pad_len.chr * pad_len).b
end

# Elimina padding PKCS#7 de los datos.
# Examples:
#   padded = pkcs7_pad("HOLA".b, 8)
#   pkcs7_unpad(padded) => "HOLA"
def pkcs7_unpad(data)
  pad_len = data.bytes.last
  data[0...-pad_len]
end
