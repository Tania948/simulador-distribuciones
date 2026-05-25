# subpaginas/bernoulli.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_bernoulli():
    titulo_rosa("Distribución de Bernoulli")
    parrafo_adaptable(
        "Un experimento de Bernoulli es un proceso estadístico con dos posibles resultados: "
        "<strong>Éxito</strong> (1) o <strong>Fracaso</strong> (0). Es la base para distribuciones más complejas."
    )

def inicializar_bernoulli():
    intro_bernoulli()
    st.markdown("---")
    
    # 1. CONTROL DE ESTADO (Sincronización perfecta)
    if 'p_bernoulli' not in st.session_state:
        st.session_state['p_bernoulli'] = 0.5

    # Funciones que se ejecutan al interactuar con los inputs
    def actualizar_desde_slider():
        st.session_state['p_bernoulli'] = st.session_state['slider_p']

    def actualizar_desde_numero():
        val = st.session_state['num_p']
        # Forzar a que esté en el rango de probabilidad [0.0, 1.0]
        st.session_state['p_bernoulli'] = min(max(val, 0.0), 1.0)

    # 2. DISEÑO EN COLUMNAS (Lado a lado en PC, apilado en celular)
    col_izquierda, col_derecha = st.columns([1.2, 1], gap="large")
    
    with col_izquierda:
        st.subheader("⚙️ Parámetros de la distribución")
        parrafo_adaptable("Ajusta la probabilidad de éxito (p):")

        # CONTROL 1: Slider (Usa el valor actual del estado)
        p_final = st.slider(
            "Selecciona con la barra:",
            min_value=0.0, max_value=1.0, step=0.01,
            key='slider_p',
            value=st.session_state['p_bernoulli'],
            on_change=actualizar_desde_slider,
            label_visibility="collapsed"
        )
        
        # CONTROL 2: Entrada manual discreta (Alineada y limpia)
        col_txt, col_inp = st.columns([2, 1])
        with col_txt:
            st.write("**O ingresa p manualmente:**")
        with col_inp:
            st.number_input(
                "Input numérico discreto",
                min_value=0.0, max_value=1.0, step=0.01,
                key='num_p',
                value=st.session_state['p_bernoulli'],
                on_change=actualizar_desde_numero,
                label_visibility="collapsed"
            )

        # Recalculamos los indicadores usando estrictamente el valor unificado
        q_final = 1.0 - p_final
        varianza = p_final * q_final
        
        # Indicadores Teóricos en la parte inferior izquierda
        st.markdown("### 📊 Indicadores Teóricos")
        col_ind1, col_ind2, col_ind3 = st.columns(3)
        with col_ind1:
            st.metric(label="Pr. de Fracaso (q)", value=f"{q_final:.4f}")
        with col_ind2:
            st.metric(label="Esperanza (E[X] / μ)", value=f"{p_final:.4f}")
        with col_ind3:
            st.metric(label="Varianza (σ²)", value=f"{varianza:.4f}")

    with col_derecha:
        st.subheader("📈 Simulación Visual")
        
        # Recuperamos el tamaño global N de la muestra
        n_muestra = st.session_state.get('tamano_muestra', 1000)
        
        # Simulación de datos realistas basados en p_final
        datos_simulados = np.random.choice([0, 1], size=n_muestra, p=[q_final, p_final])
        exitos = np.sum(datos_simulados == 1)
        fracasos = np.sum(datos_simulados == 0)
        
        # Configuración estética de la gráfica de Matplotlib
        fig, ax = plt.subplots(figsize=(5, 3.5))
        categorias = ['Fracaso (0)', 'Éxito (1)']
        conteos = [fracasos, exitos]
        
        ax.bar(categorias, conteos, color=['#31333F', '#FF69B4'], width=0.45)
        ax.set_ylabel('Frecuencia Absoluta', fontsize=10)
        ax.set_title(f'Resultados para N = {n_muestra}', fontsize=11, fontweight='bold')
        
        # Ajustes de cuadrícula discretos
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        st.pyplot(fig)