---
name: sincronizar-template
description: Propaga cambios entre la versión resuelta del profesor y el template de alumnos de un notebook del curso (repos "3 Modelos Predictivos" y "3 Regresión Lineal - Students"), sin filtrar soluciones, y mantiene idénticas las funciones auxiliares (helpers) en todos los notebooks. Úsala cuando el profesor modifique un notebook resuelto y quiera reflejarlo en el de alumnos, cuando cambie o agregue un helper de visualización o modelado, cuando pregunte si ambas versiones están alineadas, o cuando pida "pasar", "copiar" o "aplicar" un cambio "al de students/alumnos".
---

# Sincronizar template

El repo del profesor tiene los notebooks **resueltos**; el de students, los **templates** en la misma ruta relativa. Cuando uno cambia, el otro debe reflejarlo **sin revelar soluciones**. Las reglas de qué es igual y qué difiere entre versiones están en la sección 5 de `.claude/skills/crear-laboratorio/references/convenciones.md`; léela antes de editar.

## Caso A: cambiaron los helpers

Los helpers de visualización y modelado deben ser **idénticos** en todos los notebooks. La fuente de verdad es `.claude/skills/crear-laboratorio/assets/` (`helpers_viz.py`, `helpers_modelo.py`).

1. Edita el asset (si el profesor editó el helper dentro de un notebook, copia primero ese código al asset).
2. Si agregaste o renombraste una función, actualiza también su tabla en `HELPERS_VIZ_MD` / `HELPERS_MODELO_MD` de `crear-laboratorio/scripts/build_lab.py` y en la celda markdown que precede a los helpers en cada notebook.
3. Propaga: `python3 .claude/skills/sincronizar-template/scripts/sync_helpers.py --dry-run`, revisa, y ejecútalo sin `--dry-run`.
4. Re-ejecuta y guarda las versiones del profesor afectadas (`run_notebooks.py --save`) y ejecuta los templates sin guardar.

Los helpers específicos de un caso (celdas "# Funciones del caso") no se sincronizan: viven sólo en ese notebook.

## Caso B: cambió un notebook

1. **Detecta qué cambió.** Si el cambio ya está en git: `git diff` (en notebooks, fíjate en `source`; ignora salidas y metadata). Para ver la alineación entre versiones:
   ```bash
   python3 .claude/skills/sincronizar-template/scripts/compare_pair.py <ruta/relativa.ipynb>
   ```
   `=` celdas idénticas, `~` pares solución/pista, `+P` sólo en profesor, `+S` sólo en students.
2. **Clasifica cada cambio** y aplícalo en la otra versión:

   | Cambio en la versión del profesor | Qué hacer en el template |
   |---|---|
   | Markdown explicativo, portada, agenda | Copiar igual |
   | Celda dada (helpers, carga de datos, "de regalo") | Copiar igual |
   | Código que el alumno escribe | Actualizar los **pasos y pistas** para que lleven a la nueva solución; no copiar el código |
   | `✅ Qué observar` con números | Revisar si las preguntas `✍️` siguen teniendo sentido; nunca copiar los números |
   | Celda nueva | Insertarla en la misma posición relativa, como dada o como ✍️ según la sección 5 de convenciones |

   Si el cambio fue en el template (p. ej. el profesor mejoró una pista), refleja en la versión resuelta sólo lo que corresponda (texto compartido, o la solución si la pista cambió de enfoque).
3. **Edita celdas preservando el formato**: lee el notebook con `json.load`, cambia `cell["source"]` y escríbelo con `json.dumps(nb, indent=1, ensure_ascii=False) + "\n"`. Ubica celdas por su contenido (texto único), no por índice, y verifica que el texto buscado aparezca exactamente una vez.
4. **Verifica**: vuelve a correr `compare_pair.py` (no deben quedar `+P`/`+S` inesperados), re-ejecuta la versión del profesor con `--save` si cambió código, y ejecuta el template sin guardar (sólo se aceptan errores en celdas que dependen de celdas ✍️).
5. **Revisa que no se filtró la solución**: en el template no debe aparecer código resuelto de celdas ✍️, números de resultados ni el nombre de la variable "correcta" a eliminar o elegir.

## Antes de sobrescribir

VS Code guarda salidas y metadata al ejecutar. Antes de reemplazar un notebook, compara sus **fuentes** contra `HEAD`; si el profesor cambió código sin hacer commit, pregúntale antes de sobrescribirlo.

Haz commit/push sólo si el profesor lo pide, un commit por repo con el mismo resumen del cambio.
