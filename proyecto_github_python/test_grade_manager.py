from grade_manager import calcular_promedio

def test_promedio_basico():
    assert calcular_promedio([10, 8, 6]) == 8

def test_lista_vacia():
    assert calcular_promedio([]) == 0
