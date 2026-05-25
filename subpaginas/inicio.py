import streamlit as st

def modoOscuro():
    # Usamos las variables nativas de Streamlit:
    # --text-color se adapta solo al tema activo (claro u oscuro)
    st.markdown("""
        <style>
            .texto-adaptable {
                color: var(--text-color);
                font-family: 'Arial', sans-serif;
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

def textoIntro():
    # 1. El título sigue siendo rosa (se ve bien en fondo claro y oscuro)
    st.markdown("<h3 style='text-align: left; color: #FF69B4; font-size: 32px;'>Inicio</h3>", unsafe_allow_html=True)
    
    # 2. Las instrucciones usan la clase CSS 'texto-adaptable' que cambia sola
    st.markdown("<p class='texto-adaptable' style='font-size: 20px; font-weight: normal; line-height: 1.6;'>Seleccione la distribución que desea simular en las pestañas superiores. Ajuste el tamaño de la muestra en la barra lateral para ver cómo afecta a las distribuciones.</p>", unsafe_allow_html=True)
    
    st.markdown("<p class='texto-adaptable' style='font-size: 18px; font-weight: normal;'>Seleccione <strong>Guardar</strong> para ver o descargar aquí las simulaciones deseadas.</p>", unsafe_allow_html=True)

def inicioMostrar():
    modoOscuro()
    textoIntro()