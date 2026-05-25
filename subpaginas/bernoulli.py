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
    
    # ==========================================
    # 1. CONTROL DE ESTADO SÍNCRONO (EL CORAZÓN)
    # ==========================================
    # Valor inicial por defecto en el estado global
    if 'p_bernoulli' not in st.session_state:
        st.session_state['p_bernoulli'] = 0.30

    # CALLBACKS: Se ejecutan antes de volver a pintar la pantalla
    def sincronizar_desde_slider():
        # Captura lo que tiene la barra y se lo asigna al estado global
        st.session_state['p_bernoulli'] = st.session_state['control_slider']

    def sincronizar_desde_numero():
        val = st.session_state['control_num']
        # Validamos límites por seguridad matemática [0.0, 1.0]
        st.session_state['p_bernoulli'] = min(max(val, 0.0), 1.0)

    # El valor final unificado que leerán ambos componentes en este renderizado
    p_actual = st.session_state['p_bernoulli']

    # ==========================================
    # 2. DISEÑO RESPONSIVO (COLUMNAS LADO A LADO)
    # ==========================================
    col_izquierda, col_derecha = st.columns([1.2, 1], gap="large")
    
    with col_izquierda:
        st.subheader("⚙️ Parámetros de la distribución")
        parrafo_adaptable("Ajusta la probabilidad de éxito (p):")

        # CONTROL A: Deslizador Principal
        st.slider(
            "Selecciona con la barra:",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            key='control_slider',
            value=p_actual,
            on_change=sincronizar_desde_slider,
            label_visibility="collapsed"
        )
        
        # CONTROL B: Entrada Manual Discreta (Cuadradito pequeño alineado)
        col_txt, col_inp = st.columns([2, 1])
        with col_txt:
            st.write("**O ingresa p manualmente:**")
        with col_inp:
            st.number_input(
                "Input numérico discreto",
                min_value=0.0,
                max_value=1.0,
                step=0.01,
                key='control_num',
                value=p_actual,
                on_change=sincronizar_desde_numero,
                label_visibility="collapsed"
            )

        # Cálculos de los Indicadores Teóricos basados en el p_actual ya sincronizado
        q_final = 1.0 - p_actual
        varianza = p_actual * q_final
        
        # INDICADORES TEÓRICOS
        st.markdown("### 📊 Indicadores Teóricos")
        col_ind1, col_ind2, col_ind3 = st.columns(3)
        with col_ind1:
            st.metric(label="Pr. Fracaso (q)", value=f"{q_final:.4f}")
        with col_ind2:
            st.metric(label="Esperanza (μ)", value=f"{p_actual:.4f}")
        with col_ind3:
            st.metric(label="Varianza (σ²)", value=f"{varianza:.4f}")

    with col_derecha:
        st.subheader("📈 Simulación Visual")
        
        # Recuperamos la muestra global N guardada en app.py (por defecto 1000)
        n_muestra = st.session_state.get('tamano_muestra', 1000)
        
        # Generación aleatoria usando las probabilidades reales configuradas
        datos_simulados = np.random.choice([0, 1], size=n_muestra, p=[q_final, p_actual])
        exitos = np.sum(datos_simulados == 1)
        fracasos = np.sum(datos_simulados == 0)
        
        # Construcción estética del gráfico en Matplotlib
        fig, ax = plt.subplots(figsize=(5, 3.8))
        categorias = ['Fracaso (0)', 'Éxito (1)']
        conteos = [fracasos, exitos]
        
        # Paleta corporativa (Gris oscuro y Rosa)
        ax.bar(categorias, conteos, color=['#31333F', '#FF69B4'], width=0.45)
        ax.set_ylabel('Frecuencia Absoluta', fontsize=10)
        ax.set_title(f'Resultados para N = {n_muestra}', fontsize=11, fontweight='bold')
        
        # Limpieza de los bordes del gráfico para un look moderno
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        st.pyplot(fig)