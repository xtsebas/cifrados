require 'openssl'

MANIFEST = "SHA256SUMS.txt"

module ManifestGenerator
  def self.generate(paths)
    File.delete(MANIFEST) if File.exist?(MANIFEST)

    puts "\nMediSoft Release Publisher — generando manifiesto SHA-256"
    puts "-" * 60

    added = 0
    paths.each do |path|
      unless File.exist?(path)
        puts "[WARN] No encontrado: #{path}"
        next
      end
      hash = OpenSSL::Digest::SHA256.hexdigest(File.binread(path))
      File.open(MANIFEST, "a") { |f| f.puts("#{hash}  #{path}") }
      puts "[+] #{File.basename(path).ljust(30)} #{hash}"
      added += 1
    end

    puts "-" * 60
    puts "Manifiesto generado: #{MANIFEST} (#{added} archivos)"
  end
end
