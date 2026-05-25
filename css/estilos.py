import streamlit as st

st.set_page_config(page_title="Simulador Estadístico", layout="wide", initial_sidebar_state="expanded")

estilos_css = """
<style>
/* Quitar los márgenes internos extremos que deja Streamlit por defecto */
.block-container {
    max-width: 90% !important; /* Cambia esto a 100% si lo quieres pegado a las orillas */
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

.texto-adaptable {
    color: var(--text-color);
    font-family: 'Arial', sans-serif;
    text-align: justify;
    font-size: 18px;
    font-weight: normal;
    line-height: 1.6;
}
</style>
"""

pestanas_css = """<style>
    /* Cambia el texto y el borde del botón de la pestaña activa */
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FF69B4 !important;
        border-color: #FF69B4 !important;
    }
    
    /* Hover en pestañas */
    button[data-baseweb="tab"]:hover {
        color: #FFB6C1 !important;
    }

    /* Fuerza a que la barra indicadora inferior sea rosa */
    div[data-baseweb="tab-highlight-bar"] {
        background-color: #FF69B4 !important;
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