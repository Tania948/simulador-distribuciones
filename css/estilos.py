# css/estilos.py
import streamlit as st

st.set_page_config(page_title="Simulador Estadístico", layout="wide", initial_sidebar_state="expanded")

# Guardamos el CSS en una variable de texto limpio
estilos_css = """
<style>
    .texto-adaptable {
    color: var(--text-color);
    font-family: 'Arial', sans-serif;
    text-align: justify;
    font-size: 18px;
    font-weight: normal;
    line-height: 1.6;
    }
"""

pestanas_css = """<style>
    /* Rosita */
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FF69B4 !important;
        border-color: #FF69B4 !important;
    }
    /* Hover en pestañas */
    button[data-baseweb="tab"]:hover {
        color: #FFB6C1 !important;
    }
}
</style>
"""

def aplicar_estilos_inicio():
    """Inyecta el CSS base de forma invisible."""
    st.markdown(estilos_css, unsafe_allow_html=True)

def titulo_rosa(texto):
    """Pinta cualquier título centrado en color rosa."""
    st.markdown(f"<h2 style='text-align: center; color: #FF69B4; font-size: 32px;'>{texto}</h2>", unsafe_allow_html=True)

def parrafo_adaptable(texto):
    """Pinta párrafos que respetan el modo oscuro automáticamente."""
    st.markdown(f"<p class='texto-adaptable'>{texto}</p>", unsafe_allow_html=True)

def aplicar_estilos_pestanas():
    """Inyecta el CSS específico para las pestañas."""
    st.markdown(pestanas_css, unsafe_allow_html=True)

def importar_estilos():
    """Función para importar todos los estilos de una vez."""
    aplicar_estilos_inicio()
    aplicar_estilos_pestanas()