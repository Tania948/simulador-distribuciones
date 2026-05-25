import streamlit as st

# 1. ENRUTADOR DE PÁGINAS MODULARES
from subpaginas.inicio import inicioMostrar

# 2. CONFIGURACIÓN GLOBAL DE LA INTERFAZ
st.set_page_config(
    page_title="Simulador Estadístico", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.title("Simulador de Distribuciones - Probabilidad y estadística")

# Diseño rosa exclusivo para las pestañas de navegación
st.markdown("""
    <style>
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #FF69B4 !important;
            border-color: #FF69B4 !important;
        }
        button[data-baseweb="tab"]:hover {
            color: #FFB6C1 !important;
        }
    </style>
""", unsafe_allow_html=True)


# 3. PANEL DE CONTROL (BARRA LATERAL)
st.sidebar.header("Tamaño de la muestra")
st.sidebar.markdown("(Este parámetro afecta a todas las distribuciones)")

# CORRECCIÓN: Eliminados los argumentos no válidos que causaban el TypeError
tamano_muestra = st.sidebar.number_input(
    "**Ingrese el tamaño de la muestra**", 
    min_value=1, 
    max_value=100000, 
    value=1000
)
st.session_state['tamano_muestra'] = tamano_muestra


# 4. MENÚ DE OPCIONES
pestanas = st.tabs(["Inicio", "Bernoulli", "Binomial", "Geometrica", "Hipergeometrica", "Poisson"])

with pestanas[0]:
    inicioMostrar()
    
with pestanas[1]:
    st.markdown("<h2 style='text-align: center; color: #FF69B4;'>Distribución de Bernoulli</h2>", unsafe_allow_html=True)