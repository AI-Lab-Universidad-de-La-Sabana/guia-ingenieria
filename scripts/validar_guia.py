#!/usr/bin/env python3
"""Valida la coherencia interna de la guía (README.md). Lo ejecutan `make check` y CI.

Comprueba que:
  1. Cada regla [XXX-NN] se define una sola vez, con su ancla <a id="xxx-nn"></a>.
  2. Toda regla citada en el texto existe.
  3. Todo enlace interno (#ancla) apunta a un encabezado o a una regla que existe.
  4. Todo enlace relativo apunta a un archivo que existe en el repositorio.
  5. Los bloques de código están cerrados.
  6. Todo enlace de referencia ([texto][etiqueta]) tiene su definición, y no hay definiciones sin usar.

Solo usa la librería estándar de Python.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
REGLA = r"[A-Z]{2,4}-\d{2}"


def slug_github(titulo: str) -> str:
    """Reproduce cómo GitHub genera el ancla de un encabezado."""
    texto = re.sub(r"`([^`]*)`", r"\1", titulo)  # el código en línea conserva su texto
    texto = re.sub(
        r"\[([^\]]*)\]\([^)]*\)", r"\1", texto
    )  # los enlaces conservan su texto
    texto = texto.strip().lower()
    resultado = []
    for caracter in texto:
        categoria = unicodedata.category(caracter)
        if caracter in " -":
            resultado.append("-" if caracter == " " else caracter)
        elif caracter == "_" or categoria[0] in ("L", "N") or categoria == "Mn":
            resultado.append(caracter)
    return "".join(resultado)


def sin_bloques_de_codigo(texto: str) -> str:
    return re.sub(r"```.*?```", "", texto, flags=re.DOTALL)


def validar(archivo: Path) -> list[str]:
    errores: list[str] = []
    texto = archivo.read_text(encoding="utf-8")

    if texto.count("```") % 2:
        errores.append("Hay un bloque de código sin cerrar (``` impar).")

    cuerpo = sin_bloques_de_codigo(texto)

    # Anclas de encabezados (GitHub numera los repetidos con -1, -2...)
    anclas: set[str] = set()
    vistos: dict[str, int] = {}
    for titulo in re.findall(r"^#{1,6}\s+(.+?)\s*$", cuerpo, flags=re.MULTILINE):
        base = slug_github(titulo)
        n = vistos.get(base, 0)
        anclas.add(base if n == 0 else f"{base}-{n}")
        vistos[base] = n + 1

    # Reglas: definición única con ancla
    definiciones = re.findall(rf'<a id="([a-z]+-\d+)"></a>\*\*\[({REGLA})\]', cuerpo)
    ids = [regla for _, regla in definiciones]
    for ancla, regla in definiciones:
        if ancla != regla.lower():
            errores.append(f"El ancla '{ancla}' no coincide con la regla {regla}.")
        anclas.add(ancla)
    duplicadas = sorted({r for r in ids if ids.count(r) > 1})
    if duplicadas:
        errores.append(f"Reglas definidas más de una vez: {', '.join(duplicadas)}.")

    citadas = set(re.findall(rf"\[({REGLA})\]", cuerpo))
    for regla in sorted(citadas - set(ids)):
        errores.append(f"Se cita la regla {regla}, pero no está definida.")

    # Enlaces internos y relativos
    for destino in re.findall(r"\]\(([^)\s]+)\)", cuerpo):
        if destino.startswith("#"):
            if destino[1:] not in anclas:
                errores.append(f"Enlace interno roto: {destino}")
        elif not re.match(r"^[a-z]+:", destino):
            ruta = (archivo.parent / destino.split("#")[0]).resolve()
            if not ruta.exists():
                errores.append(f"Enlace a un archivo que no existe: {destino}")

    # Enlaces de referencia (p. ej., [`Makefile`][pp-makefile] → definición al final del README)
    definidas = set(re.findall(r"^\[([a-z0-9-]+)\]:\s+\S+", cuerpo, flags=re.MULTILINE))
    usadas = set(re.findall(r"\]\[([a-z0-9-]+)\]", cuerpo))
    for etiqueta in sorted(usadas - definidas):
        errores.append(f"Enlace de referencia sin definición: [{etiqueta}]")
    for etiqueta in sorted(definidas - usadas):
        errores.append(f"Definición de enlace sin usar: [{etiqueta}]")

    print(
        f"{archivo.name}: {len(ids)} reglas, {len(anclas)} anclas, {len(definidas)} enlaces de referencia."
    )
    return errores


def main() -> int:
    errores = validar(RAIZ / "README.md")
    for error in errores:
        print(f"ERROR: {error}")
    if errores:
        return 1
    print("Guía válida.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
