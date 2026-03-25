require 'openssl'

MANIFEST = "SHA256SUMS.txt" unless defined?(MANIFEST)

module PackageVerify
  def self.verify
    unless File.exist?(MANIFEST)
      puts "[ERROR] Manifiesto no encontrado: #{MANIFEST}"
      return
    end

    results      = []
    ok_count     = 0
    failed_count = 0

    File.readlines(MANIFEST).each do |line|
      line.strip!
      next if line.empty?

      expected_hash, filepath = line.split(/\s+/, 2)

      unless File.exist?(filepath)
        results << { file: filepath, status: :missing }
        failed_count += 1
        next
      end

      actual_hash = OpenSSL::Digest::SHA256.hexdigest(File.binread(filepath))

      if actual_hash == expected_hash
        results << { file: filepath, status: :ok }
        ok_count += 1
      else
        results << { file: filepath, status: :tampered, expected: expected_hash, actual: actual_hash }
        failed_count += 1
      end
    end

    col_file   = 42
    col_status = 10
    sep = "+#{"-" * (col_file + 2)}+#{"-" * (col_status + 2)}+"

    puts "\nMediSoft Integrity Verifier"
    puts sep
    puts "| %-#{col_file}s | %-#{col_status}s |" % ["Archivo", "Estado"]
    puts sep

    results.each do |r|
      label = case r[:status]
              when :ok       then "OK"
              when :tampered then "CORRUPTO"
              when :missing  then "NO EXISTE"
              end
      puts "| %-#{col_file}s | %-#{col_status}s |" % [r[:file], label]
    end

    puts sep
    puts "Resumen: #{ok_count} correctos / #{failed_count} fallidos"

    results.select { |r| r[:status] == :tampered }.each do |r|
      puts "\n[!] #{r[:file]}"
      puts "    Esperado : #{r[:expected]}"
      puts "    Recibido : #{r[:actual]}"
    end
  end

  def self.tamper(filepath)
    unless File.exist?(filepath)
      puts "[ERROR] Archivo no encontrado: #{filepath}"
      return
    end
    content = File.binread(filepath)
    content[10] = content[10] == "X" ? "Y" : "X"
    File.binwrite(filepath, content)
    puts "[ATAQUE] Byte modificado en: #{filepath}"
  end
end
