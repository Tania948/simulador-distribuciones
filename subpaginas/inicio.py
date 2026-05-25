import streamlit as st
# Importamos únicamente la función encargada del diseño
from css.estilos import aplicar_estilos_inicio

def textoIntro():
    # El título se queda con su estilo en línea rápido
    st.markdown("<h2 style='text-align: center; color: #FF69B4; font-size: 32px;'>Inicio</h2>", unsafe_allow_html=True)
    
    # Textos limpios que usan la clase que vive en css/estilos.py
    st.markdown("<p class='texto-adaptable'>Seleccione la distribución que desea simular en las pestañas superiores. Ajuste el tamaño de la muestra en la barra lateral para ver cómo afecta a las distribuciones.</p>", unsafe_allow_html=True)
    st.markdown("<p class='texto-adaptable'>Seleccione <strong>Guardar</strong> para ver o descargar aquí las simulaciones deseadas.</p>", unsafe_allow_html=True)

def inicioMostrar():
    aplicar_estilos_inicio()  # Llamamos al módulo de estilos para que prepare la página
    textoIntro()             # Pintamos los textos