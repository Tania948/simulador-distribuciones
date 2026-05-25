import streamlit as st

# =====================================================================
# 1. ENRUTADOR DE PÁGINAS MODULARES
# =====================================================================
from subpaginas.inicio import inicioMostrar

# =====================================================================
# 2. CONFIGURACIÓN GLOBAL DE LA INTERFAZ
# =====================================================================
st.set_page_config(
    page_title="Simulador Estadístico", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.title("Simulador de Distribuciones - Probabilidad y estadística")

# Inyección de estilos CSS globales exclusiva para el menú de pestañas
st.markdown("""
    <style>
        /* Pestaña seleccionada (Modo Rosita) */
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #FF69B4 !important;
            border-color: #FF69B4 !important;
        }
        /* Hover al pasar el mouse por las pestañas */
        button[data-baseweb="tab"]:hover {
            color: #FFB6C1 !important;
        }
    </style>
""", unsafe_allow_html=True)


# =====================================================================
# 3. PANEL DE CONTROL (BARRA LATERAL)
# =====================================================================
st.sidebar.header("Tamaño de la muestra")
st.sidebar.markdown("(Este parámetro afecta a todas las distribuciones)")

tamano_muestra = st.sidebar.number_input(
    "**Ingrese el tamaño de la muestra**", 
    min_value=1, 
    max_value=100000, 
    value=1000
)
# Guardamos la muestra en el estado global para que las subpáginas la lean
st.session_state['tamano_muestra'] = tamano_muestra


# =====================================================================
# 4. MENÚ DE OPCIONES (Navegación horizontal)
# =====================================================================
pestanas = st.tabs([
    "Inicio",
    "Bernoulli", 
    "Binomial", 
    "Geometrica", 
    "Hipergeometrica", 
    "Poisson"
])

# Conexión modular con cada pestaña
with pestanas[0]:
    inicioMostrar()
    
with pestanas[1]:
    st.markdown("<h2 style='text-align: center; color: #FF69B4;'>Distribución de Bernoulli</h2>", unsafe_allow_html=True)
    st.info("Próximamente: Aquí mandaremos a llamar mostrar_bernoulli()")