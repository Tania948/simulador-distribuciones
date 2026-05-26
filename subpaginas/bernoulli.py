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
    # Inicialización para la probabilidad p
    if 'p_base' not in st.session_state:
        st.session_state['p_base'] = 0.30
    if 'slider_p' not in st.session_state:
        st.session_state['slider_p'] = st.session_state['p_base']
    if 'input_p' not in st.session_state:
        st.session_state['input_p'] = st.session_state['p_base']
        
    # Inicialización para el tamaño de muestra N
    if 'n_base' not in st.session_state:
        st.session_state['n_base'] = 1000
    if 'slider_n' not in st.session_state:
        st.session_state['slider_n'] = st.session_state['n_base']
    if 'input_n' not in st.session_state:
        st.session_state['input_n'] = st.session_state['n_base']

def actualizar_p_desde_slider():
    st.session_state['p_base'] = st.session_state['slider_p']
    st.session_state['input_p'] = st.session_state['slider_p']

def actualizar_p_desde_input():
    valor = st.session_state['input_p']
    valor_validado = min(max(valor, 0.0), 1.0)
    st.session_state['p_base'] = valor_validado
    st.session_state['slider_p'] = valor_validado

def actualizar_n_desde_slider():
    st.session_state['n_base'] = st.session_state['slider_n']
    st.session_state['input_n'] = st.session_state['slider_n']

def actualizar_n_desde_input():
    valor = st.session_state['input_n']
    valor_validado = min(max(int(valor), 10), 100000)
    st.session_state['n_base'] = valor_validado
    st.session_state['slider_n'] = valor_validado

def generar_muestra_datos(p, q, n_muestra):
    """Genera la muestra simulada y computa las frecuencias absolutas."""
    datos_simulados = np.random.choice([0, 1], size=n_muestra, p=[q, p])
    exitos = np.sum(datos_simulados == 1)
    fracasos = np.sum(datos_simulados == 0)
    return datos_simulados, exitos, fracasos

def generar_grafica_seleccionada(p, q, n_muestra, exitos, fracasos, tipo_grafica):
    """Genera la figura de Matplotlib usando únicamente barras paralelas estilo pilita."""
    fig, ax = plt.subplots(figsize=(7, 4.2))
    categorias = ['Fracaso (0)', 'Éxito (1)']
    
    conteos_simulados = [fracasos, exitos]
    conteos_teoricos = [q * n_muestra, p * n_muestra]
    
    x = np.arange(len(categorias))
    ancho_barra = 0.35

    if tipo_grafica == "Muestra Simulada":
        barras = ax.bar(x, conteos_simulados, color=['#31333F', '#FF69B4'], width=0.45, alpha=0.85)
        for barra in barras:
            altura = barra.get_height()
            porcentaje = (altura / n_muestra) * 100
            ax.annotate(f'{altura:,}\n({porcentaje:.1f}%)',
                        xy=(barra.get_x() + barra.get_width() / 2, altura),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
        ax.set_ylabel('Frecuencia Absoluta (Simulada)', fontsize=11)
        ax.set_ylim(0, max(conteos_simulados) * 1.15)

    elif tipo_grafica == "Distribucion Teorica":
        barras = ax.bar(x, conteos_teoricos, color=['#555555', '#E04D98'], width=0.45, alpha=0.85)
        for barra in barras:
            altura = barra.get_height()
            porcentaje = (altura / n_muestra) * 100
            ax.annotate(f'{altura:,.1f}\n({porcentaje:.1f}%)',
                        xy=(barra.get_x() + barra.get_width() / 2, altura),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
        ax.set_ylabel('Frecuencia Esperada (Teorica)', fontsize=11)
        ax.set_ylim(0, max(conteos_teoricos) * 1.15)

    elif tipo_grafica == "Superponer Ambas":
        # Barras en paralelo una al lado de la otra
        barras_sim = ax.bar(x - ancho_barra/2, conteos_simulados, width=ancho_barra, color='#31333F', alpha=0.85, label='Simulado')
        barras_teo = ax.bar(x + ancho_barra/2, conteos_teoricos, width=ancho_barra, color='#FF69B4', alpha=0.85, label='Teorico')
        
        # Colocar etiquetas en las pilitas de simulación
        for barra in barras_sim:
            altura = barra.get_height()
            ax.annotate(f'{altura:,}', xy=(barra.get_x() + barra.get_width() / 2, altura),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)
            
        # Colocar etiquetas en las pilitas de teoría
        for barra in barras_teo:
            altura = barra.get_height()
            ax.annotate(f'{altura:,.0f}', xy=(barra.get_x() + barra.get_width() / 2, altura),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)
            
        ax.set_ylabel('Frecuencias Comparadas', fontsize=11)
        ax.set_ylim(0, max(max(conteos_simulados), max(conteos_teoricos)) * 1.2)
        ax.legend(loc='upper center', frameon=False, ncol=2)

    ax.set_xticks(x)
    ax.set_xticklabels(categorias)
    ax.set_title(f'Resultados de la Distribucion (N = {n_muestra})', fontsize=11, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    return fig

def inicializar_bernoulli():
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
    # SECCIÓN 1: PARÁMETROS DE CONFIGURACIÓN
    # ==========================================
    st.subheader("Parametros de la distribucion")
    
    col_izq_p, col_der_n = st.columns(2, gap="large")
    
    with col_izq_p:
        st.write("**Probabilidad de exito (p):**")
        st.slider(
            "Probabilidad slider",
            min_value=0.0, max_value=1.0, step=0.01,
            key='slider_p',
            on_change=actualizar_p_desde_slider,
            label_visibility="collapsed"
        )
        col_txt_p, col_inp_p = st.columns([1.5, 1])
        with col_txt_p:
            st.write("O ingresa p manual:")
        with col_inp_p:
            st.number_input(
                "Valor p input",
                min_value=0.0, max_value=1.0, step=0.01,
                key='input_p',
                on_change=actualizar_p_desde_input,
                label_visibility="collapsed"
            )

    with col_der_n:
        st.write("**Tamaño de muestra global (N):**")
        st.slider(
            "Muestra slider",
            min_value=10, max_value=100000, step=10,
            key='slider_n',
            on_change=actualizar_n_desde_slider,
            label_visibility="collapsed"
        )
        col_txt_n, col_inp_n = st.columns([1.5, 1])
        with col_txt_n:
            st.write("O ingresa N manual:")
        with col_inp_n:
            st.number_input(
                "Valor N input",
                min_value=10, max_value=100000, step=10,
                key='input_n',
                on_change=actualizar_n_desde_input,
                label_visibility="collapsed"
            )
        
        if st.button("Generar datos aleatorios de muestra", use_container_width=True):
            n_aleatorio = int(np.random.randint(100, 10001))
            st.session_state['n_base'] = n_aleatorio
            st.session_state['slider_n'] = n_aleatorio
            st.session_state['input_n'] = n_aleatorio
            st.rerun()

    p_final = st.session_state['p_base']
    q_final = 1.0 - p_final
    varianza = p_final * q_final
    n_muestra_final = st.session_state['n_base']

    st.markdown("---")

    # ==========================================
    # SECCIÓN 2: SIMULACIÓN Y ENFOQUES VISUALES
    # ==========================================
    st.subheader("Resultados de la Simulacion")
    
    tipo_grafica_seleccionada = st.radio(
        "Selecciona el enfoque visual de la grafica:",
        ["Muestra Simulada", "Distribucion Teorica", "Superponer Ambas"],
        index=0,
        horizontal=True
    )

    col_izq_sup, col_der_sup = st.columns([1.1, 1.9], gap="large")
    
    datos_raw, exitos_sim, fracasos_sim = generar_muestra_datos(p_final, q_final, n_muestra_final)
    figura = generar_grafica_seleccionada(p_final, q_final, n_muestra_final, exitos_sim, fracasos_sim, tipo_grafica_seleccionada)

    p_simulada = exitos_sim / n_muestra_final
    q_simulada = fracasos_sim / n_muestra_final

    dif_p = abs(p_final - p_simulada)
    dif_q = abs(q_final - q_simulada)

    with col_izq_sup:
        st.write("### Indicadores Teoricos")
        st.metric("Prob. Fracaso (q)", f"{q_final:.4f}")
        st.metric("Esperanza (mu)", f"{p_final:.4f}")
        st.metric("Varianza (sigma2)", f"{varianza:.4f}")

    with col_der_sup:
        st.write("### Simulacion Visual")
        st.pyplot(figura, use_container_width=True)

    st.markdown("##") 
    st.divider()

    # Fila inferior: Métricas y Descarga de reportes
    col_izq_inf, col_der_inf = st.columns([1.3, 1.7], gap="large")

    with col_izq_inf:
        st.write("### Interpretación y Comparación")
        st.write(f"Probabilidad de exito (p): **{p_final:.2%}**")
        st.write(f"Probabilidad de fracaso (q): **{q_final:.2%}**")
        st.write(f"Tamaño de muestra activo (N): **{n_muestra_final:,}**")
        
        st.write("**Tabla Comparativa e Historial de Diferencias:**")
        datos_tabla = {
            "Metrica": ["Exito (p)", "Fracaso (q)"],
            "Valor Teorico": [f"{p_final:.4f}", f"{q_final:.4f}"],
            "Valor Simulado": [f"{p_simulada:.4f}", f"{q_simulada:.4f}"],
            "Diferencia Absoluta": [f"{dif_p:.4f}", f"{dif_q:.4f}"]
        }
        df_comparativo = pd.DataFrame(datos_tabla)
        st.dataframe(df_comparativo, hide_index=True, use_container_width=True)

    with col_der_inf:
        st.write("### Herramientas y Reportes")

        with st.expander("Ver Formulas Teoricas"):
            st.latex(r"p + q = 1 \quad \lhd \quad \mu = p")
            st.latex(r"\sigma^2 = p \cdot q \quad \lhd \quad P(X = x) = p^x q^{1-x}")

        df_descarga = pd.DataFrame(datos_raw, columns=["Resultado_Simulacion"])
        csv_data = df_descarga.to_csv(index=True, index_label="Iteracion")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                label="Descargar CSV",
                data=csv_data,
                file_name=f"simulacion_bernoulli_{p_final:.2f}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col_btn2:
            reporte_texto = (
                f"REPORTE DE LABORATORIO - DISTRIBUCION DE BERNOULLI\n"
                f"--------------------------------------------------\n"
                f"Probabilidad de Exito Teorica (p): {p_final:.4f}\n"
                f"Probabilidad de Fracaso Teorica (q): {q_final:.4f}\n"
                f"Esperanza Matematica (mu): {p_final:.4f}\n"
                f"Varianza Teorica (sigma2): {varianza:.4f}\n\n"
                f"RESULTADOS Y DESVIACIONES DE LA SIMULACION (N = {n_muestra_final})\n"
                f"--------------------------------------------------\n"
                f"Frecuencia Absoluta Exitos: {exitos_sim}\n"
                f"Frecuencia Absoluta Fracasos: {fracasos_sim}\n"
                f"Proporcion de Exitos Simulada: {p_simulada:.4f} (Diferencia: {dif_p:.4f})\n"
                f"Proporcion de Fracasos Simulada: {q_simulada:.4f} (Diferencia: {dif_q:.4f})"
            )
            st.download_button(
                label="Descargar TXT",
                data=reporte_texto,
                file_name=f"reporte_bernoulli_{p_final:.2f}.txt",
                mime="text/plain",
                use_container_width=True
            )