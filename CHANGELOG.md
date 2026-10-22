# Historial de cambios

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Versiones con [SemVer](https://semver.org/lang/es/):
**mayor** cuando cambia o se elimina una regla obligatoria, **menor** cuando se añade una regla o sección,
**parche** para correcciones de redacción.

## [3.0.0] — 2026-10-22

### Cambiado
- La guía pasa a vivir como `README.md` de este repositorio: es la única fuente de verdad. Se dejan de mantener
  las versiones en PDF y LaTeX.
- Escrita para el plan **GitHub Free**: protección de `main` con hooks locales, CI y auditoría ([ORG-04]);
  CI en un solo job por el límite de 2.000 minutos ([CAL-03]); secretos de despliegue sin *environments* ([FLU-05]).
- Quien aprueba un PR es quien lo fusiona ([ORG-04]): los equipos temporales tienen permiso de escritura y
  GitHub Free no puede impedirles fusionar en repositorios privados.
- Las reglas tienen ancla propia (`#org-04`) para enlazarlas desde PR, issues y otros repositorios.

### Añadido
- Enlaces directos a [`plantilla-proyecto`](https://github.com/AI-Lab-Universidad-de-La-Sabana/plantilla-proyecto): botón *Use this template* y cada archivo citado
  (Makefile, hooks, CI, auditoría, scripts y plantillas). El validador comprueba los enlaces de referencia.
- `configuracion-org/`: script de configuración única de la organización.
- `scripts/validar_guia.py` y CI propio: valida reglas, anclas y enlaces de la guía en cada PR.

## [2.1.0] — 2026-10-22
- Ajuste de la versión esencial al plan GitHub Free.

## [2.0.0] — 2026-10-22
- Versión esencial para un equipo base pequeño con equipos temporales: de 194 a 38 reglas.

## [1.1.0] — 2026-10-22
- Capítulo de gestión de repositorios en GitHub (versión extendida).

## [1.0.0] — 2026-10-21
- Versión inicial del manual (extendida, 159 reglas).

[ORG-04]: README.md#org-04
[CAL-03]: README.md#cal-03
[FLU-05]: README.md#flu-05
