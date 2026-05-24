import streamlit as st

# Fondo
st.set_page_config(page_title="Simulador Estadístico", layout="wide", initial_sidebar_state="expanded")
st.title("Simulador de Distribuciones - Probabilidad y estadistica")

# Estilos
st.markdown("""
    <style>
        /* 1. Cambia el color del texto de la pestaña seleccionada y la línea de abajo */
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #FF69B4 !important;
            border-color: #FF69B4 !important;
        }
        /* 2. Cambia el color del texto cuando pasas el mouse por encima de una pestaña */
        button[data-baseweb="tab"]:hover {
            color: #FFB6C1 !important;
        }
    </style>
""", unsafe_allow_html=True)

#N global
st.sidebar.header("Tamaño de la muestra")
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
pestanas("<h2 style='color: #FF69B4'; margin-bottom: 0;>")

with pestanas[0]:
    st.write("Menu principal")

with pestanas[1]:
    st.write("Simulador de distribución Bernoulli")
