import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import binom
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_binomial():
    titulo_rosa("Distribución Binomial")
    parrafo_adaptable(
        "Modela el número de éxitos al realizar n experimentos independientes de Bernoulli "
        "con una probabilidad fija p de éxito. Es ideal para escenarios de aprobación/reprobación o control de calidad."
    )

def inicializar_estado():
    if 'binomial_p' not in st.session_state:
        st.session_state['binomial_p'] = 0.50
    if 'slider_p_bin' not in st.session_state:
        st.session_state['slider_p_bin'] = st.session_state['binomial_p']
    if 'input_p_bin' not in st.session_state:
        st.session_state['input_p_bin'] = st.session_state['binomial_p']
        
    if 'binomial_n' not in st.session_state:
        st.session_state['binomial_n'] = 10
    if 'slider_n_bin' not in st.session_state:
        st.session_state['slider_n_bin'] = st.session_state['binomial_n']
    if 'input_n_bin' not in st.session_state:
        st.session_state['input_n_bin'] = st.session_state['binomial_n']

    if 'N_binomial_base' not in st.session_state:
        st.session_state['N_binomial_base'] = 1000
    if 'slider_N_global_bin' not in st.session_state:
        st.session_state['slider_N_global_bin'] = st.session_state['N_binomial_base']
    if 'input_N_global_bin' not in st.session_state:
        st.session_state['input_N_global_bin'] = st.session_state['N_binomial_base']

def actualizar_p_desde_slider():
    st.session_state['binomial_p'] = st.session_state['slider_p_bin']
    st.session_state['input_p_bin'] = st.session_state['slider_p_bin']

def actualizar_p_desde_input():
    valor = min(max(float(st.session_state['input_p_bin']), 0.0), 1.0)
    st.session_state['binomial_p'] = valor
    st.session_state['slider_p_bin'] = valor

def actualizar_n_desde_slider():
    st.session_state['binomial_n'] = st.session_state['slider_n_bin']
    st.session_state['input_n_bin'] = st.session_state['slider_n_bin']

def actualizar_n_desde_input():
    valor = min(max(int(st.session_state['input_n_bin']), 1), 1000)
    st.session_state['binomial_n'] = valor
    st.session_state['slider_n_bin'] = valor

def actualizar_N_global_desde_slider():
    st.session_state['N_binomial_base'] = st.session_state['slider_N_global_bin']
    st.session_state['input_N_global_bin'] = st.session_state['slider_N_global_bin']

def actualizar_N_global_desde_input():
    valor = min(max(int(st.session_state['input_N_global_bin']), 5), 100000)
    st.session_state['N_binomial_base'] = valor
    st.session_state['slider_N_global_bin'] = valor

def callback_muestra_aleatoria_binomial():
    p_aleatorio = round(float(np.random.uniform(0.1, 0.9)), 2)
    n_aleatorio = int(np.random.randint(5, 50))
    N_aleatorio = int(np.random.randint(500, 5000))
    
    st.session_state['binomial_p'] = p_aleatorio
    st.session_state['slider_p_bin'] = p_aleatorio
    st.session_state['input_p_bin'] = p_aleatorio

    st.session_state['binomial_n'] = n_aleatorio
    st.session_state['slider_n_bin'] = n_aleatorio
    st.session_state['input_n_bin'] = n_aleatorio

    st.session_state['N_binomial_base'] = N_aleatorio
    st.session_state['slider_N_global_bin'] = N_aleatorio
    st.session_state['input_N_global_bin'] = N_aleatorio

def generar_muestra_datos(n, p, N_global):
    datos_simulados = np.random.binomial(n=n, p=p, size=N_global)
    return datos_simulados

def generar_grafica_seleccionada(n, p, N_global, datos_raw, tipo_grafica):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    
    valores_posibles = np.arange(0, n + 1)
    conteos_simulados = np.bincount(datos_raw, minlength=n+1)
    frecuencias_simuladas = conteos_simulados / N_global
    frecuencias_teoricas = binom.pmf(valores_posibles, n, p)

    ancho_barra = 0.35

    if tipo_grafica == "Muestra Simulada":
        ax.bar(valores_posibles, frecuencias_simuladas, color='#31333F', alpha=0.85, width=0.6, label='Simulado')
        ax.set_ylabel('Frecuencia Relativa', fontsize=11)

    elif tipo_grafica == "Distribucion Teorica":
        ax.bar(valores_posibles, frecuencias_teoricas, color='#E04D98', alpha=0.85, width=0.6, label='Teórico (PMF)')
        ax.set_ylabel('Probabilidad', fontsize=11)

    elif tipo_grafica == "Superponer Ambas":
        ax.bar(valores_posibles - ancho_barra/2, frecuencias_simuladas, width=ancho_barra, color='#31333F', alpha=0.85, label='Simulado')
        ax.bar(valores_posibles + ancho_barra/2, frecuencias_teoricas, width=ancho_barra, color='#FF69B4', alpha=0.85, label='Teórico (PMF)')
        ax.set_ylabel('Proporción / Probabilidad', fontsize=11)

    ax.set_xlabel('Número de Éxitos (X)', fontsize=11)
    ax.set_title(f'Resultados de la Distribución Binomial (n={n}, p={p})', fontsize=11, fontweight='bold')
    ax.set_xticks(valores_posibles)
    if n > 20:
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.legend(loc='upper right', frameon=False)
    
    plt.tight_layout()
    return fig

def renderizar_bloque_visualizacion(n, p, N_global, datos_raw, tipo_grafica):
    st.subheader("Resultados de la Simulacion")
    
    col_izq_sup, col_der_sup = st.columns([1.2, 1.8], gap="large")
    figura = generar_grafica_seleccionada(n, p, N_global, datos_raw, tipo_grafica)

    media_simulada = np.mean(datos_raw)
    var_simulada = np.var(datos_raw, ddof=1)
    desv_simulada = np.sqrt(var_simulada)

    media_teorica = n * p
    var_teorica = n * p * (1 - p)
    desv_teorica = np.sqrt(var_teorica)

    with col_izq_sup:
        if tipo_grafica == "Muestra Simulada":
            st.write("### Indicadores Simulados")
            st.metric("Media Muestral (x̄)", f"{media_simulada:.4f}")
            st.metric("Varianza Muestral (s²)", f"{var_simulada:.4f}")
            st.metric("Desviación Estándar (s)", f"{desv_simulada:.4f}")
            
        elif tipo_grafica == "Distribucion Teorica":
            st.write("### Indicadores Teoricos")
            st.metric("Esperanza Matemática (μ)", f"{media_teorica:.4f}")
            st.metric("Varianza Teórica (σ²)", f"{var_teorica:.4f}")
            st.metric("Desviación Estándar (σ)", f"{desv_teorica:.4f}")
            
        elif tipo_grafica == "Superponer Ambas":
            st.write("### Indicadores Comparados")
            col_t, col_s = st.columns(2)
            with col_t:
                st.caption("Valores Teóricos")
                st.metric("μ (Esperanza)", f"{media_teorica:.2f}")
                st.metric("σ² (Varianza)", f"{var_teorica:.2f}")
            with col_s:
                st.caption("Valores Simulados")
                st.metric("x̄ (Media)", f"{media_simulada:.2f}")
                st.metric("s² (Varianza)", f"{var_simulada:.2f}")

    with col_der_sup:
        st.write("### Simulacion Visual")
        st.pyplot(figura, use_container_width=True)
        
    return media_simulada, var_simulada, desv_simulada

def renderizar_analisis_y_reportes(n, p, N_global, media_simulada, var_simulada, desv_simulada, datos_raw):
    col_izq_inf, col_der_inf = st.columns([1.4, 1.6], gap="large")

    media_teorica = n * p
    var_teorica = n * p * (1 - p)
    desv_teorica = np.sqrt(var_teorica)

    pmf_valores = binom.pmf(datos_raw, n, p)

    with col_izq_inf:
        st.write("### Interpretación y Comparación")
        st.write(f"Ensayos por experimento (n): **{n}**")
        st.write(f"Probabilidad de éxito (p): **{p:.2%}**")
        st.write(f"Número de experimentos simulación (N): **{N_global:,}**")
        
        st.write("**Tabla de Resultados Analizados:**")
        datos_tabla = {
            "Concepto": ["Media", "Varianza", "Desviación estándar", "Total Experimentos"],
            "Valor teórico": [f"{media_teorica:.4f}", f"{var_teorica:.4f}", f"{desv_teorica:.4f}", f"{N_global:,}"],
            "Valor simulado": [f"{media_simulada:.4f}", f"{var_simulada:.4f}", f"{desv_simulada:.4f}", f"{N_global:,}"],
            "Diferencia": [f"{abs(media_teorica - media_simulada):.4f}", f"{abs(var_teorica - var_simulada):.4f}", f"{abs(desv_teorica - desv_simulada):.4f}", "-"]
        }
        df_comparativo = pd.DataFrame(datos_tabla)
        st.dataframe(df_comparativo, hide_index=True, use_container_width=True)

    with col_der_inf:
        st.write("### Herramientas y Reportes")

        with st.expander("Ver Formulas Teoricas"):
            st.latex(r"P(X=x) = \binom{n}{x} p^x (1-p)^{n-x}")
            st.latex(r"\mu = n \cdot p \quad \lhd \quad \sigma^2 = n \cdot p \cdot (1-p)")

        with st.expander("Inspeccionar Muestra Cruda y PMF Teórica"):
            df_inspeccion = pd.DataFrame({
                "Éxitos Obtenidos (X)": datos_raw,
                "PMF Teórica P(X=x)": pmf_valores
            })
            df_inspeccion.index.name = "ID_Experimento"
            st.dataframe(df_inspeccion.head(10), use_container_width=True)
            st.caption(f"Mostrando los primeros 10 experimentos de los {N_global:,} totales junto a su probabilidad exacta.")

        df_descarga = pd.DataFrame({
            "Exitos_Simulados": datos_raw,
            "PMF_Teorica": pmf_valores
        })
        csv_data = df_descarga.to_csv(index=True, index_label="Experimento")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                label="Descargar CSV", data=csv_data, key="dl_csv_bin",
                file_name=f"simulacion_binomial_n{n}_p{p:.2f}.csv", mime="text/csv", use_container_width=True
            )

        with col_btn2:
            reporte_texto = (
                f"REPORTE DE LABORATORIO - DISTRIBUCION BINOMIAL\n"
                f"--------------------------------------------------\n"
                f"Parámetros Base:\n"
                f"Ensayos (n): {n}\n"
                f"Probabilidad de éxito (p): {p:.4f}\n\n"
                f"Concepto                Valor Teorico   Valor Simulado   Diferencia\n"
                f"Media (mu / x-barra):    {media_teorica:.4f}          {media_simulada:.4f}           {abs(media_teorica - media_simulada):.4f}\n"
                f"Varianza (sigma2 / s2):  {var_teorica:.4f}          {var_simulada:.4f}           {abs(var_teorica - var_simulada):.4f}\n"
                f"Desv. Estándar (sigma):  {desv_teorica:.4f}          {desv_simulada:.4f}           {abs(desv_teorica - desv_simulada):.4f}\n"
                f"Total Experimentos (N):  {N_global}            {N_global}             -"
            )
            st.download_button(
                label="Descargar TXT", data=reporte_texto, key="dl_txt_bin",
                file_name=f"reporte_binomial_n{n}_p{p:.2f}.txt", mime="text/plain", use_container_width=True
            )

def renderizar_teorema_limite_central(n, p):
    st.markdown("---")
    st.subheader("Demostración del Teorema del Límite Central (TLC)")
    
    parrafo_adaptable(
        "Al promediar múltiples conjuntos de variables Binomiales independientes, la distribución resultante "
        "comenzará a tomar la forma de una distribución Normal, evidenciando de forma empírica los principios del TLC."
    )
    
    col_ctrl1, col_ctrl2 = st.columns(2, gap="large")
    with col_ctrl1:
        num_muestras = st.slider(
            "Número de experimentos repetidos (m):", 
            min_value=100, max_value=5000, value=2000, step=100, key="tlc_m_bin"
        )
    with col_ctrl2:
        tam_muestra_tlc = st.slider(
            "Tamaño de cada grupo/muestra (k):", 
            min_value=2, max_value=100, value=30, step=1, key="tlc_k_bin"
        )

    matriz_binomial = np.random.binomial(n=n, p=p, size=(num_muestras, tam_muestra_tlc))
    promedios_muestrales = np.mean(matriz_binomial, axis=1)
    
    fig, ax = plt.subplots(figsize=(7, 3.5))
    
    ax.hist(
        promedios_muestrales, bins=25, 
        density=True, color='#E04D98', alpha=0.7, edgecolor='white', label='Promedios Muestrales'
    )
    
    mu_tlc = n * p
    sigma_tlc = np.sqrt((n * p * (1 - p)) / tam_muestra_tlc)
    xmin, xmax = ax.get_xlim()
    x_axis = np.linspace(xmin, xmax, 100)
    curve_teorica = (1 / (sigma_tlc * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_axis - mu_tlc) / sigma_tlc)**2)
    ax.plot(x_axis, curve_teorica, color='#31333F', linewidth=2.5, linestyle='--', label='Tendencia Normal Teórica')
    
    ax.set_title(f"Distribución de {num_muestras:,} Promedios Muestrales (Cada uno con k = {tam_muestra_tlc})", fontsize=10, fontweight='bold')
    ax.set_xlabel("Valor del Promedio Muestral (x̄)", fontsize=9)
    ax.set_ylabel("Densidad de Probabilidad", fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(loc='upper right', frameon=False, fontsize=8)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    
    col_graf, col_info = st.columns([1.8, 1.2], gap="large")
    with col_graf:
        st.pyplot(fig, use_container_width=True)
    with col_info:
        st.write("### Evidencia de Laboratorio")
        st.markdown(f"* **Esperanza del Promedio:** {np.mean(promedios_muestrales):.4f} (Teórico: {mu_tlc:.4f})")
        st.markdown(f"* **Error Estándar:** {np.std(promedios_muestrales):.4f} (Teórico: {sigma_tlc:.4f})")
        st.info("La curva normal se ajusta de manera precisa sobre las frecuencias experimentales, verificando el comportamiento asintótico del teorema.")

def renderizar_controles_parametros():
    st.subheader("Parametros de la distribucion")
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.write("**Probabilidad de éxito (p):**")
        st.slider(
            "Probabilidad slider bin", min_value=0.0, max_value=1.0, step=0.01,
            key='slider_p_bin', on_change=actualizar_p_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Valor p input bin", min_value=0.0, max_value=1.0, step=0.01,
            key='input_p_bin', on_change=actualizar_p_desde_input, label_visibility="collapsed"
        )

    with col2:
        st.write("**Número de ensayos (n):**")
        st.slider(
            "Ensayos slider bin", min_value=1, max_value=100, step=1,
            key='slider_n_bin', on_change=actualizar_n_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Valor n input bin", min_value=1, max_value=100, step=1,
            key='input_n_bin', on_change=actualizar_n_desde_input, label_visibility="collapsed"
        )

    with col3:
        st.write("**Número de experimentos (N):**")
        st.slider(
            "Muestra global slider bin", min_value=5, max_value=100000, step=50,
            key='slider_N_global_bin', on_change=actualizar_N_global_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Valor N input bin", min_value=5, max_value=100000, step=50,
            key='input_N_global_bin', on_change=actualizar_N_global_desde_input, label_visibility="collapsed"
        )
        
    st.button(
        "Generar datos aleatorios de muestra", 
        key="btn_aleatorio_bin",
        use_container_width=True, 
        on_click=callback_muestra_aleatoria_binomial
    )

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
    inicializar_estado()

    renderizar_controles_parametros()
    
    p_teorica = st.session_state['binomial_p']
    n_teorica = st.session_state['binomial_n']
    N_global_final = st.session_state['N_binomial_base']

    st.markdown("---")

    tipo_grafica_seleccionada = st.radio(
        "Selecciona el enfoque visual de la grafica:",
        ["Muestra Simulada", "Distribucion Teorica", "Superponer Ambas"],
        index=0, horizontal=True, key="radio_bin"
    )

    datos_raw = generar_muestra_datos(n_teorica, p_teorica, N_global_final)
    
    media_sim, var_sim, desv_sim = renderizar_bloque_visualizacion(
        n_teorica, p_teorica, N_global_final, datos_raw, tipo_grafica_seleccionada
    )

    st.markdown("##") 
    st.divider()

    renderizar_analisis_y_reportes(
        n_teorica, p_teorica, N_global_final, media_sim, var_sim, desv_sim, datos_raw
    )

    renderizar_teorema_limite_central(n_teorica, p_teorica)