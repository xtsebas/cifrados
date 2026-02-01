import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def analisis_frecuencia(mensaje, titulo="ANÁLISIS DE FRECUENCIAS"):
    if not mensaje:
        print("No hay caracteres para analizar")
        return {}
    
    frecuencias = {}
    for char in mensaje:
        if char in frecuencias:
            frecuencias[char] = frecuencias[char] + 1
        else:
            frecuencias[char] = 1
    
    total_chars = len(mensaje)
    frecuencias_con_porcentaje = {}
    
    for char, cantidad in frecuencias.items():
        porcentaje = (cantidad * 100) / total_chars
        frecuencias_con_porcentaje[char] = (cantidad, porcentaje)
    
    mostrar_tabla_frecuencias(frecuencias_con_porcentaje, titulo)
    return frecuencias_con_porcentaje


def ordenar_frecuencias_descendente(frecuencias):
    if not frecuencias:
        return []
    
    lista_frecuencias = []
    for char, (cantidad, porcentaje) in frecuencias.items():
        lista_frecuencias.append((char, cantidad, porcentaje))
    
    n = len(lista_frecuencias)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista_frecuencias[j][1] < lista_frecuencias[j + 1][1]:
                temp = lista_frecuencias[j]
                lista_frecuencias[j] = lista_frecuencias[j + 1]
                lista_frecuencias[j + 1] = temp
    
    return lista_frecuencias


def mostrar_tabla_frecuencias(frecuencias, titulo="ANÁLISIS DE FRECUENCIAS"):
    if not frecuencias:
        print("No hay caracteres para analizar")
        return
    
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)
    print(f"{'Carácter':<15} {'Cantidad':<15} {'Porcentaje':<15} {'Barra':<25}")
    print("-" * 70)
    
    frecuencias_ordenadas = ordenar_frecuencias_descendente(frecuencias)
    
    for char, cantidad, porcentaje in frecuencias_ordenadas:
        if char == ' ':
            char_repr = '[ESPACIO]'
        elif char == '\n':
            char_repr = '[SALTO]'
        elif char == '\t':
            char_repr = '[TAB]'
        else:
            char_repr = f"'{char}'"
        
        barra_longitud = int(porcentaje / 2)  
        barra = '#' * barra_longitud
        
        print(f"{char_repr:<15} {cantidad:<15} {porcentaje:>6.2f}%      {barra:<25}")
    
    print("=" * 70 + "\n")