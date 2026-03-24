require 'openssl'
require 'net/http'
require 'uri'

module PasswordChecker
  PASSWORDS = ["admin", "123456", "hospital", "medisoft2024", "contrasena123", "password", "thiagohugo2014"]

  def self.sha256(str)
    OpenSSL::Digest::SHA256.hexdigest(str).upcase
  end

  def self.sha1(str)
    OpenSSL::Digest::SHA1.hexdigest(str).upcase
  end

  # HIBP usa k-Anonymity con SHA-1: solo se envian los primeros 5 chars.
  # Nunca sale el hash completo de la maquina.
  def self.check_hibp(password)
    sha1_hash = sha1(password)
    prefix    = sha1_hash[0..4]
    suffix    = sha1_hash[5..]

    uri      = URI("https://api.pwnedpasswords.com/range/#{prefix}")
    response = Net::HTTP.get(uri)

    match = response.lines.find { |line| line.upcase.start_with?(suffix) }
    match ? match.split(':').last.strip.to_i : 0
  end

  def self.check_all
    PASSWORDS.map do |pwd|
      count = check_hibp(pwd)
      {
        password:    pwd,
        sha256:      sha256(pwd),
        sha1_prefix: sha1(pwd)[0..4],
        pwned_count: count
      }
    end
  end

  def self.print_results(results)
    col_pwd    = 14
    col_sha256 = 64
    col_prefix =  7
    col_count  = 10

    sep = "+#{"-" * (col_pwd + 2)}+#{"-" * (col_sha256 + 2)}+#{"-" * (col_prefix + 2)}+#{"-" * (col_count + 2)}+"

    puts "\nVerificacion de contrasenas en HIBP"
    puts sep
    puts "| %-#{col_pwd}s | %-#{col_sha256}s | %-#{col_prefix}s | %#{col_count}s |" %
      ["Contrasena", "SHA-256", "SHA1[0:5]", "Filtraciones"]
    puts sep

    results.each do |r|
      status = r[:pwned_count] > 0 ? "#{r[:pwned_count]} veces" : "No encontrada"
      puts "| %-#{col_pwd}s | %-#{col_sha256}s | %-#{col_prefix}s | %#{col_count}s |" %
        [r[:password], r[:sha256], r[:sha1_prefix], status]
    end

    puts sep

    puts "\n[!] Contrasenas comprometidas:"
    results.select { |r| r[:pwned_count] > 0 }.each do |r|
      puts "    #{r[:password].ljust(16)} aparece #{r[:pwned_count]} veces en filtraciones conocidas"
    end
  end
end
