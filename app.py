#!/usr/bin/python3

import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Diagnóstico API", page_icon="🔧")

# Configuración API
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error de secretos: {e}")

st.title("🔧 Diagnóstico de Modelos")

# Botón para probar conexión
if st.button("Listar Modelos Disponibles"):
    try:
        st.write("Consultando API de Google...")
        modelos = []
        # Buscamos todos los modelos que sirvan para generar texto
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                modelos.append(m.name)
        
        if modelos:
            st.success("¡Conexión exitosa! Estos son los modelos que tu API Key puede usar:")
            st.code("\n".join(modelos))
            st.info("Copia uno de estos nombres (ej: models/gemini-pro) para usarlo en tu app.")
        else:
            st.warning("No se encontraron modelos compatibles.")
            
    except Exception as e:
        st.error(f"Error fatal: {e}")

st.write("---")
st.caption("Si esto funciona, sabremos exactamente qué nombre poner en el código.")
