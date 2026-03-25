require 'openssl'

module VerifySignature
  def self.verify(pub_key_path: PUBLIC_KEY_PATH, manifest_path: MANIFEST_PATH, sig_path: SIGNATURE_PATH)
    missing = [pub_key_path, manifest_path, sig_path].reject { |f| File.exist?(f) }
    unless missing.empty?
      puts "[ERROR] Archivos faltantes: #{missing.join(', ')}"
      return false
    end

    pub_key   = OpenSSL::PKey::RSA.new(File.read(pub_key_path))
    content   = File.binread(manifest_path)
    signature = File.binread(sig_path)
    digest    = OpenSSL::Digest::SHA256.new

    valid = pub_key.verify(digest, signature, content)

    if valid
      puts "[OK] Firma valida. El manifiesto es autentico y proviene de MediSoft."
    else
      puts "[FAIL] Firma INVALIDA. El manifiesto fue alterado o no proviene de MediSoft."
    end

    valid
  rescue OpenSSL::PKey::RSAError => e
    puts "[ERROR] Fallo al verificar firma: #{e.message}"
    false
  end

  # Altera un caracter del hash en SHA256SUMS.txt y guarda backup
  def self.tamper_manifest(manifest_path: MANIFEST_PATH)
    content = File.read(manifest_path)
    File.write("#{manifest_path}.bak", content)

    # Cambia el primer caracter del primer hash (a->b, cualquier otro -> a)
    tampered = content.sub(/^([0-9a-f])/) { |c| c == 'a' ? 'b' : 'a' }
    File.write(manifest_path, tampered)
    puts "[ATAQUE] Caracter modificado en #{manifest_path} (backup en #{manifest_path}.bak)"
  end

  # Restaura el manifesto desde backup
  def self.restore_manifest(manifest_path: MANIFEST_PATH)
    backup = "#{manifest_path}.bak"
    unless File.exist?(backup)
      puts "[WARN] No hay backup para restaurar."
      return
    end
    File.write(manifest_path, File.read(backup))
    File.delete(backup)
    puts "[OK] Manifiesto restaurado desde backup."
  end
end
