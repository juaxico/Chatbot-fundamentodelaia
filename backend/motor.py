"""Conecta el servidor Python con SWI-Prolog por proceso independiente.

Una consulta siempre pasa por el motor SWI-Prolog real; no se simulan
respuestas del archivo .pl dentro de Python.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from .interpretador import Consulta, interpretar

ROOT = Path(__file__).resolve().parents[1]
MOTOR = ROOT / "prolog" / "motor_chatbot.pl"


class PrologNoDisponible(RuntimeError):
    pass


def consultar(consulta: Consulta) -> list[str]:
    binario = shutil.which("swipl")
    if not binario:
        raise PrologNoDisponible("SWI-Prolog no está instalado o swipl no figura en el PATH.")
    args = [binario, "-q", "-s", str(MOTOR), "-g", "main", "--", *consulta.argumentos()]
    try:
        ejecucion = subprocess.run(args, cwd=MOTOR.parent, capture_output=True,
                                   text=True, timeout=8, check=False)
    except subprocess.TimeoutExpired as exc:
        raise PrologNoDisponible("La consulta de Prolog excedió el tiempo máximo.") from exc
    if ejecucion.returncode != 0:
        raise PrologNoDisponible("Error de SWI-Prolog: " + ejecucion.stderr.strip()[:400])
    try:
        salida = json.loads(ejecucion.stdout)
    except json.JSONDecodeError as exc:
        raise PrologNoDisponible("SWI-Prolog devolvió una respuesta ilegible.") from exc
    if not salida.get("ok"):
        raise PrologNoDisponible(salida.get("error", "No se pudo realizar la consulta."))
    return salida["resultados"]


def mostrar_atom(atom: str) -> str:
    return atom.replace("_", " ")


def responder(pregunta: str) -> dict:
    consulta = interpretar(pregunta)
    if consulta is None:
        return {"respuesta": "No pude interpretar esa pregunta. Pregunta por músculos, equipo, nivel o tipo de los ejercicios registrados.",
                "resultados": [], "comprendida": False}
    if consulta.accion == "ficha":
        datos = {}
        for campo in ["musculo", "equipo", "nivel", "tipo"]:
            datos[campo] = consultar(Consulta("atributo", consulta.ejercicio, campo))
        respuesta = (f"{mostrar_atom(consulta.ejercicio).capitalize()}: músculos: {', '.join(map(mostrar_atom, datos['musculo']))}; "
                     f"equipamiento: {', '.join(map(mostrar_atom, datos['equipo']))}; "
                     f"nivel: {', '.join(map(mostrar_atom, datos['nivel']))}; "
                     f"tipo: {', '.join(map(mostrar_atom, datos['tipo']))}.")
        return {"respuesta": respuesta, "resultados": datos, "comprendida": True}
    resultados = consultar(consulta)
    if not resultados:
        return {"respuesta": "No encontré resultados para esa consulta en la base de conocimiento.",
                "resultados": [], "comprendida": True}
    visibles = ", ".join(map(mostrar_atom, resultados))
    if consulta.accion == "atributo":
        nombres = {"musculo": "Músculos", "equipo": "Equipamiento", "nivel": "Nivel", "tipo": "Tipo"}
        respuesta = f"{nombres[consulta.campo]} de {mostrar_atom(consulta.ejercicio)}: {visibles}."
    else:
        respuesta = f"Ejercicios encontrados ({len(resultados)}): {visibles}."
    return {"respuesta": respuesta, "resultados": resultados, "comprendida": True}
