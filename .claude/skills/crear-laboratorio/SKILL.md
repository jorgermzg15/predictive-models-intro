---
name: crear-laboratorio
description: Crea un laboratorio de clase de data analytics / machine learning como par de notebooks Jupyter, la versión resuelta del profesor (ejecutada, con salidas) y el template hands-on para alumnos (con celdas ✍️ y pistas), a partir de un dataset y un tema (regresión, KNN, árboles de decisión, clasificación, VIF, RFECV, etc.). Úsala siempre que el profesor pida preparar, armar o diseñar un caso, laboratorio, práctica, sesión o notebook nuevo para su curso de Modelos Predictivos, o convertir un notebook resuelto en template para alumnos, aunque no diga "laboratorio".
---

# Crear laboratorio

Genera, desde **una sola definición**, la versión resuelta (repo del profesor) y el template (repo de students) de un laboratorio de 3 horas para alumnos novatos. Así ambas versiones tienen exactamente la misma estructura y el profesor proyecta el mismo archivo que el alumno tiene abierto.

Antes de empezar, lee `references/convenciones.md`: ahí están los repos, el público, la estructura de un laboratorio, las reglas del template y los errores técnicos que no deben repetirse. El laboratorio de referencia es `mpg_case/regression_on_mpg.ipynb`; úsalo como modelo de tono y de estructura (con `scripts/notebook_outline.py <ruta> --full` lo recorres sin cargar las salidas).

## Flujo

### 1. Entender el encargo
Aclara con el profesor, si no es evidente:
- **Tema y técnica** (p. ej. KNN de clasificación con titanic) y **qué debe aprender el alumno** al final.
- **Dataset**: preferir el repo SQLite ya usado en el curso (`mpg`, `diamonds`, `titanic`, `tips`, `iris`, …) o `sklearn.datasets`. Si propones otro, explica por qué.
- **Duración** (por defecto 3 horas con descanso) y si reemplaza o complementa un caso existente.
- **Ruta**: `<caso>_case/<nombre>.ipynb`, la misma en ambos repos.

### 2. Explorar los datos y fijar los números **antes** de escribir
La historia depende de resultados reales. Con `uv run python -` (entorno del proyecto) calcula todo lo que el laboratorio va a mostrar: nulos, correlaciones, métricas de cada modelo en test, coeficientes, VIF por paso, resultados de selección de variables. Usa `random_state=42`.

Busca en esos números los momentos didácticos:
- Un resultado que **no cuadra** (signo contraintuitivo, p-value alto, sobreajuste) que motive la siguiente técnica.
- Un resultado que **contradiga la receta automática** (p. ej. quitar la variable de mayor VIF empeora el modelo).
- **Dos caminos que convergen** (selección manual y automática eligen lo mismo).
- El modelo **más simple** que rinde igual que el complejo.

Si los números no cuentan una buena historia, ajusta el diseño (otra variable objetivo, otro dataset, otro orden) antes de escribir.

### 3. Diseñar el guion
Propón al profesor la estructura (partes, minutos, qué descubre el alumno en cada una) en una tabla breve y ajústala con él si hay dudas importantes. La estructura estándar está en la sección 4 de `convenciones.md`.

Decide qué celdas son:
- **Objetivo de aprendizaje** → el alumno las escribe (template con pasos numerados y pistas).
- **Técnicas pero no el objetivo** (encoding, configuración de un algoritmo, joins) → `lab.regalo(...)`.
- **Repetitivas** → usa los helpers (`evaluar_modelo`, `ajustar_ols`, …). Si una técnica nueva se repite mucho (p. ej. evaluar un clasificador), agrega un helper nuevo al notebook en una celda "Funciones del caso"; si servirá en varios laboratorios, agrégalo a `assets/` y sincroniza con la skill `sincronizar-template`.

### 4. Escribir la especificación
Escribe un archivo de especificación en tu scratchpad (no en el repo) usando `scripts/build_lab.py`; su docstring explica la API (`lab.md`, `lab.code`, `lab.regalo`, `lab.helpers_viz`, `lab.helpers_modelo`, `lab.build`). Cada celda recibe el texto del profesor y, si difiere, el del alumno.

Al escribir:
- Cita en markdown los **números reales** del paso 2 (redondeados como los mostrará la salida).
- En el template, las pistas dicen **qué hacer y qué función usar**, nunca el resultado ni cuál variable eliminar.
- Cada `✅ Qué observar` del profesor tiene su versión `✍️` con preguntas para el alumno.
- Un nombre por modelo y listas de columnas; nada de reasignar `X_train_enc` (ver sección 6 de `convenciones.md`).

Ejecuta la especificación para generar ambos notebooks. **No importes** otro archivo de especificación desde uno nuevo: al importarlo se ejecuta su `build()` y sobrescribe notebooks existentes.

### 5. Verificar
Desde la raíz del repo del profesor:
```bash
uv run --with nbclient python .claude/skills/crear-laboratorio/scripts/run_notebooks.py <caso>_case/<nombre>.ipynb --save
```
- La versión del profesor debe correr **sin errores**; se guarda ejecutada.
- Compara **cada número citado en markdown** contra las salidas guardadas. Si alguno no coincide, corrige la especificación y vuelve a generar.
- En el repo de students, ejecuta el template **sin** `--save`: sólo deben fallar celdas que dependen de celdas ✍️ (`NameError`). Un error en otra celda es un bug.
- Si agregaste dependencias: `pyproject.toml` en ambos repos, `uv lock`, `uv sync --frozen`.

### 6. Integrar y reportar
- Actualiza la sección de estructura del README en **ambos** repos.
- Resume al profesor: la historia en 3-4 líneas, la tabla de la agenda, los números clave y qué quedó como ✍️ para el alumno.
- Haz commit/push sólo si el profesor lo pide (un commit por repo).
