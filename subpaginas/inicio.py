import streamlit as st

def modoOscuro():
    if st.session_state.get("dark_mode", True):
        st.markdown(
            """<style>
    body { color: #31333F; background-color: #FFFFFF; }
    .stApp { background-color: #FFFFFF; }
    .stButton>button { background-color: #FF69B4; color: #FFFFFF; border: none; padding: 10px 20px; border-radius: 5px; font-size: 16px; }
    .stButton>button:hover { background-color: #FF1493; }
    </style>""",
            unsafe_allow_html=True,
        )
            
            


def textoIntro():
    st.markdown("<h2 style='text-align: center; color: #FF69B4; font-size: 32px;'>Inicio</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; color: #31333F; font-size: 20px; font-weight: normal; line-height: 1.6;'>Seleccione la distribución que desea simular en las pestañas superiores. Ajuste el tamaño de la muestra en la barra lateral para ver cómo afecta a las distribuciones.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; color: #31333F; font-size: 18px; font-weight: normal;'>Seleccione <strong>Guardar</strong> para ver o descargar aquí las simulaciones deseadas.</p>", unsafe_allow_html=True)


def inicioMostrar():
    modoOscuro()
    textoIntro()