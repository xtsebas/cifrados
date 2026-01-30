import time
from dynamics_keys import DynamicKeyGenerator


print("\n" + "="*70)
print("    EJEMPLOS DE GENERACIÓN DE LLAVES DINÁMICAS - ASCII")
print("="*70)

generator = DynamicKeyGenerator()

print("\nLLAVE ALEATORIA BÁSICA")
print("-" * 70)

random_key = generator.generate_random_key(16, 'all')
print(f"Llave de 16 caracteres (todos): {random_key}")
print(f"Longitud: {len(random_key)} | Valores ASCII: {[ord(c) for c in random_key[:5]]}...")

print("\nLLAVES CON DIFERENTES CONJUNTOS DE CARACTERES")
print("-" * 70)

key_letters = generator.generate_random_key(12, 'letters')
key_digits = generator.generate_random_key(12, 'digits')
key_alphanum = generator.generate_random_key(12, 'alphanumeric')
key_symbols = generator.generate_random_key(12, 'symbols')

print(f"Solo letras (a-z, A-Z):      {key_letters}")
print(f"Solo dígitos (0-9):          {key_digits}")
print(f"Alfanumérico:                {key_alphanum}")
print(f"Solo símbolos:               {key_symbols}")

print("\nLLAVES BASADAS EN TIEMPO")
print("-" * 70)

key_time_1, ts_1 = generator.generate_time_based_key(16, 'alphanumeric')
time.sleep(0.1) 
key_time_2, ts_2 = generator.generate_time_based_key(16, 'alphanumeric')

print(f"Llave tiempo 1: {key_time_1} (timestamp: {ts_1})")
print(f"Llave tiempo 2: {key_time_2} (timestamp: {ts_2})")

print("\nLLAVES CON PATRÓN PERSONALIZADO")
print("-" * 70)
print("Patrones: L=mayúscula, l=minúscula, d=dígito, s=símbolo, a=alfanum, *=cualquiera")

pattern2 = "llll-dddd-llll"  
key_pattern_2 = generator.generate_key_with_pattern(pattern2)

print(f"Patrón '{pattern2}': {key_pattern_2}")

print("\nLLAVES DE DIFERENTES LONGITUDES")
print("-" * 70)

for length in [8, 16, 32, 64]:
    key = generator.generate_random_key(length, 'alphanumeric')
    print(f"Longitud {length:2d}: {key}")
    
print("Ejemplos completados. Todas las llaves utilizan caracteres ASCII.")
print("="*70 + "\n")