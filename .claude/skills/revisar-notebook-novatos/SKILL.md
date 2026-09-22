---
name: revisar-notebook-novatos
description: Revisa un notebook de clase (Jupyter) desde la perspectiva de alumnos novatos en data science y Python y da retroalimentación pedagógica y técnica concreta con una propuesta de estructura - extensión y ritmo para una sesión de 3 horas, cantidad de conceptos, claridad de la historia, interpretación de resultados, variables sobrescritas, errores conceptuales y dificultad de las celdas para el alumno. Úsala cuando el profesor pregunte si un notebook es muy largo, si es buena demostración, si es adecuado para principiantes, o pida retroalimentación, opinión o mejoras sobre un notebook, caso o laboratorio, aunque no mencione a los novatos.
---

# Revisar notebook para novatos

Da una opinión honesta y accionable, como lo haría un colega con experiencia docente. El profesor decide; tu trabajo es que vea con claridad qué funciona, qué no, y qué harías tú.

Lee `.claude/skills/crear-laboratorio/references/convenciones.md` (público, formato de sesión, estructura de laboratorio y errores técnicos conocidos). El laboratorio `01-regresion-lineal/caso_mpg.ipynb` es el ejemplo de referencia de cómo se ve un laboratorio bien estructurado para este curso.

## 1. Leer el notebook completo
```bash
python3 .claude/skills/crear-laboratorio/scripts/notebook_outline.py <notebook> --full
```
Si hay versión template en el repo de students, revísala también (misma ruta relativa): muchos problemas de dificultad sólo se ven ahí. Si el notebook tiene salidas, lee también los resultados clave (métricas, summaries); si no, ejecútalo con `run_notebooks.py` (sin `--save`) para conocer los números.

## 2. Evaluar

**Historia y propósito**
- ¿Hay una pregunta que el notebook responde? ¿Se responde al final?
- ¿Cada técnica nueva está motivada por un problema que el alumno acaba de ver?
- ¿Se interpretan los resultados en palabras y unidades, o sólo se imprimen?

**Carga cognitiva y ritmo** (sesión de 3 h, alumnos que apenas empiezan con Python)
- ¿Cuántos conceptos nuevos introduce? ¿Hay teoría mezclada con práctica que convenga separar?
- ¿Cuánto tiempo tomaría cada parte con alumnos escribiendo código? Estima minutos por sección.
- ¿Hay código repetido que distraiga del concepto (candidato a helper)?
- ¿Se muestran salidas abrumadoras (un `summary()` completo) sin decir qué mirar?

**Robustez para el alumno**
- ¿Variables que se sobrescriben o reasignan (ejecutar fuera de orden cambia resultados)?
- En el template: ¿la dificultad de las celdas ✍️ es pareja?, ¿alguna pide todo un flujo de golpe?, ¿las pistas son suficientes sin regalar la respuesta?, ¿hay celdas dadas que fallan si el alumno se equivocó antes?

**Corrección técnica**: revisa la sección 6 de `convenciones.md` (dummies, fit en test, escalado antes de RFE, pandas 3, plotly 7, números en markdown vs salidas). Un error conceptual que el notebook enseña como correcto es el hallazgo más importante: menciónalo primero.

## 3. Responder
Responde en español, directo:
1. **Veredicto** en 1-2 frases (p. ej. "Sí, es demasiado extenso, y tiene un problema de fondo").
2. **Hallazgos numerados**, del más grave al menos grave, cada uno con dónde está (celda o sección), por qué afecta a un novato y qué harías.
3. **Estructura propuesta** en una tabla: parte, tiempo, qué pasa. Los tiempos suman la duración de la sesión. Indica qué mover a otro notebook o sesión en lugar de simplemente borrarlo.
4. **Ofrece aplicarlo** en ambos repos (con la skill `crear-laboratorio` si es una reestructura completa, o `sincronizar-template` si son cambios puntuales).

No modifiques el notebook durante la revisión: el profesor pidió una opinión.
