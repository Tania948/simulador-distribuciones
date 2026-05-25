# subpaginas/bernoulli.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from css.estilos import titulo_rosa, parrafo_adaptable


def intro_bernoulli():
    titulo_rosa("Distribución de Bernoulli")

    parrafo_adaptable(
        "Un experimento de Bernoulli es un proceso estadístico con dos posibles resultados: "
        "<strong>Éxito</strong> (1) o <strong>Fracaso</strong> (0). "
        "Es la base para distribuciones más complejas."
    )


def inicializar_estado():

    if 'p_base' not in st.session_state:
        st.session_state['p_base'] = 0.30

    if 'slider_p' not in st.session_state:
        st.session_state['slider_p'] = st.session_state['p_base']

    if 'input_p' not in st.session_state:
        st.session_state['input_p'] = st.session_state['p_base']


def actualizar_desde_slider():

    st.session_state['p_base'] = st.session_state['slider_p']
    st.session_state['input_p'] = st.session_state['slider_p']


def actualizar_desde_input():

    valor = st.session_state['input_p']

    valor_validado = min(max(valor, 0.0), 1.0)

    st.session_state['p_base'] = valor_validado
    st.session_state['slider_p'] = valor_validado


def generar_grafica(p, q):

    n_muestra = st.session_state.get(
        'tamano_muestra',
        1000
    )

    datos_simulados = np.random.choice(
        [0, 1],
        size=n_muestra,
        p=[q, p]
    )

    exitos = np.sum(datos_simulados == 1)
    fracasos = np.sum(datos_simulados == 0)

    fig, ax = plt.subplots(figsize=(8, 3))

    categorias = ['Fracaso (0)', 'Éxito (1)']
    conteos = [fracasos, exitos]

    ax.bar(
        categorias,
        conteos,
        color=['#31333F', '#FF69B4'],
        width=0.5
    )

    ax.set_ylabel(
        'Frecuencia Absoluta',
        fontsize=11
    )

    ax.set_title(
        f'Resultados para N = {n_muestra}',
        fontsize=13,
        fontweight='bold'
    )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.grid(
        axis='y',
        linestyle='--',
        alpha=0.3
    )

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


def inicializar_bernoulli():

    st.markdown("""
    <style>
    .main .block-container{
        max-width:1100px;
        margin:auto;
    }
    </style>
    """, unsafe_allow_html=True)

    intro_bernoulli()

    st.markdown("---")

    inicializar_estado()

    # ==========================================
    # PARÁMETROS
    # ==========================================

    st.subheader("⚙️ Parámetros de la distribución")

    parrafo_adaptable(
        "Ajusta la probabilidad de éxito (p):"
    )

    st.slider(
        "Probabilidad",
        min_value=0.0,
        max_value=1.0,
        step=0.01,
        key='slider_p',
        on_change=actualizar_desde_slider,
        label_visibility="collapsed"
    )

    col_txt, col_inp = st.columns([2, 1])

    with col_txt:
        st.write("**O ingresa p manualmente:**")

    with col_inp:
        st.number_input(
            "Valor p",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            key='input_p',
            on_change=actualizar_desde_input,
            label_visibility="collapsed"
        )

    p_final = st.session_state['p_base']
    q_final = 1.0 - p_final
    varianza = p_final * q_final

    st.markdown("---")

    # ==========================================
    # RESULTADOS
    # ==========================================

    st.subheader("📊 Resultados")

    col_info, col_grafica = st.columns([1, 2])

    with col_info:

        st.metric(
            "Prob. Fracaso (q)",
            f"{q_final:.4f}"
        )

        st.metric(
            "Esperanza (μ)",
            f"{p_final:.4f}"
        )

        st.metric(
            "Varianza (σ²)",
            f"{varianza:.4f}"
        )

        st.divider()

        st.markdown("#### Interpretación")

        st.write(
            f"Probabilidad de éxito: **{p_final:.2%}**"
        )

        st.write(
            f"Probabilidad de fracaso: **{q_final:.2%}**"
        )

        st.write(
            f"Tamaño de muestra: **{st.session_state['tamano_muestra']}**"
        )

    with col_grafica:

        st.subheader("📈 Simulación Visual")

        generar_grafica(
            p_final,
            q_final
        )