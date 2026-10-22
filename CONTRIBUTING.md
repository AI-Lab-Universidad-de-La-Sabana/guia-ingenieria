# Cómo proponer cambios a la guía

Esta guía se cambia igual que el código: con un issue, una rama y un PR.

1. Abre un issue explicando qué regla quieres añadir, cambiar o quitar, y **por qué** (qué problema real resuelve).
2. Ejecuta `make setup` una vez para activar los hooks.
3. Crea una rama `docs/<numero-issue>-<descripcion>` y edita `README.md`.
4. Reglas nuevas: usa el siguiente número libre del prefijo y su ancla, con este formato:

   ```markdown
   - <a id="cal-06"></a>**[CAL-06] Título corto.** Texto de la regla.
   ```

   Nunca reutilices el identificador de una regla eliminada: márcala como retirada en el CHANGELOG.
5. Actualiza `CHANGELOG.md` y la versión al inicio del `README.md` (mayor si cambia o se elimina una regla
   obligatoria, menor si se añade algo, parche si es redacción).
6. Ejecuta `make check` y abre el PR con título `docs(guia): ...`. Necesita la aprobación de otra persona
   del equipo base.
7. Tras el merge, un integrante del equipo base crea la etiqueta `vX.Y.Z` y su GitHub Release.

**Criterio para aceptar una regla nueva:** debe evitar un problema que ya ocurrió o que es probable, y no
debe poder resolverse mejor con una herramienta automática (plantilla, CI, hook). Si se puede automatizar,
se automatiza en [`plantilla-proyecto`](https://github.com/AI-Lab-Universidad-de-La-Sabana/plantilla-proyecto) y aquí solo se menciona.
