# app.py
import streamlit as st
from subpaginas.bernoulli import inicializar_bernoulli
from subpaginas.geometrica import inicializar_geometrica
from subpaginas.binomial import inicializar_binomial
from subpaginas.hipergeometrica import inicializar_hipergeometrica
from subpaginas.poisson import inicializar_poisson
from subpaginas.uniforme import inicializar_uniforme
from subpaginas.normal import inicializar_normal
from css.estilos import importar_estilos


importar_estilos()
st.title("Simulador de Distribuciones - Probabilidad y estadística")

pestanas = st.tabs([
    "Bernoulli", 
    "Binomial", 
    "Geometrica", 
    "Hipergeometrica", 
    "Poisson",
    "Uniforme",
    "Normal",
    "Exponencial",
    "Gamma"
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

with pestanas[5]:
    inicializar_uniforme()

with pestanas[6]:
    inicializar_normal()
