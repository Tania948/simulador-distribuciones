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

    fig, ax = plt.subplots(figsize=(4, 3))

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

    fig, ax = plt.subplots(figsize=(8, 3.5))

    categorias = ['Fracaso (0)', 'Éxito (1)']
    conteos = [fracasos, exitos]

    ax.bar(
        categorias,
        conteos,
        color=['#31333F', '#FF69B4']
    )

    ax.set_ylabel('Frecuencia')

    ax.set_title(
        f'Resultados para N = {n_muestra}'
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