require_relative 'hash_explore'
require_relative 'keys'

# --- Problema 1: Comparativa de algoritmos ---
rows = HashExplore.compare_strings("MediSoft-v2.1.0", "medisoft-v2.1.0")
HashExplore.print_table(rows)

# --- Problema 2: Verificacion HIBP ---
results = PasswordChecker.check_all
PasswordChecker.print_results(results)
