require_relative 'hash_explore'
require_relative 'keys'
require_relative 'manifest_generator'
require_relative 'package_verify'
require_relative 'sign_manifest'

puts "\n" + "=" * 70
puts " PROBLEMA 1: Comparativa de algoritmos de hash"
puts "=" * 70
rows = HashExplore.compare_strings("MediSoft-v2.1.0", "medisoft-v2.1.0")
HashExplore.print_table(rows)

puts "\n" + "=" * 70
puts " PROBLEMA 2: Verificacion de contrasenas en HIBP"
puts "=" * 70
results = PasswordChecker.check_all
PasswordChecker.print_results(results)

puts "\n" + "=" * 70
puts " PROBLEMA 3: Verificacion de integridad de paquetes"
puts "=" * 70
PACKAGE_FILES = %w[
  packages/config.ini
  packages/installer.sh
  packages/medisoft_core.dll
  packages/updater.rb
  packages/license.txt
]
ManifestGenerator.generate(PACKAGE_FILES)
puts "\n--- Verificacion inicial (sin modificaciones) ---"
PackageVerify.verify
puts "\n--- Simulando ataque: modificando 1 byte en config.ini ---"
PackageVerify.tamper("packages/config.ini")
puts "\n--- Verificacion post-ataque ---"
PackageVerify.verify

puts "\n" + "=" * 70
puts " PROBLEMA 4: Firma digital del manifiesto"
puts "=" * 70
SignManifest.run
