"""Aplicación FastAPI. Ejecutar: python -m uvicorn backend.app:app --reload"""
from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import llm, motor

ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title="GimnasIA", version="2.0", description="Chatbot Prolog vs LLM")
app.mount("/static", StaticFiles(directory=str(ROOT / "frontend")), name="static")


class Mensaje(BaseModel):
    pregunta: str = Field(min_length=1, max_length=500)
    modo: str = "comparar"


@app.get("/")
def inicio():
    return FileResponse(ROOT / "frontend" / "index.html")


@app.get("/api/estado")
def estado():
    return {"prolog": shutil.which("swipl") is not None,
            "llm": llm.gemini_disponible(), "gemini_configurada": bool(llm._clave()), "modelo": llm.GEMINI_MODEL}


@app.get("/api/preguntas")
def preguntas():
    from .preguntas import PREGUNTAS
    return [{"id": p["id"], "pregunta": p["pregunta"], "categoria": p["categoria"]}
            for p in PREGUNTAS]


@app.post("/api/chat")
def chat(mensaje: Mensaje):
    if mensaje.modo not in {"prolog", "llm", "comparar"}:
        return {"error": "Modo no válido. Use prolog, llm o comparar."}
    salida = {"pregunta": mensaje.pregunta, "modo": mensaje.modo}
    if mensaje.modo in ("prolog", "comparar"):
        try:
            salida["prolog"] = motor.responder(mensaje.pregunta)
        except motor.PrologNoDisponible as exc:
            salida["prolog"] = {"error": str(exc)}
    if mensaje.modo in ("llm", "comparar"):
        try:
            salida["llm"] = {"respuesta": llm.llamar_gemini(mensaje.pregunta)}
        except llm.LLMNoDisponible as exc:
            salida["llm"] = {"error": str(exc)}
    return salida
