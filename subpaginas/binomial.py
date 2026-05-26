# subpaginas/binomial.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_binomial():
    titulo_rosa("Distribución Binomial")
    parrafo_adaptable(
        "La distribución binomial describe el número de éxitos al realizar "
        "<strong>n</strong> experimentos de Bernoulli independientes entre sí, "
        "cada uno con una probabilidad fija <strong>p</strong> de ocurrencia."
    )

def inicializar_estado_binomial():
    if 'binom_p' not in st.session_state:
        st.session_state['binom_p'] = 0.50
    if 'slider_binom_p' not in st.session_state:
        st.session_state['slider_binom_p'] = st.session_state['binom_p']
    if 'input_binom_p' not in st.session_state:
        st.session_state['input_binom_p'] = st.session_state['binom_p']
        
    if 'binom_n' not in st.session_state:
        st.session_state['binom_n'] = 10
    if 'slider_binom_n' not in st.session_state:
        st.session_state['slider_binom_n'] = st.session_state['binom_n']
    if 'input_binom_n' not in st.session_state:
        st.session_state['input_binom_n'] = st.session_state['binom_n']

def actualizar_p_desde_slider():
    st.session_state['binom_p'] = st.session_state['slider_binom_p']
    st.session_state['input_binom_p'] = st.session_state['slider_binom_p']

def actualizar_p_desde_input():
    valor = st.session_state['input_binom_p']
    valor_validado = min(max(valor, 0.0), 1.0)
    st.session_state['binom_p'] = valor_validado
    st.session_state['slider_binom_p'] = valor_validado

def actualizar_n_desde_slider():
    st.session_state['binom_n'] = st.session_state['slider_binom_n']
    st.session_state['input_binom_n'] = st.session_state['slider_binom_n']

def actualizar_n_desde_input():
    valor = st.session_state['input_binom_n']
    valor_validado = min(max(int(valor), 1), 100)
    st.session_state['binom_n'] = valor_validado
    st.session_state['slider_binom_n'] = valor_validado

def generar_grafica_binomial(n, p, n_muestra):
    """Genera la muestra simulada binomial y retorna la figura, los datos y estadísticos."""
    datos_simulados = np.random.binomial(n=n, p=p, size=n_muestra)
    valores, conteos = np.unique(datos_simulados, return_counts=True)
    
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.bar(valores, conteos, color='#FF69B4', edgecolor='#31333F', alpha=0.85, width=0.6)
    
    ax.set_xlabel('Numero de Exitos (k)', fontsize=10)
    ax.set_ylabel('Frecuencia Absoluta', fontsize=11)
    ax.set_title(f'Resultados de la Simulacion (N = {n_muestra})', fontsize=12, fontweight='bold')
    
    ax.set_xticks(np.arange(0, n + 1, max(1, n // 10)))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    
    # Calculamos la media y varianza reales obtenidas en la simulación
    media_simulada = float(np.mean(datos_simulados))
    varianza_simulada = float(np.var(datos_simulados))
    
    return fig, datos_simulados, media_simulada, varianza_simulada

def inicializar_binomial():
    st.markdown("""
    <style>
    .main .block-container{
        max-width: 1100px;
        margin: auto;
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    intro_binomial()
    st.markdown("---")
    inicializar_estado_binomial()

    # ==========================================
    # SECCIÓN 1: PARÁMETROS
    # ==========================================
    st.subheader("Parametros de la distribucion")
    
    col_p, col_n = st.columns(2, gap="large")
    
    with col_p:
        st.write("**Probabilidad de exito (p):**")
        st.slider(
            "Probabilidad p", min_value=0.0, max_value=1.0, step=0.01,
            key='slider_binom_p', on_change=actualizar_p_desde_slider, label_visibility="collapsed"
        )
        col_txt_p, col_inp_p = st.columns([1.5, 1])
        with col_txt_p:
            st.write("Ingresar p manual:")
        with col_inp_p:
            st.number_input(
                "Valor p manual", min_value=0.0, max_value=1.0, step=0.01,
                key='input_binom_p', on_change=actualizar_p_desde_input, label_visibility="collapsed"
            )

    with col_n:
        st.write("**Numero de ensayos (n):**")
        st.slider(
            "Ensayos n", min_value=1, max_value=100, step=1,
            key='slider_binom_n', on_change=actualizar_n_desde_slider, label_visibility="collapsed"
        )
        col_txt_n, col_inp_n = st.columns([1.5, 1])
        with col_txt_n:
            st.write("Ingresar n manual:")
        with col_inp_n:
            st.number_input(
                "Valor n manual", min_value=1, max_value=100, step=1,
                key='input_binom_n', on_change=actualizar_n_desde_input, label_visibility="collapsed"
            )

    p_final = st.session_state['binom_p']
    n_final = st.session_state['binom_n']
    q_final = 1.0 - p_final
    
    esperanza_teorica = n_final * p_final
    varianza_teorica = n_final * p_final * q_final
    n_muestra = st.session_state.get('tamano_muestra', 1000)

    st.markdown("---")

    # ==========================================
    # SECCIÓN 2: RESULTADOS Y SIMULACIÓN
    # ==========================================
    st.subheader("Resultados de la Simulacion")

    col_izq_sup, col_der_sup = st.columns([1.1, 1.9], gap="large")
    figura, datos_raw, media_sim, varianza_sim = generar_grafica_binomial(n_final, p_final, n_muestra)

    with col_izq_sup:
        st.write("### Indicadores Teoricos")
        st.metric("Prob. Fracaso (q)", f"{q_final:.4f}")
        st.metric("Esperanza (mu)", f"{esperanza_teorica:.4f}")
        st.metric("Varianza (sigma2)", f"{varianza_teorica:.4f}")

    with col_der_sup:
        st.write("### Simulacion Visual")
        st.pyplot(figura, use_container_width=True)

    st.markdown("##") 
    st.divider()

    # Fila inferior: Interpretación y Comparativa vs Herramientas
    col_izq_inf, col_der_inf = st.columns([1.3, 1.7], gap="large")

    with col_izq_inf:
        st.write("### Interpretacion y Comparacion")
        st.write(f"En cada uno de los **{n_final}** ensayos individuales:")
        st.write(f"- Probabilidad de exito (p): **{p_final:.2%}**")
        st.write(f"- Probabilidad de fracaso (q): **{q_final:.2%}**")
        st.write(f"Tamaño de muestra simulada (N): **{n_muestra:,}**")
        
        st.write("**Tabla Comparativa (Estadisticos):**")
        datos_tabla = {
            "Metrica": ["Esperanza (mu)", "Varianza (sigma2)"],
            "Valor Teorico": [f"{esperanza_teorica:.4f}", f"{varianza_teorica:.4f}"],
            "Valor Simulado": [f"{media_sim:.4f}", f"{varianza_sim:.4f}"]
        }
        df_comparativo = pd.DataFrame(datos_tabla)
        st.dataframe(df_comparativo, hide_index=True, use_container_width=True)

    with col_der_inf:
        st.write("### Herramientas y Reportes")

        with st.expander("Ver Formulas Teoricas"):
            st.latex(r"\mu = n \cdot p \quad \lhd \quad \sigma^2 = n \cdot p \cdot q")
            st.latex(r"P(X = k) = \binom{n}{k} p^k q^{n-k}")

        df_descarga = pd.DataFrame(datos_raw, columns=["Exitos_por_Iteracion"])
        csv_data = df_descarga.to_csv(index=True, index_label="Iteracion")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                label="Descargar CSV",
                data=csv_data,
                file_name=f"simulacion_binomial_n_{n_final}_p_{p_final:.2f}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col_btn2:
            reporte_texto = (
                f"REPORTE DE LABORATORIO - DISTRIBUCION BINOMIAL\n"
                f"--------------------------------------------------\n"
                f"Numero de Ensayos (n): {n_final}\n"
                f"Probabilidad de Exito Teorica (p): {p_final:.4f}\n"
                f"Probabilidad de Fracaso Teorica (q): {q_final:.4f}\n\n"
                f"COMPARATIVA DE ESTADISTICOS (N = {n_muestra})\n"
                f"--------------------------------------------------\n"
                f"Esperanza Teorica (mu): {esperanza_teorica:.4f}\n"
                f"Media Simulada Obtenida: {media_sim:.4f}\n"
                f"Varianza Teorica (sigma2): {varianza_teorica:.4f}\n"
                f"Varianza Simulada Obtenida: {varianza_sim:.4f}"
            )
            st.download_button(
                label="Descargar TXT",
                data=reporte_texto,
                file_name=f"reporte_binomial_{n_final}_{p_final:.2f}.txt",
                mime="text/plain",
                use_container_width=True
            )