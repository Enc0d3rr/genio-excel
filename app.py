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

# --- CONFIGURACIÓN DE LA API (SEGURA) ---
# Streamlit busca automáticamente en .streamlit/secrets.toml
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except FileNotFoundError:
    st.error("⚠️ No encontré el archivo de secretos. Asegúrate de crear .streamlit/secrets.toml")
    st.stop()

# Usamos el modelo Gemini 1.5 Flash (es el más rápido y barato/gratis para esto)
model = genai.GenerativeModel('gemini-1.5-flash')

def consultar_gemini(problema, herramienta):
    """Envía el prompt a Gemini y retorna la respuesta"""
    
    prompt = f"""
    Actúa como un experto avanzado en hojas de cálculo y bases de datos.
    El usuario necesita ayuda con: {herramienta}.
    
    Problema del usuario: "{problema}"
    
    Tu misión:
    1. Proporcionar la fórmula, consulta SQL o código VBA exacto.
    2. Si es una fórmula compleja, explícala en 1 frase simple.
    3. Si el problema no es claro, pide más detalles amablemente.
    4. Responde en Español.
    5. Usa formato Markdown para resaltar el código.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al conectar con Gemini: {e}"

# --- INTERFAZ GRÁFICA ---
st.title("📊 El Genio de las Hojas de Cálculo")
st.write("Escribe qué necesitas hacer y la IA generará la fórmula por ti. Gratis y al instante.")

# Selector
opcion = st.selectbox(
    "¿Qué herramienta estás usando?",
    ["Microsoft Excel", "Google Sheets", "SQL (Bases de datos)", "Python (Pandas)"]
)

# Área de texto
problema_usuario = st.text_area(
    "Describe tu problema:",
    placeholder="Ejemplo: Quiero sumar la columna A solo si la columna B dice 'Ventas' y la fecha es de hoy.",
    height=100
)

# Botón de acción
if st.button("✨ Generar Solución", type="primary"):
    if not problema_usuario:
        st.warning("Por favor, escribe tu problema primero.")
    else:
        with st.spinner("🧠 Analizando lógica..."):
            resultado = consultar_gemini(problema_usuario, opcion)
            
            st.success("¡Aquí tienes!")
            st.markdown("---")
            st.markdown(resultado)
            st.markdown("---")
            st.caption("Copia el código y pégalo en tu herramienta.")

# --- SECCION DE MOETIZACION ---
st.divider()
st.write("¿Te sirvió? Invítame un café para seguir mejorando la IA:")
st.link_button("Donar con PayPal", "https://paaypal.me/Hunterb0y7z")

# Footer simple
st.markdown("Power by Python")
