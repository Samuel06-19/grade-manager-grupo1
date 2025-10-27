import os

# Crear carpeta "tests" si no existe
os.makedirs("tests", exist_ok=True)

# Crear los archivos
files = [
    "grade_manager.py",
    "requirements.txt",
    "README.md",
    ".gitignore",
    "tests/test_grade_manager.py"
]

for file in files:
    # Crear el archivo si no existe
    with open(file, "a") as f:
        pass

print("✅ Archivos y carpetas creados correctamente.")

