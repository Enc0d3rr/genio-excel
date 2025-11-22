#!/usr/bin/python3

import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURACIÓN DE PAGINA ---
st.set_page_config(
    page_title="Genio de Excel 🧞‍♂️",
    page_icon="📊",
    layout="centered"
)

# --- CONFIGURACIÓN DE LA API ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Error: No se encontró la API Key en secrets.")
    st.stop()

# --- MODELO SELECCIONADO (USANDO TU LISTA) ---
# Usamos gemini-2.0-flash que es rapidísimo
model = genai.GenerativeModel('models/gemini-2.0-flash')

def consultar_gemini(problema, herramienta):
    """Envía el prompt a Gemini y retorna la respuesta"""
    
    prompt = f"""
    Actúa como un experto avanzado en hojas de cálculo y programación.
    Herramienta solicitada: {herramienta}.
    
    El usuario tiene este problema: "{problema}"
    
    Tu misión:
    1. Dame SOLAMENTE la solución (fórmula, código o pasos).
    2. Si es código, usa bloques de código.
    3. Agrega una explicación de 1 línea al final.
    4. Responde en Español.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error de conexión: {e}"

# --- INTERFAZ GRÁFICA ---
st.title("📊 El Genio de las Hojas de Cálculo")
st.markdown("##### Tu asistente de IA para Excel, SQL y Python.")

# Selector
col1, col2 = st.columns([1, 2])
with col1:
    opcion = st.selectbox(
        "Herramienta:",
        ["Excel / Sheets", "SQL", "Python (Pandas)", "Power BI (DAX)"]
    )

# Área de texto
problema_usuario = st.text_area(
    "¿Qué necesitas resolver?",
    placeholder="Ej: Sumar la columna A si la B dice 'Pagado'...",
    height=120
)

# Botón de acción
if st.button("✨ Generar Solución", type="primary"):
    if not problema_usuario:
        st.warning("Escribe tu problema primero.")
    else:
        with st.spinner("🧠 Pensando solución..."):
            resultado = consultar_gemini(problema_usuario, opcion)
            
            st.markdown("### Solución:")
            st.success("¡Aquí tienes!")
            st.markdown(resultado)

# --- MONETIZACIÓN ---
st.divider()
st.caption("¿Te ahorré tiempo de trabajo? Invítame un café:")
# Reemplaza con TU link de PayPal que creamos
st.link_button("☕ Donar con PayPal", "https://paypal.me/TU_LINK_AQUI")
