# app.py
import streamlit as st
from subpaginas.inicio import mostrar_inicio
from subpaginas.bernoulli import inicializar_bernoulli
from subpaginas.geometrica import inicializar_geometrica
from subpaginas.binomial import inicializar_binomial
from subpaginas.hipergeometrica import inicializar_hipergeometrica
from subpaginas.poisson import inicializar_poisson
from css.estilos import importar_estilos


importar_estilos()
st.title("Simulador de Distribuciones - Probabilidad y estadística")

pestanas = st.tabs([
    "Inicio",
    "Bernoulli", 
    "Binomial", 
    "Geometrica", 
    "Hipergeometrica", 
    "Poisson"
])


with pestanas[0]:
    inicializar_bernoulli()

with pestanas[1]:
    inicializar_binomial()

with pestanas[2]:
    inicializar_geometrica()

with pestanas[3]:
    inicializar_hipergeometrica()

with pestanas[4]:
    inicializar_poisson()