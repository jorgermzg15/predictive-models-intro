"""Resumen compacto de un notebook: una línea por celda (índice, tipo, primeras palabras, marcas).

    python3 .claude/skills/crear-laboratorio/scripts/notebook_outline.py <notebook.ipynb> [--full]

Marcas: [✍️] celda para el alumno, [ERR] tiene salida de error, [OUT] tiene salidas, [HELPERS] celda de helpers.
Con --full imprime el código completo de cada celda de código (útil para revisar un notebook sin
cargar las salidas, que suelen pesar cientos de KB por las gráficas de plotly).
"""
import json
import sys


def main():
    path = sys.argv[1]
    full = "--full" in sys.argv
    with open(path, encoding="utf-8") as f:
        nb = json.load(f)

    code_cells = sum(c["cell_type"] == "code" for c in nb["cells"])
    print(f"{path}: {len(nb['cells'])} celdas ({code_cells} de código)")
    for i, cell in enumerate(nb["cells"]):
        src = "".join(cell["source"])
        marks = []
        if "✍️" in src:
            marks.append("✍️")
        if src.startswith("# Funciones auxiliares de visualización") or src.startswith("# Funciones de modelado"):
            marks.append("HELPERS")
        outs = cell.get("outputs", [])
        if any(o.get("output_type") == "error" for o in outs):
            marks.append("ERR")
        elif outs:
            marks.append("OUT")
        first = next((l for l in src.splitlines() if l.strip()), "")[:100]
        tag = f" [{' '.join(marks)}]" if marks else ""
        kind = "md  " if cell["cell_type"] == "markdown" else "code"
        print(f"[{i:>3}] {kind}{tag} {first}")
        if full and cell["cell_type"] == "code" and "HELPERS" not in marks:
            for line in src.splitlines():
                print(f"        {line}")


if __name__ == "__main__":
    main()
