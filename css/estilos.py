# css/estilos.py
import streamlit as st

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