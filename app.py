import streamlit as st

from subpaginas.inicio import mostrar_inicio

# Fondo
st.set_page_config(page_title="Simulador Estadístico", layout="wide", initial_sidebar_state="expanded")
st.title("Simulador de Distribuciones - Probabilidad y estadistica")

# Estilos
st.markdown("""
    <style>
        /* Rosita */
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #FF69B4 !important;
            border-color: #FF69B4 !important;
        }
        /* Hoover en pestañas */
        button[data-baseweb="tab"]:hover {
            color: #FFB6C1 !important;
        }
    </style>
""", unsafe_allow_html=True)

#N global
st.sidebar.header("Tamaño de la muestra")
st.sidebar.markdown("(Este parámetro afecta a todas las distribuciones)")
tamano_muestra = st.sidebar.number_input("**Ingrese el tamaño de la muestra**", min_value=1, max_value=100000, value=1000)
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

with pestanas[0]:
   st.open("subpaginas/inicio.py")
    
with pestanas[1]:
    st.markdown("<h2 style='text-align: center; color: #FF69B4;'>Distribución de Bernoulli</h2>", unsafe_allow_html=True)