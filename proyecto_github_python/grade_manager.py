#!/usr/bin/env python3
&quot;&quot;&quot;
GradeManager - pequeña app CLI para administrar alumnos y sus notas.
Guarda los datos en un archivo JSON (data.json) en el mismo
directorio.
&quot;&quot;&quot;
import argparse
import json
import os
from typing import Dict, List
DATA_FILE = &quot;data.json&quot;
def load_data() -&gt; Dict[str, Dict]:
if not os.path.exists(DATA_FILE):
return {&quot;students&quot;: {}}
with open(DATA_FILE, &quot;r&quot;, encoding=&quot;utf-8&quot;) as f:
return json.load(f)
def save_data(data: Dict[str, Dict]) -&gt; None:
with open(DATA_FILE, &quot;w&quot;, encoding=&quot;utf-8&quot;) as f:
json.dump(data, f, indent=2, ensure_ascii=False)

def add_student(name: str) -&gt; str:
data = load_data()
students = data.setdefault(&quot;students&quot;, {})
next_id = str(max((int(i) for i in students.keys()), default=0) +
1)
students[next_id] = {&quot;name&quot;: name, &quot;grades&quot;: []}
save_data(data)
return next_id
def add_grade(student_id: str, grade: float) -&gt; bool:
data = load_data()
students = data.get(&quot;students&quot;, {})
if student_id not in students:
return False
students[student_id][&quot;grades&quot;].append(float(grade))
save_data(data)
return True
def average(student_id: str) -&gt; float:
data = load_data()
s = data[&quot;students&quot;].get(student_id)
if not s or not s[&quot;grades&quot;]:
return 0.0
return sum(s[&quot;grades&quot;]) / len(s[&quot;grades&quot;])
def list_students() -&gt; List[Dict]:
data = load_data()
return [{&quot;id&quot;: sid, &quot;name&quot;: info[&quot;name&quot;], &quot;grades&quot;:
info[&quot;grades&quot;]}
for sid, info in data.get(&quot;students&quot;, {}).items()]
def export_csv(path: str) -&gt; None:
import csv
students = list_students()
with open(path, &quot;w&quot;, newline=&#39;&#39;, encoding=&quot;utf-8&quot;) as f:
writer = csv.writer(f)
writer.writerow([&quot;id&quot;, &quot;name&quot;, &quot;grades&quot;, &quot;average&quot;])
for s in students:
avg = sum(s[&quot;grades&quot;]) / len(s[&quot;grades&quot;]) if s[&quot;grades&quot;]
else 0.0
writer.writerow([s[&#39;id&#39;], s[&#39;name&#39;], &quot;|&quot;.join(map(str,
s[&#39;grades&#39;])), f&quot;{avg:.2f}&quot;])
def parse_args():
parser = argparse.ArgumentParser(prog=&quot;grade_manager&quot;,
description=&quot;Gestor simple de notas&quot;)
sub = parser.add_subparsers(dest=&quot;cmd&quot;, required=True)
p_add = sub.add_parser(&quot;add-student&quot;, help=&quot;Agregar alumno&quot;)
p_add.add_argument(&quot;name&quot;)
p_grade = sub.add_parser(&quot;add-grade&quot;, help=&quot;Agregar nota&quot;)
p_grade.add_argument(&quot;student_id&quot;)
p_grade.add_argument(&quot;grade&quot;, type=float)
p_avg = sub.add_parser(&quot;average&quot;, help=&quot;Promedio de alumno&quot;)
p_avg.add_argument(&quot;student_id&quot;)
p_list = sub.add_parser(&quot;list&quot;, help=&quot;Listar alumnos&quot;)
p_csv = sub.add_parser(&quot;export-csv&quot;, help=&quot;Exportar a CSV&quot;)

p_csv.add_argument(&quot;path&quot;)
return parser.parse_args()
def main():
args = parse_args()
if args.cmd == &quot;add-student&quot;:
sid = add_student(args.name)
print(f&quot;Alumno creado con id {sid}&quot;)
elif args.cmd == &quot;add-grade&quot;:
ok = add_grade(args.student_id, args.grade)
print(&quot;Nota agregada&quot; if ok else &quot;Alumno no encontrado&quot;)
elif args.cmd == &quot;average&quot;:
avg = average(args.student_id)
print(f&quot;Promedio: {avg:.2f}&quot;)
elif args.cmd == &quot;list&quot;:
for s in list_students():
print(f&quot;{s[&#39;id&#39;]}: {s[&#39;name&#39;]} -&gt; {s[&#39;grades&#39;]}&quot;)
elif args.cmd == &quot;export-csv&quot;:
export_csv(args.path)
print(f&quot;Exportado a {args.path}&quot;)
if __name__ == &quot;__main__&quot;:
main()
