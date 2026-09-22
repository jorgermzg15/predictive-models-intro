---
name: auditar-curso
description: Audita los repos del curso de Modelos Predictivos (profesor "3 Modelos Predictivos" y alumnos "3 Modelos Predictivos - Students") - que el entorno local sea idéntico al de GitHub Codespaces (Python, uv.lock, devcontainer), que las dependencias estén en sus versiones más recientes compatibles, que todos los notebooks corran sin errores, que no haya errores conceptuales ni desalineación entre versión resuelta y template, y que los README estén al día. Úsala antes de una sesión de clase, al actualizar dependencias o Python, cuando algo "no corre" en Codespaces, o cuando el profesor pida revisar, auditar, verificar o poner al día los repos.
---

# Auditar curso

Revisa ambos repos y reporta hallazgos priorizados. Lee primero `.claude/skills/crear-laboratorio/references/convenciones.md`: ahí están las rutas de los repos, cómo se construye el entorno y los errores técnicos conocidos.

Audita **primero el repo del profesor** y luego aplica lo mismo al de students. Pregunta antes de hacer cambios grandes (subir la versión de Python, borrar archivos), y haz commit/push sólo si el profesor lo pide.

## 1. Estado de git
- `git status` en ambos repos. Los archivos **sin versionar no existen en Codespaces**: si un notebook los necesita, o si son material nuevo, repórtalo.
- Notebooks modificados: distingue cambios de **código** vs sólo salidas/metadata (compara `source` contra `HEAD`).

## 2. Versiones
- Última versión estable de Python: `curl -s https://endoflife.date/api/python.json`. Últimas versiones de los paquetes: `https://pypi.org/pypi/<paquete>/json`. Confirma que haya wheels para esa versión de Python antes de proponer el cambio.
- Actualizar: cambia `.python-version` y `requires-python` (si aplica) y los mínimos de `pyproject.toml` en **ambos** repos; luego `uv lock --upgrade` y `uv sync --frozen` en cada uno.
- Los paquetes compartidos deben resolver a la **misma versión** en ambos `uv.lock` (compáralos con `tomllib`).
- Si hay un major bump (pandas, plotly, scikit-learn, numpy), lee sus notas de cambios y busca en los notebooks las APIs afectadas.

## 3. Paridad local ↔ Codespaces
```bash
bash .claude/skills/auditar-curso/scripts/env_parity.sh "<repo>" "<scratchpad>" --run-notebooks
```
Requiere Docker Desktop corriendo (`open -a Docker`) y ejecutarse **con el sandbox deshabilitado** (dentro del sandbox las descargas de imágenes se cuelgan). La salida esperada es la misma versión de Python (sólo cambia la fecha de compilación) y el mismo freeze, salvo paquetes exclusivos de macOS como `appnope`. Revisa también que la versión de uv del Dockerfile coincida con la local (`uv --version`) y que la etiqueta de la imagen base exista.

## 4. Notebooks
```bash
uv run --with nbclient python .claude/skills/crear-laboratorio/scripts/run_notebooks.py .
```
- **Versiones del profesor**: 0 errores. `stderr` sólo si es un aviso esperado y explicado en el notebook.
- **Templates**: sólo `NameError` en celdas que dependen de celdas ✍️.
- Si el kernel no es el del proyecto (p. ej. aparece `/opt/anaconda3` en un traceback), revisa si es una salida vieja guardada; las celdas vacías conservan salidas antiguas.

Para cada error, identifica la causa: API que cambió de versión, bug previo del notebook o dato externo que ya no existe.

## 5. Revisión conceptual
Recorre los notebooks con `notebook_outline.py --full` y busca los errores de la sección 6 de `convenciones.md`: trampa de dummies, `fit` en test, RFE sin escalar, variables sobrescritas, `inplace=True` con pandas 3, números en markdown que no coinciden con las salidas, órdenes de categorías incorrectos.

Para cada par profesor/students, corre `.claude/skills/sincronizar-template/scripts/compare_pair.py <ruta>` y verifica que los helpers sean idénticos (`sync_helpers.py --dry-run` no debe reportar cambios).

## 6. Documentación
READMEs de ambos repos: estructura de archivos real, instrucciones de entorno (uv, Codespaces, kernel), URL de clonado correcta en cada repo.

## Reporte
Presenta los hallazgos en tablas cortas, **priorizados**:
1. 🔴 Impide dar la clase (no corre en Codespaces, notebook con errores, archivo sin versionar que se necesita)
2. 🟠 Errores conceptuales que enseñan algo incorrecto
3. 🟡 Desalineación, dependencias atrasadas, documentación

Para cada uno: dónde está, qué pasa y qué propones. Luego aplica las correcciones acordadas: primero el repo del profesor, después el de students.
