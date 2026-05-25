import streamlit as st

from css.estilos import generales

def modoOscuro():
    st.markdown(generales, unsafe_allow_html=True)

def textoIntro():
    st.markdown("<h2 style='text-align: center; color: #FF69B4; font-size: 32px;'>Inicio</h2>", unsafe_allow_html=True)
    
    st.markdown("<p class='texto-adaptable'>Seleccione la distribución que desea simular en las pestañas superiores. Ajuste el tamaño de la muestra en la barra lateral para ver cómo afecta a las distribuciones.</p>", unsafe_allow_html=True)
    st.markdown("<p class='texto-adaptable'>Seleccione <strong>Guardar</strong> para ver o descargar aquí las simulaciones deseadas.</p>", unsafe_allow_html=True)

def inicioMostrar():
    modoOscuro()
    textoIntro()