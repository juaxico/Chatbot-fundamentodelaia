"""Interpreta un conjunto delimitado de preguntas en lenguaje natural.

No se usa un LLM para interpretar las consultas de Prolog: esto permite comparar
reglas deterministas con una implementación generativa de LLM.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from .conocimiento import cargar_ejercicios


@dataclass(frozen=True)
class Consulta:
    accion: str
    ejercicio: str = "ninguno"
    campo: str = "ninguno"
    valor: str = "ninguno"
    filtro_campo: str = "ninguno"
    filtro_valor: str = "ninguno"

    def argumentos(self) -> list[str]:
        return [self.accion, self.ejercicio, self.campo, self.valor,
                self.filtro_campo, self.filtro_valor]


def normalizar(texto: str) -> str:
    texto = "".join(c for c in unicodedata.normalize("NFD", texto.lower())
                    if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", texto)).strip()


ALIAS = {
    "barra_de_dominadas": ("barra de dominadas",),
    "mancuernas": ("mancuernas", "mancuerna"),
    "maquina": ("maquina", "maquinas"),
    "polea": ("polea", "poleas"),
    "banco": ("banco",),
    "barra": ("barra",),
}

CAMPOS = {
    "musculo": ("musculos", "musculo", "trabaja", "trabajan", "entrenan", "estimulan"),
    "equipo": ("equipamiento", "equipo", "implementos", "utiliza", "utilizan", "requiere", "usan", "usa"),
    "nivel": ("dificultad", "nivel"),
    "tipo": ("tipo", "compuesto", "aislamiento"),
}


def contiene(texto: str, termino: str) -> bool:
    return f" {termino} " in f" {texto} "


def detectar_entidad(texto: str, nombres: list[str]) -> str | None:
    # Prioriza 'barra de dominadas' sobre 'barra' y nombres largos.
    for nombre in sorted(nombres, key=len, reverse=True):
        if contiene(texto, normalizar(nombre.replace("_", " "))):
            return nombre
    return None


def interpretar(pregunta: str) -> Consulta | None:
    texto = normalizar(pregunta)
    if not texto:
        return None
    ejercicios = cargar_ejercicios()
    nombre_ejercicio = detectar_entidad(texto, list(ejercicios))
    # Incluye atajos de nombres usados en el lenguaje cotidiano.
    if nombre_ejercicio:
        for campo, pistas in CAMPOS.items():
            if any(contiene(texto, pista) for pista in pistas):
                return Consulta("atributo", nombre_ejercicio, campo)
        return Consulta("ficha", nombre_ejercicio)

    condiciones: list[tuple[str, str]] = []
    grupos = ("piernas", "torso superior", "brazos")
    grupo = detectar_entidad(texto, list(grupos))
    if grupo:
        condiciones.append(("grupo", grupo.replace(" ", "_")))
    musculos = ["isquiotibiales", "cuadriceps", "gluteos", "hombros", "espalda", "pecho", "biceps", "triceps"]
    musculo = detectar_entidad(texto, musculos)
    if musculo:
        condiciones.append(("musculo", musculo))
    equipo = None
    for clave, alias in sorted(ALIAS.items(), key=lambda p: -max(map(len, p[1]))):
        if any(contiene(texto, frase) for frase in alias):
            equipo = clave
            break
    if equipo:
        condiciones.append(("equipo", equipo))
    nivel = detectar_entidad(texto, ["principiantes", "intermedios", "avanzados", "principiante", "intermedio", "avanzado"])
    if nivel:
        condiciones.append(("nivel", nivel[:-1] if nivel.endswith("s") else nivel))
    tipo = detectar_entidad(texto, ["aislamiento", "compuesto", "compuestos"])
    if tipo:
        condiciones.append(("tipo", "compuesto" if tipo == "compuestos" else tipo))
    if not condiciones or len(condiciones) > 2:
        return None
    campo, valor = condiciones[0]
    fc, fv = condiciones[1] if len(condiciones) == 2 else ("ninguno", "ninguno")
    return Consulta("buscar", "ninguno", campo, valor, fc, fv)
