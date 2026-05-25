import streamlit as st
from css.estilos import titulo_rosa

def intro_binomial():
    titulo_rosa("Distribución Binomial")

def solicitar_parametros():
    parrafo_adaptable("Ingresa los datos con los que trabajaremos:")
    st.text_input("")

def inicializar_binomial():
    intro_binomial()
    solicitar_parametros()