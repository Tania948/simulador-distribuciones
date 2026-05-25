# app.py
import streamlit as st
from subpaginas.inicio import mostrar_inicio
from subpaginas.bernoulli import inicializar_bernoulli
from subpaginas.geometrica import inicializar_geometrica
from subpaginas.binomial import inicializar_binomial
from css.estilos import importar_estilos


importar_estilos()
st.title("Simulador de Distribuciones - Probabilidad y estadística")

st.sidebar.header("Tamaño de la muestra")
st.sidebar.markdown("(Este parámetro afecta a todas las distribuciones)")
tamano_muestra = st.sidebar.number_input("**Ingrese el tamaño de la muestra**", min_value=1, max_value=100000, value=1000)
st.session_state['tamano_muestra'] = tamano_muestra

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

with pestanas[2]:
    inicializar_binomial()

with pestanas[3]:
    inicializar_geometrica()

