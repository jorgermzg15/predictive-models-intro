"""Genera el par de notebooks de un laboratorio: versión resuelta (profesor) y template (students).

Uso: escribe un archivo de especificación (p. ej. en tu scratchpad) que importe este módulo:

    import sys
    sys.path.insert(0, "<repo_profesor>/.claude/skills/crear-laboratorio/scripts")
    from build_lab import Lab, TODO, OPINA

    lab = Lab()
    lab.md("# 🚗 Laboratorio: ...")                      # igual en ambas versiones
    lab.helpers_viz()                                     # tabla + celda de helpers de visualización
    lab.helpers_modelo()                                  # tabla + celda de helpers de modelado (opcional)
    lab.code("df.describe()",                             # profesor
             "# Pista: df.describe()\\n" + TODO)          # students
    lab.md("✅ **Qué observar:** ...",
           "✍️ ¿Qué observas?\\n\\n" + OPINA)
    lab.build("<repo_profesor>/caso/notebook.ipynb",
              "<repo_students>/caso/notebook.ipynb")

Cada celda recibe el texto del profesor y, opcionalmente, el de students. Si no se pasa el de students,
la celda es idéntica en ambas versiones. Los notebooks se escriben sin salidas: ejecuta después la versión
del profesor con `run_notebooks.py --save`.
"""
import json
import os
import uuid

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

TODO = "# ✍️ Tu código aquí\n"
OPINA = "RELLENAR CON TUS COMENTARIOS"
REGALO = "# Esta celda va de regalo: léela con calma y ejecútala\n"

HELPERS_VIZ_MD = """## 🛠️ Funciones auxiliares de visualización

Ejecuta la siguiente celda **una sola vez** al inicio. Después sólo tienes que **llamar** a la función que necesites:

| Función | ¿Para qué sirve? |
|---|---|
| `plot_distributions(df, columnas)` | Histograma + boxplot de variables numéricas |
| `plot_frequencies(df, columnas, top_n=None)` | Frecuencia de variables categóricas |
| `plot_correlation_matrix(df, columnas)` | Matriz de correlación |
| `plot_pairplot(df, columnas, color=None)` | Dispersión entre todas las variables numéricas |
| `plot_simple_regression(x, y, results)` | Recta ajustada de un modelo OLS con 1 variable |
| `plot_actual_vs_predicted(y_real, y_pred)` | Valores reales vs predichos |
| `plot_residuals(y_real, y_pred)` | Residuales vs predichos |
| `plot_rfecv(rfecv)` | R² según el número de variables seleccionadas por RFECV |"""

HELPERS_MODELO_MD = """### 🧰 Funciones de modelado

Hacen en una línea lo que de otra forma repetirías en cada modelo:

| Función | ¿Para qué sirve? |
|---|---|
| `ajustar_ols(X_train, y_train)` | Ajusta un modelo OLS (ya agrega la constante) |
| `predecir(results, X)` | Genera predicciones con el modelo |
| `evaluar_modelo(nombre, results, X_test, y_test)` | R² y RMSE en el conjunto de prueba |
| `calcular_vif(X)` | VIF de cada variable, de mayor a menor |"""


def read_asset(name):
    with open(os.path.join(ASSETS, name), encoding="utf-8") as f:
        return f.read().rstrip("\n")


def _lines(s):
    parts = s.split("\n")
    return [p + "\n" for p in parts[:-1]] + ([parts[-1]] if parts[-1] else [])


def _cell(kind, src):
    cid = uuid.uuid4().hex[:8]
    if kind == "md":
        return {"cell_type": "markdown", "id": cid, "metadata": {}, "source": _lines(src)}
    return {"cell_type": "code", "execution_count": None, "id": cid,
            "metadata": {}, "outputs": [], "source": _lines(src)}


class Lab:
    def __init__(self, python_version="3.14.7"):
        self.cells = []
        self.python_version = python_version

    def md(self, prof, student=None):
        self.cells.append(("md", prof, student))

    def code(self, prof, student=None):
        self.cells.append(("code", prof, student))

    def regalo(self, src):
        """Celda de código técnico: resuelta para el profesor, dada (con aviso) al alumno."""
        self.cells.append(("code", src, REGALO + src))

    def helpers_viz(self, md=HELPERS_VIZ_MD):
        self.md(md)
        self.code(read_asset("helpers_viz.py"))

    def helpers_modelo(self, md=HELPERS_MODELO_MD):
        self.md(md)
        self.code(read_asset("helpers_modelo.py"))

    def _notebook(self, student):
        cells = [_cell(kind, student_src if (student and student_src is not None) else prof_src)
                 for kind, prof_src, student_src in self.cells]
        return {
            "cells": cells,
            "metadata": {
                "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "language_info": {"name": "python", "version": self.python_version},
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }

    def build(self, prof_path, student_path=None):
        targets = [(prof_path, False)] + ([(student_path, True)] if student_path else [])
        for path, student in targets:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(json.dumps(self._notebook(student), indent=1, ensure_ascii=False) + "\n")
            print(f"escrito: {path} ({len(self.cells)} celdas)")
