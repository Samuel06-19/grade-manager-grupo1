def calcular_promedio(notas):
    if not notas:
        return 0
    return sum(notas) / len(notas)

if __name__ == "__main__":
    print("Bienvenido al gestor de notas.")
    notas = []

    for i in range(3):
        nota = float(input(f"Ingrese la nota {i+1}: "))
        notas.append(nota)

    promedio = calcular_promedio(notas)
    print(f"El promedio de las notas es: {promedio:.2f}")
