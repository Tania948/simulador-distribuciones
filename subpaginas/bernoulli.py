# subpaginas/bernoulli.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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

def generar_grafica(p, q, n_muestra):
    """Genera la muestra simulada y retorna la figura de Matplotlib y los datos."""
    datos_simulados = np.random.choice([0, 1], size=n_muestra, p=[q, p])
    exitos = np.sum(datos_simulados == 1)
    fracasos = np.sum(datos_simulados == 0)

    # Ajustamos el tamaño para que cuadre perfecto con la columna lateral
    fig, ax = plt.subplots(figsize=(7, 4.2))
    categorias = ['Fracaso (0)', 'Éxito (1)']
    conteos = [fracasos, exitos]

    ax.bar(categorias, conteos, color=['#31333F', '#FF69B4'], width=0.45)
    ax.set_ylabel('Frecuencia Absoluta', fontsize=11)
    ax.set_title(f'Resultados de la Simulación (N = {n_muestra})', fontsize=12, fontweight='bold')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    plt.tight_layout()
    return fig, datos_simulados

def inicializar_bernoulli():
    # Fijamos el contenedor para pantallas de escritorio (Adiós dolores de cabeza)
    st.markdown("""
    <style>
    .main .block-container{
        max-width: 1100px;
        margin: auto;
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    intro_bernoulli()
    st.markdown("---")
    inicializar_estado()

    # ==========================================
    # SECCIÓN 1: PARÁMETROS
    # ==========================================
    st.subheader("⚙️ Parámetros de la distribución")
    parrafo_adaptable("Ajusta la probabilidad de éxito (p):")

    st.slider(
        "Probabilidad",
        min_value=0.0, max_value=1.0, step=0.01,
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
            min_value=0.0, max_value=1.0, step=0.01,
            key='input_p',
            on_change=actualizar_desde_input,
            label_visibility="collapsed"
        )

    p_final = st.session_state['p_base']
    q_final = 1.0 - p_final
    varianza = p_final * q_final
    n_muestra = st.session_state.get('tamano_muestra', 1000)

    st.markdown("---")

    # ==========================================
    # SECCIÓN 2: RESULTADOS Y SIMULACIÓN
    # ==========================================
    st.subheader("📊 Resultados de la Simulación")

    # Fila superior: Indicadores y Gráfica en dos columnas limpias
    col_izq_sup, col_der_sup = st.columns([1.1, 1.9], gap="large")
    figura, datos_raw = generar_grafica(p_final, q_final, n_muestra)

    with col_izq_sup:
        st.write("### 📐 Indicadores Teóricos")
        st.metric("Prob. Fracaso (q)", f"{q_final:.4f}")
        st.metric("Esperanza (μ)", f"{p_final:.4f}")
        st.metric("Varianza (σ²)", f"{varianza:.4f}")

    with col_der_sup:
        st.write("### 📈 Simulación Visual")
        st.pyplot(figura, use_container_width=True)

    st.markdown("##") # Pequeño espaciador sutil para separar las filas
    st.divider()

    # Fila inferior: Interpretación (Izquierda) y Herramientas/Descargas (Derecha)
    col_izq_inf, col_der_inf = st.columns([1.3, 1.7], gap="large")

    with col_izq_inf:
        st.write("### 📋 Interpretación")
        st.write(f"Probabilidad de éxito ($p$): **{p_final:.2%}**")
        st.write(f"Probabilidad de fracaso ($q$): **{q_final:.2%}**")
        st.write(f"Tamaño de muestra activo ($N$): **{n_muestra:,}**")

    with col_der_inf:
        st.write("### 🛠️ Herramientas y Reportes")

        # Fórmulas teóricas compactas
        with st.expander("📐 Ver Fórmulas Teóricas"):
            st.latex(r"p + q = 1 \quad \lhd \quad \mu = p")
            st.latex(r"\sigma^2 = p \cdot q \quad \lhd \quad P(X = x) = p^x q^{1-x}")

        # Preparación de datos para la descarga de CSV
        df_descarga = pd.DataFrame(datos_raw, columns=["Resultado_Simulacion"])
        csv_data = df_descarga.to_csv(index=True, index_label="Iteracion")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                label="📥 Descargar CSV",
                data=csv_data,
                file_name=f"simulacion_bernoulli_{p_final:.2f}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col_btn2:
            reporte_texto = f"Reporte Bernoulli\np: {p_final:.4f}\nq: {q_final:.4f}\nmu: {p_final:.4f}\nsigma2: {varianza:.4f}\nN: {n_muestra}"
            st.download_button(
                label="📄 Descargar PDF (TXT)",
                data=reporte_texto,
                file_name=f"reporte_bernoulli_{p_final:.2f}.txt",
                mime="text/plain",
                use_container_width=True
            )