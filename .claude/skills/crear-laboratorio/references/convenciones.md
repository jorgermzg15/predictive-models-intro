# Convenciones del curso de Modelos Predictivos

Referencia compartida por las skills `crear-laboratorio`, `sincronizar-template`, `auditar-curso` y `revisar-notebook-novatos`.

## Contenido
1. Los dos repos
2. Público y formato de las sesiones
3. Entorno (idéntico en local y Codespaces)
4. Estructura de un laboratorio
5. Versión resuelta vs template de alumnos
6. Buenas prácticas técnicas que el material debe respetar
7. Estilo de escritura
8. Git

---

## 1. Los dos repos

| Repo | Ruta local | Remoto | Para quién |
|---|---|---|---|
| Profesor | `3 Modelos Predictivos/` (este repo) | `jorgermzg15/predictive-models-intro` | Versiones **resueltas** y con salidas guardadas |
| Students | `../3 Modelos Predictivos - Students/` (hermano de este repo) | `jorgermzg15/modelos-predictivos-students` | **Templates** que los alumnos llenan en clase (hands-on lab) |

- Los notebooks compartidos viven en la **misma ruta relativa** en ambos repos (p. ej. `01-regresion-lineal/caso_mpg.ipynb`). Así el profesor proyecta el mismo archivo que el alumno tiene abierto.
- En el repo de students sólo existe lo que se trabaja con alumnos. Material exclusivo del profesor (p. ej. `Intro a Regresion Logistica.ipynb`) no se copia.
- **Una carpeta por sesión**, con prefijo numérico: `01-regresion-lineal/`, y las siguientes (`02-`, `03-`, `04-`) conforme se construyan. Dentro de cada una: `fundamentos.ipynb` (teoría), `caso_<dataset>.ipynb` (laboratorio) y `slides/` si aplica.
- `extra/` guarda casos de respaldo y material que no se usa en clase: `extra/diamonds/`, `extra/california/` y, sólo en el repo del profesor, `extra/clasificacion/`.
- Nombres de archivo en español y sin mayúsculas ni espacios.

## 2. Público y formato de las sesiones

- Alumnos **novatos**: nuevos en data science y con poca experiencia en Python.
- Sesiones de **3 horas**, en formato de **laboratorio intensivo**, con descanso de 10 min a la mitad.
- Plan del curso: **4 sesiones (12 h)** para cubrir **Regresión lineal, KNN y Árboles de decisión**, tanto de regresión como de clasificación.
- Lo que importa: **contar bien la historia** del caso. Cada parte responde un pedazo de una pregunta de negocio.

## 3. Entorno

- Python exacto en `.python-version` (hoy 3.14.7); dependencias en `pyproject.toml` y versiones exactas en `uv.lock`. Ambos repos resuelven las mismas versiones para los paquetes que comparten.
- Local y Codespaces se crean con el mismo comando: `uv sync --frozen`. El devcontainer (`.devcontainer/`) usa `mcr.microsoft.com/devcontainers/base:<tag>-trixie` + `uv` copiado de `ghcr.io/astral-sh/uv:<versión>`; `postCreateCommand` = `uv sync --frozen`.
- `pyproject.toml` fija `python-preference = "only-managed"` para que uv use siempre su propio Python (misma build en Mac y Linux).
- Kernel en VS Code: el `.venv` del proyecto (aparece como `predictive-models-intro (3.14.7)` en el repo del profesor y `modelos-predictivos-students (3.14.7)` en el de students). No usar kernels de Anaconda.
- Las bases SQLite se descargan en cada ejecución y están en `.gitignore` (`*.db`).
- Para agregar un paquete: agregarlo a `pyproject.toml` **en ambos repos** si ambos lo usan, `uv lock`, `uv sync --frozen`, y verificar que las versiones compartidas coincidan entre los dos `uv.lock`.

## 4. Estructura de un laboratorio

Referencia viva: `01-regresion-lineal/caso_mpg.ipynb` (laboratorio de 3 h). Úsalo como modelo cuando dudes.

1. **Portada** (markdown):
   - `📖 La historia`: contexto real del dataset que dé sentido a los datos (p. ej. la crisis del petróleo para MPG)
   - `❓` **Una pregunta de negocio** que el laboratorio responde al final
   - `🧭 Lo que vas a aprender` (4-5 objetivos)
   - `⏱️ Agenda (3 horas)`: tabla Parte / Tema / Tiempo, con descanso ☕ a la mitad y tiempos que sumen 180 min
   - `📋 Las variables`: tabla con unidades; la variable objetivo marcada con 🎯
2. **Parte 0 — Preparación** (dada, "ejecuta una sola vez"):
   - Markdown con la tabla de funciones de visualización + celda de helpers de visualización (`assets/helpers_viz.py`, **idéntica en todos los notebooks**)
   - Si el caso modela: tabla + celda de helpers de modelado (`assets/helpers_modelo.py`)
   - Carga de datos **completa** (incluida la consulta SQL): los alumnos no escriben la extracción
3. **Partes numeradas** (`---` + `# 1️⃣ Título (N min)`). Cada parte sigue el patrón:
   - Markdown: **qué haremos y por qué**, en palabras simples
   - Código
   - Markdown `✅ **Qué observar:**` con los hallazgos **con números reales** de la ejecución
4. **Cierre**: tabla comparativa de modelos (`pd.DataFrame(comparacion)`), gráfica del modelo final, `❓ Respuesta a la pregunta`, `📝 Lo que aprendimos`, `🚀 Retos opcionales`.

Principios de la historia:
- Construir **tensión**: un resultado que "no cuadra" (signo raro, p-value alto) motiva la siguiente técnica.
- Mostrar cuando dos caminos llegan a la misma conclusión (p. ej. VIF manual y RFE eligen las mismas variables).
- Preferir el modelo más simple con desempeño similar (parsimonia) y decirlo explícitamente.
- Interpretar coeficientes **en palabras y en unidades útiles** ("+1,000 lb = -7.9 mpg"), siempre "manteniendo lo demás constante" en regresión múltiple.

## 5. Versión resuelta vs template de alumnos

Se generan juntas desde una sola definición (`scripts/build_lab.py`), para que la estructura sea idéntica.

| Tipo de celda | Profesor | Students |
|---|---|---|
| Portada, explicaciones "qué haremos y por qué" | igual | igual |
| Helpers, carga de datos | igual | igual |
| Código técnico que no es objetivo de la clase (encoding, configuración de RFECV, etc.) | resuelto | igual, con comentario `# Esta celda va de regalo: léela con calma y ejecútala` |
| Código que **sí** es objetivo de aprendizaje | resuelto | comentarios con pasos numerados + pistas con la función a llamar + `# ✍️ Tu código aquí` |
| `✅ Qué observar` | hallazgos con números | preguntas `✍️` + `RELLENAR CON TUS COMENTARIOS` |
| Tabla "Cómo leer" con valores | con valores | sin valores, pidiendo al alumno anotarlos |

Reglas del template:
- **Nunca** filtrar la solución: nada de números de resultados, nombres de la variable a eliminar, etc. Las pistas dicen **qué función usar**, no el resultado.
- Los pasos a llenar deben tener **dificultad pareja**: ninguna celda debe pedir todo un flujo de golpe.
- El template se guarda **sin salidas**; la versión del profesor se guarda **ejecutada** (salidas visibles al abrirla).
- Es normal que el template, ejecutado sin llenar, lance `NameError` en celdas "de regalo" que dependen de celdas ✍️. Lo que **no** es normal es un error en una celda que no depende del alumno.

## 6. Buenas prácticas técnicas que el material debe respetar

Errores que ya aparecieron en el curso y no deben repetirse:
- **Trampa de las variables dummy**: con constante en el modelo, usar `OneHotEncoder(drop=[...])` eligiendo una categoría de referencia **interpretable** (p. ej. `drop=['usa']`) y explicarla.
- `fit` / `fit_transform` sólo en **train**; en test sólo `transform`.
- **Escalar antes de RFE/RFECV** (rankean por tamaño de coeficiente). Ajustar el modelo final sin escalar para interpretar en unidades originales.
- **No sobrescribir variables**: un nombre por modelo (`modelo_simple`, `modelo_multiple`, `modelo_vif`…) y listas de columnas (`cols_vif = cols_vif.drop(...)`) en vez de reasignar `X_train_enc`. Ejecutar fuera de orden no debe cambiar resultados.
- VIF: quitar **una variable a la vez** y recalcular; umbral 5 (tabla < 5 / 5–10 / > 10). Explicar que un VIF alto indica redundancia, no inutilidad.
- pandas 3: nada de `df['col'].fillna(..., inplace=True)` (Copy-on-Write); usar `df['col'] = df['col'].fillna(...)`. Texto es dtype `str`: `select_dtypes(include=['object', 'str'])`.
- Plotly 7: no existe `ff.create_annotated_heatmap`; usar `plot_correlation_matrix` (internamente `px.imshow(text_auto=True)`).
- Los números citados en markdown deben coincidir con las salidas de la versión ejecutada (semillas fijas: `random_state=42`).
- Datasets: evitar Boston Housing (retirado de scikit-learn por una variable con sesgo racial). Fuentes usadas: repo SQLite de David James Knight (`mpg`, `diamonds`, `titanic`, `tips`, `iris`, …) y `sklearn.datasets` (`fetch_california_housing`).

## 7. Estilo de escritura

- Español, tuteando al alumno, frases cortas.
- Títulos de parte con emoji numérico (`1️⃣`…`🔟`) y minutos. Marcadores: `✅` qué observar, `⚠️` cuidado, `💡` lección, `🤔`/`🚩` algo no cuadra, `✍️` acción del alumno, `🎯` objetivo.
- Explicar la intuición antes que la fórmula (p. ej. train/test = "estudiar con unos ejercicios y hacer el examen con otros").
- Código: el estilo de los notebooks existentes (argumentos en líneas separadas en llamadas largas, comentarios breves en español).

## 8. Git

- Hacer commit/push sólo cuando el profesor lo pida. Commits separados por repo, con mensajes tipo `feat(mpg): ...`, `fix(diamonds): ...`.
- Antes de reemplazar o borrar un notebook, comparar sus **fuentes** contra `HEAD`: VS Code suele dejar cambios sólo de salidas o metadata; los cambios de código del profesor nunca se descartan sin preguntar.
