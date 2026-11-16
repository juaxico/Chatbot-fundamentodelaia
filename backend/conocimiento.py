"""Lee los hechos de la base Prolog entregada en la primera etapa."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prolog" / "gimnasio.pl"

PREDICADOS = {
    "trabaja_musculo": "musculos",
    "utiliza_equipo": "equipos",
    "tiene_nivel": "niveles",
    "tipo_ejercicio": "tipos",
}
HECHO = re.compile(r"^\s*(trabaja_musculo|utiliza_equipo|tiene_nivel|tipo_ejercicio)\(([a-z][a-z0-9_]*),\s*([a-z][a-z0-9_]*)\)\.\s*$")


def cargar_ejercicios(archivo: Path = BASE) -> dict[str, dict[str, list[str]]]:
    """Lee los hechos, sin duplicar ni modificar la base de conocimiento."""
    ejercicios: dict[str, dict[str, list[str]]] = {}
    for linea in archivo.read_text(encoding="utf-8-sig").splitlines():
        match = HECHO.fullmatch(linea)
        if not match:
            continue
        predicado, nombre, valor = match.groups()
        registro = ejercicios.setdefault(nombre, {campo: [] for campo in PREDICADOS.values()})
        campo = PREDICADOS[predicado]
        if valor not in registro[campo]:
            registro[campo].append(valor)
    return ejercicios


def grupos_musculares(archivo: Path = BASE) -> dict[str, list[str]]:
    grupos: dict[str, list[str]] = {}
    patron = re.compile(r"^\s*grupo_muscular\(([a-z][a-z0-9_]*),\s*([a-z][a-z0-9_]*)\)\.\s*$")
    for linea in archivo.read_text(encoding="utf-8-sig").splitlines():
        match = patron.fullmatch(linea)
        if match:
            grupo, musculo = match.groups()
            grupos.setdefault(grupo, []).append(musculo)
    return grupos


def conocimiento_para_llm() -> str:
    """Conocimiento enviado al LLM: exactamente lo leído del archivo .pl."""
    ejercicios = cargar_ejercicios()
    grupos = grupos_musculares()
    lineas = ["CATALOGO DE EJERCICIOS (la unica fuente de datos):"]
    for nombre, info in ejercicios.items():
        lineas.append(
            f"- {nombre.replace('_', ' ')}: musculos={', '.join(info['musculos'])}; "
            f"equipos={', '.join(info['equipos'])}; "
            f"nivel={', '.join(info['niveles'])}; tipo={', '.join(info['tipos'])}."
        )
    lineas.append("GRUPOS MUSCULARES:")
    for grupo, musculos in grupos.items():
        lineas.append(f"- {grupo}: {', '.join(musculos)}")
    return "\n".join(lineas)
