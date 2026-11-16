"use strict";
const chat = document.getElementById("chat");
const form = document.getElementById("form");
const input = document.getElementById("pregunta");
const send = document.getElementById("send");
const modo = document.getElementById("modo");

async function estado() {
  try {
    const respuesta = await fetch("/api/estado", {cache: "no-store"});
    if (!respuesta.ok) throw new Error("Servidor no disponible");
    const info = await respuesta.json();
    for (const nombre of ["prolog", "llm"]) {
      const disponible = !!info[nombre];
      document.getElementById("dot-" + nombre).className = "dot " + (disponible ? "online" : "offline");
      const texto = nombre === "llm" && !disponible && !info.gemini_configurada
        ? "Falta API Key" : (disponible ? "Disponible" : "No disponible");
      document.getElementById("state-" + nombre).textContent = texto;
    }
  } catch (_) {
    for (const nombre of ["prolog", "llm"]) {
      document.getElementById("dot-" + nombre).className = "dot offline";
      document.getElementById("state-" + nombre).textContent = "Sin conexión";
    }
  }
}

function agregarRespuesta(contenedor, titulo, dato) {
  const tarjeta = document.createElement("article");
  tarjeta.className = "answer" + (dato?.error ? " error" : "");
  const etiqueta = document.createElement("span");
  etiqueta.className = "tag";
  etiqueta.textContent = titulo;
  const texto = document.createElement("p");
  texto.textContent = dato?.error || dato?.respuesta || "Sin respuesta";
  tarjeta.append(etiqueta, texto);
  contenedor.append(tarjeta);
}

async function preguntar(texto) {
  const pregunta = String(texto || "").trim();
  if (!pregunta || send.disabled) return;
  chat.querySelector(".welcome")?.remove();
  const turno = document.createElement("div");
  turno.className = "turn";
  const usuario = document.createElement("div");
  usuario.className = "user-text";
  usuario.textContent = pregunta;
  const resultados = document.createElement("div");
  resultados.className = "results";
  turno.append(usuario, resultados);
  chat.append(turno);
  chat.scrollTop = chat.scrollHeight;
  send.disabled = true;
  input.value = "";
  agregarRespuesta(resultados, "Consultando", {respuesta: "Procesando consulta..."});
  try {
    const respuesta = await fetch("/api/chat", {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({pregunta, modo: modo.value})
    });
    if (!respuesta.ok) throw new Error("Error HTTP " + respuesta.status);
    const datos = await respuesta.json();
    resultados.replaceChildren();
    if (datos.prolog) agregarRespuesta(resultados, "Prolog", datos.prolog);
    if (datos.llm) agregarRespuesta(resultados, "LLM (Gemini)", datos.llm);
    if (datos.error) agregarRespuesta(resultados, "Error", {error: datos.error});
  } catch (error) {
    resultados.replaceChildren();
    agregarRespuesta(resultados, "Error", {error: error.message});
  } finally {
    send.disabled = false;
    input.focus();
    chat.scrollTop = chat.scrollHeight;
  }
}

form.addEventListener("submit", evento => { evento.preventDefault(); preguntar(input.value); });
document.getElementById("clear").addEventListener("click", () => {
  chat.replaceChildren();
  const inicio = document.createElement("p");
  inicio.className = "welcome";
  inicio.textContent = "Las respuestas de los chatbots aparecerán aquí.";
  chat.append(inicio); input.focus();
});
document.getElementById("refresh").addEventListener("click", estado);
document.getElementById("ejemplos").addEventListener("click", evento => {
  const boton = evento.target.closest("[data-question]");
  if (boton) preguntar(boton.dataset.question);
});

async function cargarPreguntas() {
  const contenedor = document.getElementById("ejemplos");
  try {
    const respuesta = await fetch("/api/preguntas");
    if (!respuesta.ok) throw new Error("No disponibles");
    const preguntas = await respuesta.json();
    for (const pregunta of preguntas) {
      const boton = document.createElement("button");
      boton.type = "button";
      boton.className = "example-btn";
      boton.dataset.question = pregunta.pregunta;
      boton.textContent = `${pregunta.id}. ${pregunta.pregunta}`;
      contenedor.append(boton);
    }
  } catch (_) {
    contenedor.textContent = "No se pudieron cargar las preguntas sugeridas.";
  }
}

estado();
cargarPreguntas();
