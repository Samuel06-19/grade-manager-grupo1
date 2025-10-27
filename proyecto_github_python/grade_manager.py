#!/usr/bin/env python3
"""
GradeManager - pequeña app CLI para administrar alumnos y sus notas.
Guarda los datos en un archivo JSON (data.json) en el mismo
directorio.
"""
import argparse
import json
import os
from typing import Dict, List

DATA_FILE = "data.json"


def load_data() -> Dict[str, Dict]:
    if not os.path.exists(DATA_FILE):
        return {"students": {}}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: Dict[str, Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_student(name: str) -> str:
    data = load_data()
    students = data.setdefault("students", {})
    next_id = str(max((int(i) for i in students.keys()), default=0) + 1)
    students[next_id] = {"name": name, "grades": []}
    save_data(data)
    return next_id


def add_grade(student_id: str, grade: float) -> bool:
    data = load_data()
    students = data.get("students", {})
    if student_id not in students:
        return False
    students[student_id]["grades"].append(float(grade))
    save_data(data)
    return True


def average(student_id: str) -> float:
    data = load_data()
    s = data["students"].get(student_id)
    if not s or not s["grades"]:
        return 0.0
    return sum(s["grades"]) / len(s["grades"])


def list_students() -> List[Dict]:
    data = load_data()
    return [
        {"id": sid, "name": info["name"], "grades": info["grades"]}
        for sid, info in data.get("students", {}).items()
    ]


def export_csv(path: str) -> None:
    import csv
    students = list_students()
    with open(path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "grades", "average"])
        for s in students:
            avg = sum(s["grades"]) / len(s["grades"]) if s["grades"] else 0.0
            writer.writerow([
                s['id'],
                s['name'],
                "|".join(map(str, s['grades'])),
                f"{avg:.2f}"
            ])


def parse_args():
    parser = argparse.ArgumentParser(
        prog="grade_manager",
        description="Gestor simple de notas"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add-student", help="Agregar alumno")
    p_add.add_argument("name")

    p_grade = sub.add_parser("add-grade", help="Agregar nota")
    p_grade.add_argument("student_id")
    p_grade.add_argument("grade", type=float)

    p_avg = sub.add_parser("average", help="Promedio de alumno")
    p_avg.add_argument("student_id")

    p_list = sub.add_parser("list", help="Listar alumnos")

    p_csv = sub.add_parser("export-csv", help="Exportar a CSV")
    p_csv.add_argument("path")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.cmd == "add-student":
        sid = add_student(args.name)
        print(f"Alumno creado con id {sid}")

    elif args.cmd == "add-grade":
        ok = add_grade(args.student_id, args.grade)
        print("Nota agregada" if ok else "Alumno no encontrado")

    elif args.cmd == "average":
        avg = average(args.student_id)
        print(f"Promedio: {avg:.2f}")

    elif args.cmd == "list":
        for s in list_students():
            print(f"{s['id']}: {s['name']} -> {s['grades']}")

    elif args.cmd == "export-csv":
        export_csv(args.path)
        print(f"Exportado a {args.path}")


if __name__ == "__main__":
    main()
