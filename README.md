# GimnasIA

Chatbot de ejercicios de gimnasio con dos versiones: Prolog y Gemini.

## Requisitos

- Python y SWI-Prolog instalados.
- Una API Key de Google Gemini.

## Cómo ejecutar la página

1. Abre la carpeta del proyecto en Visual Studio Code.
2. En la terminal, ejecuta:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Copia `.env.example` como `.env` y coloca tu API Key en `GEMINI_API_KEY`.
4. Inicia la página con:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app:app --reload
```

5. Abre **http://127.0.0.1:8000** en el navegador.

En la página puedes elegir **Prolog**, **Gemini** o **comparar ambos**.

