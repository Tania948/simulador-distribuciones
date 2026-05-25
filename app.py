# app.py
import streamlit as st
from subpaginas.inicio import mostrar_inicio
from subpaginas.bernoulli import inicializar_bernoulli
from css.estilos import importar_estilos

# Inyectamos los estilos CSS globales desde tu archivo de estilos
importar_estilos()
st.title("Simulador de Distribuciones - Probabilidad y estadística")

# Menú lateral
st.sidebar.header("Tamaño de la muestra")
st.sidebar.markdown("(Este parámetro afecta a todas las distribuciones)")
tamano_muestra = st.sidebar.number_input("**Ingrese el tamaño de la muestra**", min_value=1, max_value=100000, value=1000)
st.session_state['tamano_muestra'] = tamano_muestra

# Menú de pestañas
pestanas = st.tabs([
    "Inicio",
    "Bernoulli", 
    "Binomial", 
    "Geometrica", 
    "Hipergeometrica", 
    "Poisson"
])

with pestanas[0]:
    mostrar_inicio()

with pestanas[1]:
    inicializar_bernoulli()