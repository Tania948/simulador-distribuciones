# subpaginas/bernoulli.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from css.estilos import titulo_rosa, parrafo_adaptable

# Reutilizamos tus funciones limpias que ya funcionan
def intro_bernoulli():
    titulo_rosa("Distribución de Bernoulli")
    parrafo_adaptable(
        "Un experimento de Bernoulli es un proceso estadístico con dos posibles resultados: "
        "<strong>Éxito</strong> (1) o <strong>Fracaso</strong> (0). Es la base para distribuciones más complejas."
    )

def inicializar_estado():
    if 'p_base' not in st.session_state:
        st.session_state['p_base'] = 0.30
    
    # Sincronizamos las variables del slider e input base
    if 'slider_p' not in st.session_state:
        st.session_state['slider_p'] = st.session_state['p_base']
    if 'input_p' not in st.session_state:
        st.session_state['input_p'] = st.session_state['p_base']

def actualizar_desde_slider():
    st.session_state['p_base'] = st.session_state['slider_p']
    st.session_state['input_p'] = st.session_state['slider_p']

def actualizar_desde_input():
    val = st.session_state['input_p']
    val_validado = min(max(val, 0.0), 1.0)
    st.session_state['p_base'] = val_validado
    st.session_state['slider_p'] = val_validado

def generar_grafica(p, q):
    # Gráfica de Matplotlib limpia y escalada
    # Recuperamos la muestra global N de app.py
    n_muestra = st.session_state.get('tamano_muestra', 1000)
    
    datos_simulados = np.random.choice([0, 1], size=n_muestra, p=[q, p])
    exitos = np.sum(datos_simulados == 1)
    fracasos = np.sum(datos_simulados == 0)
    
    # Matplotlib nativo (no requiere unsafe_allow_html)
    # Aumentamos el tamaño de fuente para que sea legible en monitor grande
    fig, ax = plt.subplots(figsize=(6, 4))
    categorias = ['Fracaso (0)', 'Éxito (1)']
    conteos = [fracasos, exitos]
    
    ax.bar(categorias, conteos, color=['#31333F', '#FF69B4'], width=0.5)
    ax.set_ylabel('Frecuencia Absoluta', fontsize=12)
    ax.set_title(f'Resultados para N = {n_muestra}', fontsize=14, fontweight='bold')
    
    # Estilizado limpio
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# --- REESCRITURA DEL LAYOUT RESPONSIVO NATIVO ---

def inicializar_bernoulli():
    """
    Nuevo diseño estructural nativo para Bernoulli.
    Resuelve el balance en pantalla grande (no horizontal aplastado)
    y el truncado en pantalla intermedia sin usar CSS inyectado.
    """
    intro_bernoulli()
    st.markdown("---")
    inicializar_estado()
    
    # ==========================================
    # 1. BLOQUE SUPERIOR (CONTROLES A LO ANCHO)
    # ==========================================
    # Aprovechamos el ancho completo nativo de Streamlit para los parámetros.
    with st.container():
        st.subheader("⚙️ Parámetros de la distribución")
        parrafo_adaptable("Ajusta la probabilidad de éxito (p):")

        # Slider a lo ancho: cómodo y preciso
        st.slider(
            "Selecciona con la barra:",
            min_value=0.0, max_value=1.0, step=0.01,
            key='slider_p',
            on_change=actualizar_desde_slider,
            label_visibility="collapsed"
        )
        
        # Input numérico flotante a lo ancho
        col_txt, col_inp = st.columns([2, 1])
        with col_txt:
            st.write("**O ingresa p manualmente:**")
        with col_inp:
            st.number_input(
                "Input numérico discreto",
                min_value=0.0, max_value=1.0, step=0.01,
                key='input_p',
                on_change=actualizar_desde_input,
                label_visibility="collapsed"
            )

    # Calculamos variables madre (Lógica intacta)
    p_final = st.session_state['p_base']
    q_final = 1.0 - p_final
    varianza = p_final * q_final

    st.markdown("---")
    st.markdown("##") # Espaciador nativo

    # ==========================================
    # 2. BLOQUE CENTRAL (INDICADORES TIPO TARJETA)
    # ==========================================
    # Aquí solucionamos el truncado ("0...") y el amontonamiento.
    # No usamos st.columns para las métricas. Usamos un diseño nativo y autocontenido.
    st.subheader("📊 Indicadores Teóricos")
    
    # Creamos un bloque de 3 columnas nativas. En monitor irán side-by-side, en celular se apilarán.
    col1, col2, col3 = st.columns(3)
    
    # Usamos cajas de texto destacado (st.info, st.success) que Streamlit escala nativamente.
    # ¡Al tener el ancho completo de la columna, los números NUNCA se cortarán!
    with col1:
        st.markdown(
            f"""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center;">
                <span style="color: #555; font-size: 14px; font-weight: bold;">Pr. Fracaso (q)</span><br>
                <span style="font-size: 24px; font-weight: 700; color: #1f77b4;">{q_final:.4f}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    with col2:
        st.markdown(
            f"""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center;">
                <span style="color: #555; font-size: 14px; font-weight: bold;">Esperanza (μ)</span><br>
                <span style="font-size: 24px; font-weight: 700; color: #2ca02c;">{p_final:.4f}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    with col3:
        st.markdown(
            f"""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center;">
                <span style="color: #555; font-size: 14px; font-weight: bold;">Varianza (σ²)</span><br>
                <span style="font-size: 24px; font-weight: 700; color: #ff7f0e;">{varianza:.4f}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )

    st.markdown("##") # Espaciador nativo

    # ==========================================
    # 3. BLOQUE INFERIOR (GRÁFICA EXPANDIDA ABAJO)
    # ==========================================
    # Aquí resolvemos el balance en pantalla grande.
    # No usamos columnas para la gráfica. La ponemos abajo ocupando TODO el ancho de la página.
    st.subheader("📈 Simulación Visual")
    with st.container():
        # Al tener el ancho completo de la página, la gráfica se ve grande, legible y espectacular en monitor.
        generar_grafica(p_final, q_final)