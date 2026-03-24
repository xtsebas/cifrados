require 'openssl'

module HashExplore
  ALGORITHMS = [
    { name: "MD5",      bits: 128, digest: ->(s) { OpenSSL::Digest::MD5.hexdigest(s) } },
    { name: "SHA-1",    bits: 160, digest: ->(s) { OpenSSL::Digest::SHA1.hexdigest(s) } },
    { name: "SHA-256",  bits: 256, digest: ->(s) { OpenSSL::Digest::SHA256.hexdigest(s) } },
    { name: "SHA3-256", bits: 256, digest: ->(s) { OpenSSL::Digest.new("SHA3-256").hexdigest(s) } },
  ]

  def self.compare_strings(*strings)
    rows = []
    strings.each do |str|
      ALGORITHMS.each do |alg|
        rows << {
          input:   str,
          algo:    alg[:name],
          bits:    alg[:bits],
          hex_len: alg[:bits] / 4,
          hash:    alg[:digest].call(str)
        }
      end
    end
    rows
  end

  def self.print_table(rows)
    col_input   = 17
    col_algo    = 10
    col_bits    =  7
    col_hex_len =  9
    col_hash    = 64

    sep = "+#{"-" * (col_input + 2)}+#{"-" * (col_algo + 2)}+#{"-" * (col_bits + 2)}+#{"-" * (col_hex_len + 2)}+#{"-" * (col_hash + 2)}+"

    puts "\nComparativa de algoritmos de hash - MediSoft"
    puts sep
    puts "| %-#{col_input}s | %-#{col_algo}s | %#{col_bits}s | %#{col_hex_len}s | %-#{col_hash}s |" %
      ["Input", "Algoritmo", "Bits", "Hex len", "Hash"]
    puts sep

    rows.each_with_index do |r, i|
      puts sep if i > 0 && i % ALGORITHMS.size == 0
      puts "| %-#{col_input}s | %-#{col_algo}s | %#{col_bits}d | %#{col_hex_len}d | %-#{col_hash}s |" %
        [r[:input], r[:algo], r[:bits], r[:hex_len], r[:hash]]
    end

    puts sep
  end
end
