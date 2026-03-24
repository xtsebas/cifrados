require_relative 'hash_explore'

rows = HashExplore.compare_strings("MediSoft-v2.1.0", "medisoft-v2.1.0")
HashExplore.print_table(rows)
