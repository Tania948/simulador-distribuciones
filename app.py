import streamlit as st

# Fondo
st.set_page_config(page_title="Simulador Estadístico", layout="wide", initial_sidebar_state="expanded")
st.title("Simulador de Distribuciones - Probabilidad y estadistica")

#N global
st.sidebar.header("Tamaño de la muestra", color="pink")
st.sidebar.markdown("(Este parámetro afecta a todas las distribuciones)")
tamano_muestra = st.sidebar.number_input("Ingrese el tamaño de la muestra", min_value=1, max_value=100000, value=1000)
st.session_state['tamano_muestra'] = tamano_muestra

# Menu de opciones
pestanas = st.tabs([
    "Inicio",
    "Bernoulli", 
    "Binomial", 
    "Geometrica", 
    "Hipergeometrica", 
    "Poisson"
])
