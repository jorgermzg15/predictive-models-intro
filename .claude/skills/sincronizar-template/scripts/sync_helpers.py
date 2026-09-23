"""Reemplaza las celdas de helpers en todos los notebooks de ambos repos con la versión de assets/.

    python3 .claude/skills/sincronizar-template/scripts/sync_helpers.py [--dry-run]

Busca celdas de código que empiecen con:
  "# Funciones auxiliares de visualización"  -> crear-laboratorio/assets/helpers_viz.py
  "# Funciones de modelado"                   -> crear-laboratorio/assets/helpers_modelo.py
y reemplaza su código (conserva salidas y demás celdas). Los helpers específicos de un caso
(p. ej. "# Funciones del caso" del caso California) no se tocan.

Flujo para cambiar un helper: edita el archivo en assets/, corre este script, re-ejecuta las versiones
del profesor con run_notebooks.py --save.
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_PROF = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
REPO_STU = os.path.join(os.path.dirname(REPO_PROF), "3 Modelos Predictivos - Students")
ASSETS = os.path.join(REPO_PROF, ".claude", "skills", "crear-laboratorio", "assets")

HELPERS = {
    "# Funciones auxiliares de visualización": "helpers_viz.py",
    "# Funciones de modelado": "helpers_modelo.py",
    "# Funciones de clasificación": "helpers_clasificacion.py",
    "# Datos del caso MPG": "datos_mpg.py",
    "# Datos del caso Titanic": "datos_titanic.py",
}


def lines(s):
    parts = s.split("\n")
    return [p + "\n" for p in parts[:-1]] + ([parts[-1]] if parts[-1] else [])


def main():
    dry = "--dry-run" in sys.argv
    sources = {}
    for prefix, name in HELPERS.items():
        with open(os.path.join(ASSETS, name), encoding="utf-8") as f:
            sources[prefix] = f.read().rstrip("\n")

    for repo in (REPO_PROF, REPO_STU):
        for path in sorted(glob.glob(os.path.join(repo, "**", "*.ipynb"), recursive=True)):
            if ".venv" in path or ".ipynb_checkpoints" in path:
                continue
            with open(path, encoding="utf-8") as f:
                raw = f.read()
            nb = json.loads(raw)
            changed = []
            for i, cell in enumerate(nb["cells"]):
                src = "".join(cell["source"])
                for prefix, new in sources.items():
                    if cell["cell_type"] == "code" and src.startswith(prefix) and src != new:
                        cell["source"] = lines(new)
                        changed.append(i)
            if changed:
                rel = os.path.relpath(path, os.path.dirname(REPO_PROF))
                print(f"{'(dry-run) ' if dry else ''}actualizado {rel}: celdas {changed}")
                if not dry:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
    print("listo")


if __name__ == "__main__":
    main()
