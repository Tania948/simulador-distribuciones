import streamlit as st
from css.estilos import titulo_rosa

def intro_binomial():
    titulo_rosa("Distribución Binomial")

def solicitar_parametros():
    p = st.text.number_input("p = ", min_value=0, max_value=1)

def inicializar_binomial():
    intro_binomial()
    solicitar_parametros