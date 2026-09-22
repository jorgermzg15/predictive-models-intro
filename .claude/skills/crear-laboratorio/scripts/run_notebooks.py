"""Ejecuta notebooks con el kernel del proyecto y reporta errores y salidas a stderr.

Ejecutar desde la raíz del repo, con el entorno del proyecto:

    uv run --with nbclient python .claude/skills/crear-laboratorio/scripts/run_notebooks.py <notebook o carpeta> [...] [--save]

--save   guarda las salidas en el notebook (úsalo sólo con versiones del profesor y sólo si no hubo errores).

Cada notebook se ejecuta con su propia carpeta como directorio de trabajo (así las bases .db se descargan
junto al notebook, como cuando lo abre el alumno).
"""
import argparse
import glob
import os
import sys

import nbformat
from nbclient import NotebookClient


def find_notebooks(targets):
    for target in targets:
        if os.path.isdir(target):
            for path in sorted(glob.glob(os.path.join(target, "**", "*.ipynb"), recursive=True)):
                if ".venv" not in path and ".ipynb_checkpoints" not in path:
                    yield path
        else:
            yield target


def run(path, save):
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(
        nb, timeout=900, kernel_name="python3", allow_errors=True,
        resources={"metadata": {"path": os.path.dirname(os.path.abspath(path))}},
    )
    client.execute()

    errors, stderr = [], []
    for i, cell in enumerate(nb.cells):
        for out in cell.get("outputs", []):
            if out.get("output_type") == "error":
                errors.append((i, out["ename"], out["evalue"].splitlines()[0][:200] if out["evalue"] else ""))
            elif out.get("name") == "stderr":
                stderr.append((i, out["text"].strip().splitlines()[-1][:200]))

    print(f"== {path}: {len(errors)} errores, {len(stderr)} celdas con stderr")
    for i, name, msg in errors:
        print(f"   ERROR celda {i}: {name}: {msg}")
    for i, msg in stderr:
        print(f"   stderr celda {i}: {msg}")

    if save:
        if errors:
            print("   (no se guardó: hay errores)")
        else:
            nbformat.write(nb, path)
            print("   salidas guardadas")
    return not errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("targets", nargs="+")
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    ok = all([run(p, args.save) for p in find_notebooks(args.targets)])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
