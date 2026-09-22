"""Compara la versión del profesor con el template de students, celda por celda.

    python3 .claude/skills/sincronizar-template/scripts/compare_pair.py <ruta relativa del notebook>

La ruta es relativa a la raíz de cada repo (p. ej. 01-regresion-lineal/caso_mpg.ipynb). El repo de students
se busca en ../3 Modelos Predictivos - Students (o en --students <ruta>).

Alinea las celdas por contenido (difflib) y reporta:
  =   idéntica en ambos
  ~   par profesor/alumno (misma posición, texto distinto: normalmente solución vs pista)
  +P  sólo existe en el profesor  (¿falta en el template?)
  +S  sólo existe en students      (¿sobra o quedó vieja?)
"""
import argparse
import difflib
import json
import os

REPO_PROF = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
REPO_STU_DEFAULT = os.path.join(os.path.dirname(REPO_PROF), "3 Modelos Predictivos - Students")


def load(path):
    with open(path, encoding="utf-8") as f:
        return [(c["cell_type"], "".join(c["source"])) for c in json.load(f)["cells"]]


def first_line(src):
    return next((l for l in src.splitlines() if l.strip()), "")[:90]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook")
    parser.add_argument("--students", default=REPO_STU_DEFAULT)
    args = parser.parse_args()

    prof = load(os.path.join(REPO_PROF, args.notebook))
    stu = load(os.path.join(args.students, args.notebook))
    matcher = difflib.SequenceMatcher(a=[s for _, s in prof], b=[s for _, s in stu], autojunk=False)

    counts = {"=": 0, "~": 0, "+P": 0, "+S": 0}
    for op, a0, a1, b0, b1 in matcher.get_opcodes():
        if op == "equal":
            counts["="] += a1 - a0
            continue
        pairs = min(a1 - a0, b1 - b0) if op == "replace" else 0
        for k in range(pairs):
            counts["~"] += 1
            print(f"~  P[{a0 + k}] {prof[a0 + k][0]:4} {first_line(prof[a0 + k][1])}")
            print(f"   S[{b0 + k}] {stu[b0 + k][0]:4} {first_line(stu[b0 + k][1])}")
        for i in range(a0 + pairs, a1):
            counts["+P"] += 1
            print(f"+P P[{i}] {prof[i][0]:4} {first_line(prof[i][1])}")
        for j in range(b0 + pairs, b1):
            counts["+S"] += 1
            print(f"+S S[{j}] {stu[j][0]:4} {first_line(stu[j][1])}")

    print(f"\nprofesor: {len(prof)} celdas | students: {len(stu)} celdas | "
          f"idénticas: {counts['=']} | pares distintos: {counts['~']} | "
          f"sólo profesor: {counts['+P']} | sólo students: {counts['+S']}")


if __name__ == "__main__":
    main()
