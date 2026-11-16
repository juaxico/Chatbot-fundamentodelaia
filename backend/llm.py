"""Segundo chatbot: Google Gemini por API HTTP, sin Ollama ni GPU local."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

from .conocimiento import conocimiento_para_llm

# Lee la clave privada del .env de la carpeta principal.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


class LLMNoDisponible(RuntimeError):
    pass


def _clave() -> str:
    return os.getenv("GEMINI_API_KEY", "").strip()


def _cabeceras() -> dict[str, str]:
    return {"Content-Type": "application/json", "x-goog-api-key": _clave()}


def llamar_gemini(pregunta: str) -> str:
    if not _clave():
        raise LLMNoDisponible("Falta GEMINI_API_KEY. Agrégala al archivo .env y reinicia Uvicorn.")

    mensaje = (
        "Eres un chatbot de ejercicios de gimnasio para un proyecto universitario. "
        "Responde solamente usando el conocimiento suministrado. "
        "No inventes ejercicios, músculos, equipamientos, niveles ni tipos. "
        "Para consultas combinadas considera todas las condiciones a la vez. "
        "Si preguntan qué ejercicios trabajan piernas, revisa cuadriceps, gluteos e isquiotibiales "
        "y no repitas ejercicios. Usa nombres legibles en español, una respuesta clara y breve. "
        "Si la pregunta no puede contestarse con el catálogo, dilo explícitamente.\n\n"
        + conocimiento_para_llm()
        + f"\n\nPREGUNTA DEL USUARIO: {pregunta}\nRESPUESTA:"
    )
    datos = json.dumps({
        "contents": [{"role": "user", "parts": [{"text": mensaje}]}],
        "generationConfig": {"temperature": 0, "maxOutputTokens": 1800},
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE}/{GEMINI_MODEL}:generateContent", data=datos,
        headers=_cabeceras(), method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            salida = json.load(resp)
    except urllib.error.HTTPError as exc:
        try:
            detalle = json.loads(exc.read().decode("utf-8"))
            mensaje_error = detalle.get("error", {}).get("message", "Error de Gemini")
        except (ValueError, UnicodeDecodeError, AttributeError):
            mensaje_error = "La API rechazó la solicitud"
        raise LLMNoDisponible(f"Gemini HTTP {exc.code}: {mensaje_error[:220]}") from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise LLMNoDisponible(f"No se pudo conectar con Gemini: {str(exc)[:160]}") from exc
    except ValueError as exc:
        raise LLMNoDisponible("Gemini devolvió una respuesta que no es JSON válido.") from exc

    try:
        partes = salida["candidates"][0]["content"]["parts"]
        respuesta = "\n".join(p["text"] for p in partes if p.get("text")).strip()
    except (KeyError, TypeError, IndexError) as exc:
        raise LLMNoDisponible("Gemini no generó texto (posible bloqueo o respuesta vacía).") from exc
    if not respuesta:
        raise LLMNoDisponible("Gemini devolvió una respuesta vacía.")
    return respuesta


def gemini_disponible() -> bool:
    """Verifica clave/modelo mediante una consulta GET sin generar contenido."""
    if not _clave():
        return False
    req = urllib.request.Request(f"{API_BASE}/{GEMINI_MODEL}", headers=_cabeceras())
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False
