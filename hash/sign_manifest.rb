require 'openssl'
require_relative '../RSA/keys_generator'

PRIVATE_KEY_PATH = "medisoft_priv.pem"
PUBLIC_KEY_PATH  = "medisoft_pub.pem"
MANIFEST_PATH    = "SHA256SUMS.txt"
SIGNATURE_PATH   = "SHA256SUMS.sig"
KEY_PASSPHRASE   = "medisoft-lab-2024"  

module SignManifest
  def self.generate_keys
    puts "\nGenerando par de claves RSA de 2048 bits..."
    keys = generate_rsa_keys(2048)
    save_keys(keys, PRIVATE_KEY_PATH, PUBLIC_KEY_PATH, KEY_PASSPHRASE)
    puts "[!]  Clave PRIVADA (#{PRIVATE_KEY_PATH}): exclusiva de MediSoft, NO compartir."
    puts "[OK] Clave PUBLICA (#{PUBLIC_KEY_PATH}):  puede distribuirse a los hospitales."
  end

  def self.sign
    unless File.exist?(MANIFEST_PATH)
      puts "[ERROR] Manifiesto no encontrado: #{MANIFEST_PATH}"
      return
    end

    unless File.exist?(PRIVATE_KEY_PATH)
      puts "[ERROR] Clave privada no encontrada: #{PRIVATE_KEY_PATH}"
      return
    end

    private_key = OpenSSL::PKey::RSA.new(File.read(PRIVATE_KEY_PATH), KEY_PASSPHRASE)
    content     = File.binread(MANIFEST_PATH)
    digest      = OpenSSL::Digest::SHA256.new

    # Firma con PKCS#1
    signature = private_key.sign(digest, content)
    File.binwrite(SIGNATURE_PATH, signature)

    puts "\nFirma generada: #{SIGNATURE_PATH} (#{signature.bytesize} bytes)"
    puts "SHA-256 del manifiesto firmado:"
    puts "  #{OpenSSL::Digest::SHA256.hexdigest(content)}"
  end

  def self.run
    generate_keys
    sign
  end
end
