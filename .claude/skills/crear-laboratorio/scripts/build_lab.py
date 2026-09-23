"""Genera el par de notebooks de un laboratorio: versión resuelta (profesor) y template (students).

Uso: escribe un archivo de especificación (p. ej. en tu scratchpad) que importe este módulo:

    import sys
    sys.path.insert(0, "<repo_profesor>/.claude/skills/crear-laboratorio/scripts")
    from build_lab import Lab, TODO, OPINA

    lab = Lab()
    lab.md("# 🚗 Laboratorio: ...")                      # igual en ambas versiones
    lab.helpers_viz()                                     # tabla + celda de helpers de visualización
    lab.helpers_modelo()                                  # tabla + celda de helpers de modelado (opcional)
    lab.datos("mpg")                                      # carga + preparación ya resuelta (sesiones 3 en adelante)
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

HELPERS_CLASIF_MD = """### 🧰 Funciones de clasificación

Ejecuta la celda una vez; después sólo llamas a la función que necesites:

| Función | ¿Para qué sirve? |
|---|---|
| `ajustar_logit(X_train, y_train)` | Ajusta una regresión logística (ya agrega la constante) |
| `predecir_proba(results, X)` | Probabilidad estimada de la clase positiva |
| `razon_de_momios(results)` | Coeficientes, razón de momios y p-value en una tabla |
| `evaluar_clasificador(nombre, y_real, y_pred)` | Exactitud, precisión, recall y F1 |
| `plot_tasa_por_categoria(df, columna, objetivo)` | Tasa de la clase positiva por categoría |
| `plot_matriz_confusion(y_real, y_pred, etiquetas)` | Matriz de confusión |
| `plot_curva_roc(y_real, y_proba)` | Curva ROC y AUC |
| `plot_metricas_por_umbral(y_real, y_proba)` | Cómo cambian las métricas al mover el umbral |
| `plot_sigmoide()` | La curva que convierte cualquier número en probabilidad |"""

HELPERS_MODELO_MD = """### 🧰 Funciones de modelado

Hacen en una línea lo que de otra forma repetirías en cada modelo:

| Función | ¿Para qué sirve? |
|---|---|
| `ajustar_ols(X_train, y_train)` | Ajusta un modelo OLS (ya agrega la constante) |
| `predecir(results, X)` | Genera predicciones con el modelo |
| `evaluar_modelo(nombre, results, X_test, y_test)` | R² y RMSE en el conjunto de prueba |
| `calcular_vif(X)` | VIF de cada variable, de mayor a menor |"""


# Preparadores de datos: en las sesiones donde el caso YA se trabajó, la preparación va dada
DATOS = {
    "mpg": ("datos_mpg.py", """### 📥 Los datos, ya preparados

Este caso lo trabajaste en la sesión de regresión lineal, así que no repetimos la exploración ni el preprocesamiento: la celda siguiente trae las dos funciones que hacen lo mismo que hiciste a mano.

| Función | ¿Qué hace? |
|---|---|
| `cargar_mpg()` | Descarga la base SQLite y elimina los nulos de `horsepower` |
| `preparar_mpg(df)` | Separa X/y, hace el split 80/20 (`random_state=42`) y codifica `origin` con los autos americanos como referencia |

Usa exactamente la **misma partición** de aquella sesión, así que las métricas son comparables."""),
    "titanic": ("datos_titanic.py", """### 📥 Los datos, ya preparados

Este caso lo trabajaste en la sesión de regresión logística, así que no repetimos la exploración ni el preprocesamiento: la celda siguiente trae las dos funciones que hacen lo mismo que hiciste a mano.

| Función | ¿Qué hace? |
|---|---|
| `cargar_titanic()` | Descarga la base SQLite con los 891 pasajeros |
| `preparar_titanic(df)` | Split estratificado 80/20, imputa `age` y `embarked` con datos de train, crea `viaja_solo` y `es_menor`, y codifica las categóricas |

Usa exactamente la **misma partición** de aquella sesión, así que las métricas son comparables."""),
}


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

    def helpers_clasificacion(self, md=HELPERS_CLASIF_MD):
        self.md(md)
        self.code(read_asset("helpers_clasificacion.py"))

    def datos(self, caso):
        """Celda dada con las funciones de carga y preparación del caso ('mpg' o 'titanic')."""
        asset, md = DATOS[caso]
        self.md(md)
        self.code(read_asset(asset))

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
