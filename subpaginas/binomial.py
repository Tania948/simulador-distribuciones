# subpaginas/binomial.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import binom
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_binomial():
    titulo_rosa("Distribución Binomial")
    parrafo_adaptable(
        "La distribución Binomial describe el número de <strong>éxitos</strong> obtenidos al realizar "
        "<strong>n</strong> ensayos independientes de Bernoulli, cada uno con una probabilidad fija "
        "<strong>p</strong> de éxito. Es ideal para modelar conteos acumulados."
    )

def inicializar_estado_binomial():
    # p: Probabilidad de éxito
    if 'p_binom_base' not in st.session_state:
        st.session_state['p_binom_base'] = 0.50
    if 'slider_binom_p' not in st.session_state:
        st.session_state['slider_binom_p'] = st.session_state['p_binom_base']
    if 'input_binom_p' not in st.session_state:
        st.session_state['input_binom_p'] = st.session_state['p_binom_base']
        
    # n: Número de ensayos por experimento
    if 'n_ensayos_base' not in st.session_state:
        st.session_state['n_ensayos_base'] = 10
    if 'slider_n_ensayos' not in st.session_state:
        st.session_state['slider_n_ensayos'] = st.session_state['n_ensayos_base']
    if 'input_n_ensayos' not in st.session_state:
        st.session_state['input_n_ensayos'] = st.session_state['n_ensayos_base']

    # N: Tamaño de muestra global (Repeticiones de la simulación)
    if 'N_global_base' not in st.session_state:
        st.session_state['N_global_base'] = 1000
    if 'slider_N_global' not in st.session_state:
        st.session_state['slider_N_global'] = st.session_state['N_global_base']
    if 'input_N_global' not in st.session_state:
        st.session_state['input_N_global'] = st.session_state['N_global_base']

# --- Callbacks de Sincronización ---
def actualizar_binom_p_desde_slider():
    st.session_state['p_binom_base'] = st.session_state['slider_binom_p']
    st.session_state['input_binom_p'] = st.session_state['slider_binom_p']

def actualizar_binom_p_desde_input():
    valor = st.session_state['input_binom_p']
    valor_validado = min(max(valor, 0.0), 1.0)
    st.session_state['p_binom_base'] = valor_validado
    st.session_state['slider_binom_p'] = valor_validado

def actualizar_ensayos_desde_slider():
    st.session_state['n_ensayos_base'] = st.session_state['slider_n_ensayos']
    st.session_state['input_n_ensayos'] = st.session_state['slider_n_ensayos']

def actualizar_ensayos_desde_input():
    valor = st.session_state['input_n_ensayos']
    valor_validado = min(max(int(valor), 1), 500)
    st.session_state['n_ensayos_base'] = valor_validado
    st.session_state['slider_n_ensayos'] = valor_validado

def actualizar_N_global_desde_slider():
    st.session_state['N_global_base'] = st.session_state['slider_N_global']
    st.session_state['input_N_global'] = st.session_state['slider_N_global']

def actualizar_N_global_desde_input():
    valor = st.session_state['input_N_global']
    valor_validado = min(max(int(valor), 5), 100000)
    st.session_state['N_global_base'] = valor_validado
    st.session_state['slider_N_global'] = valor_validado

def callback_muestra_aleatoria_binomial():
    p_aleatorio = round(float(np.random.uniform(0.1, 0.9)), 2)
    st.session_state['p_binom_base'] = p_aleatorio
    st.session_state['slider_binom_p'] = p_aleatorio
    st.session_state['input_binom_p'] = p_aleatorio
    
    n_aleatorio = int(np.random.randint(5, 51))
    st.session_state['n_ensayos_base'] = n_aleatorio
    st.session_state['slider_n_ensayos'] = n_aleatorio
    st.session_state['input_n_ensayos'] = n_aleatorio

    N_aleatorio = int(np.random.randint(100, 5001))
    st.session_state['N_global_base'] = N_aleatorio
    st.session_state['slider_N_global'] = N_aleatorio
    st.session_state['input_N_global'] = N_aleatorio

def generar_muestra_datos_binomial(n, p, N_global):
    # Genera la simulación Binomial real usando numpy
    datos_simulados = np.random.binomial(n=n, p=p, size=N_global)
    return datos_simulados

def renderizar_controles_parametros():
    st.subheader("Parámetros de la distribución")
    
    col_p, col_n, col_N = st.columns(3, gap="medium")
    
    with col_p:
        st.write("**Probabilidad de éxito (p):**")
        st.slider(
            "Prob slider", min_value=0.0, max_value=1.0, step=0.01,
            key='slider_binom_p', on_change=actualizar_binom_p_desde_slider, label_visibility="collapsed"
        )
        col_t, col_i = st.columns([1.2, 1])
        with col_t: st.caption("O ingresa p manual:")
        with col_i:
            st.number_input(
                "Prob input", min_value=0.0, max_value=1.0, step=0.01,
                key='input_binom_p', on_change=actualizar_binom_p_desde_input, label_visibility="collapsed"
            )

    with col_n:
        st.write("**Número de ensayos (n):**")
        st.slider(
            "Ensayos slider", min_value=1, max_value=100, step=1,
            key='slider_n_ensayos', on_change=actualizar_ensayos_desde_slider, label_visibility="collapsed"
        )
        col_t, col_i = st.columns([1.2, 1])
        with col_t: st.caption("O ingresa n manual:")
        with col_i:
            st.number_input(
                "Ensayos input", min_value=1, max_value=100, step=1,
                key='input_n_ensayos', on_change=actualizar_ensayos_desde_input, label_visibility="collapsed"
            )

    with col_N:
        st.write("**Muestra global (N):**")
        st.slider(
            "Global slider", min_value=5, max_value=50000, step=1,
            key='slider_N_global', on_change=actualizar_N_global_desde_slider, label_visibility="collapsed"
        )
        col_t, col_i = st.columns([1.2, 1])
        with col_t: st.caption("O ingresa N manual:")
        with col_i:
            st.number_input(
                "Global input", min_value=5, max_value=50000, step=1,
                key='input_N_global', on_change=actualizar_N_global_desde_input, label_visibility="collapsed"
            )
            
    st.button(
        "Generar datos aleatorios de muestra",
        key="btn_generar_binomial",  # <--- ¡AÑADE ESTA LÍNEA AQUÍ! 
        use_container_width=True, 
        on_click=callback_muestra_aleatoria_binomial
    )

def generar_grafica_binomial(n, p, N_global, datos_raw, tipo_grafica):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    
    # Rango de valores posibles para el eje X (de 0 a n éxitos)
    x_valores = np.arange(0, n + 1)
    
    # Obtener frecuencias absolutas de la simulación
    valores_sim, conteos_sim = np.unique(datos_raw, return_counts=True)
    frecuencias_simuladas = np.zeros(n + 1)
    for v, c in zip(valores_sim, conteos_sim):
        if v <= n: frecuencias_simuladas[v] = c

    # Obtener frecuencias teóricas calculadas con SciPy PMF
    frecuencias_teoricas = binom.pmf(x_valores, n, p) * N_global

    ancho_barra = 0.35

    if tipo_grafica == "Muestra Simulada":
        ax.bar(x_valores, frecuencias_simuladas, color='#31333F', alpha=0.85, edgecolor='white', label='Simulado')
        ax.set_ylabel('Frecuencia Absoluta (Simulada)', fontsize=11)
        
    elif tipo_grafica == "Distribucion Teorica":
        ax.bar(x_valores, frecuencias_teoricas, color='#E04D98', alpha=0.85, edgecolor='white', label='Teórico')
        ax.set_ylabel('Frecuencia Esperada (Teórica)', fontsize=11)
        
    elif tipo_grafica == "Superponer Ambas":
        ax.bar(x_valores - ancho_barra/2, frecuencias_simuladas, width=ancho_barra, color='#31333F', alpha=0.85, label='Simulado')
        ax.bar(x_valores + ancho_barra/2, frecuencias_teoricas, width=ancho_barra, color='#FF69B4', alpha=0.75, label='Teórico')
        ax.set_ylabel('Frecuencias Comparadas', fontsize=11)
        ax.legend(loc='upper right', frameon=False)

    ax.set_xlabel('Número de éxitos (k)', fontsize=11)
    ax.set_title(f'Distribución Binomial (n = {n}, p = {p}, N = {N_global})', fontsize=11, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    return fig

def renderizar_bloque_visualizacion_binomial(n, p, N_global, datos_raw, tipo_grafica):
    st.subheader("Resultados de la Simulación")
    col_izq, col_der = st.columns([1.2, 1.8], gap="large")
    
    figura = generar_grafica_binomial(n, p, N_global, datos_raw, tipo_grafica)
    
    media_sim = np.mean(datos_raw)
    var_sim = np.var(datos_raw, ddof=1)
    desv_sim = np.sqrt(var_sim)
    
    media_teo = n * p
    var_teo = n * p * (1.0 - p)
    desv_teo = np.sqrt(var_teo)

    with col_izq:
        if tipo_grafica == "Muestra Simulada":
            st.write("### Indicadores Simulados")
            st.metric("Media Muestral (x̄)", f"{media_sim:.4f}")
            st.metric("Varianza Muestral (s²)", f"{var_sim:.4f}")
            st.metric("Desviación Estándar (s)", f"{desv_sim:.4f}")
            
        elif tipo_grafica == "Distribucion Teorica":
            st.write("### Indicadores Teóricos")
            st.metric("Esperanza Matemática (μ)", f"{media_teo:.4f}")
            st.metric("Varianza Teórica (σ²)", f"{var_teo:.4f}")
            st.metric("Desviación Estándar (σ)", f"{desv_teo:.4f}")
            
        elif tipo_grafica == "Superponer Ambas":
            st.write("### Indicadores Comparados")
            col_t, col_s = st.columns(2)
            with col_t:
                st.caption("Valores Teóricos")
                st.metric("μ (Esperanza)", f"{media_teo:.2f}")
                st.metric("σ² (Varianza)", f"{var_teo:.2f}")
            with col_s:
                st.caption("Valores Simulados")
                st.metric("x̄ (Media)", f"{media_sim:.2f}")
                st.metric("s² (Varianza)", f"{var_sim:.2f}")
                
    with col_der:
        st.write("### Simulación Visual")
        st.pyplot(figura, use_container_width=True)
        
    return media_sim, var_sim, desv_sim

def renderizar_analisis_y_reportes_binomial(n, p, N_global, media_sim, var_sim, desv_sim, datos_raw):
    col_izq_inf, col_der_inf = st.columns([1.4, 1.6], gap="large")
    
    media_teo = n * p
    var_teo = n * p * (1.0 - p)
    desv_teo = np.sqrt(var_teo)

    with col_izq_inf:
        st.write("### Interpretación y Comparación")
        st.write(f"Cada experimento consiste en **{n}** ensayos individuales.")
        st.write(f"Probabilidad de éxito en cada ensayo (p): **{p:.2%}**")
        st.write(f"Número total de experimentos simulados (N): **{N_global:,}**")
        
        st.write("**Tabla de Resultados Analizados:**")
        datos_tabla = {
            "Concepto": ["Media", "Varianza", "Desviación estándar", "Experimentos (N)"],
            "Valor teórico": [f"{media_teo:.4f}", f"{var_teo:.4f}", f"{desv_teo:.4f}", f"{N_global:,}"],
            "Valor simulado": [f"{media_sim:.4f}", f"{var_sim:.4f}", f"{desv_sim:.4f}", f"{N_global:,}"],
            "Diferencia": [f"{abs(media_teo - media_sim):.4f}", f"{abs(var_teo - var_sim):.4f}", f"{abs(desv_teo - desv_sim):.4f}", "-"]
        }
        df_comparativo = pd.DataFrame(datos_tabla)
        st.dataframe(df_comparativo, hide_index=True, use_container_width=True)
        
        if N_global >= 5000:
            st.info("🔬 **Nota de Laboratorio:** Observa cómo al incrementar los experimentos globales ($N$), los estadísticos experimentales se acoplan casi perfectamente a las ecuaciones teóricas.")

    with col_der_inf:
        st.write("### Herramientas y Reportes")
        
        with st.expander("Ver Fórmulas Teóricas Binomiales"):
            st.latex(r"\mu = n \cdot p")
            st.latex(r"\sigma^2 = n \cdot p \cdot (1 - p) \quad \lhd \quad \sigma = \sqrt{n \cdot p \cdot (1 - p)}")
            st.latex(r"P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}")

        with st.expander("Inspeccionar Muestra Cruda Generada"):
            df_inspeccion = pd.DataFrame({"Éxitos Obtenidos (X)": datos_raw})
            df_inspeccion.index.name = "ID_Experimento"
            st.dataframe(df_inspeccion.head(10), use_container_width=True)
            st.caption(f"Mostrando los primeros 10 resultados acumulados de los {N_global:,} experimentos.")

        df_descarga = pd.DataFrame(datos_raw, columns=["Exitos_Binomial"])
        csv_data = df_descarga.to_csv(index=True, index_label="Experimento")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                label="Descargar CSV", data=csv_data,
                file_name=f"simulacion_binomial_n{n}_p{p:.2f}.csv", mime="text/csv", use_container_width=True
            )
            
        with col_btn2:
            reporte_texto = (
                f"REPORTE DE LABORATORIO - DISTRIBUCION BINOMIAL\n"
                f"--------------------------------------------------\n"
                f"Parámetros: Ensayos (n) = {n} | Prob. Éxito (p) = {p:.4f}\n"
                f"Concepto                Valor Teórico   Valor Simulado   Diferencia\n"
                f"Media (mu / x-barra):    {media_teo:.4f}          {media_sim:.4f}           {abs(media_teo - media_sim):.4f}\n"
                f"Varianza (sigma2 / s2):  {var_teo:.4f}          {var_sim:.4f}           {abs(var_teo - var_sim):.4f}\n"
                f"Desv. Estándar (sigma):  {desv_teo:.4f}          {desv_sim:.4f}           {abs(desv_teo - desv_sim):.4f}\n"
                f"Experimentos Totales (N): {N_global}            {N_global}             -"
            )
            st.download_button(
                label="Descargar TXT", data=reporte_texto,
                file_name=f"reporte_binomial_n{n}_p{p:.2f}.txt", mime="text/plain", use_container_width=True
            )

def renderizar_tlc_binomial(n_ensayos, p_teorica):
    """Demostración del TLC: Tomando muestras de la distribución Binomial."""
    st.markdown("---")
    st.subheader("Demostración del Teorema del Límite Central (TLC)")
    
    parrafo_adaptable(
        "Incluso si la Binomial es inherentemente discreta y asimétrica (cuando p está cerca de 0 o 1), "
        "el promedio de múltiples variables Binomiales independientes convergerá hacia una distribución Normal continua."
    )
    
    col_c1, col_c2 = st.columns(2, gap="large")
    with col_c1:
        num_muestras = st.slider(
            "Número de promedios calculados (m):", 
            min_value=100, max_value=5000, value=2000, step=100, key="tlc_binom_m"
        )
    with col_c2:
        tam_muestra_tlc = st.slider(
            "Tamaño de cada muestra agrupada (k):", 
            min_value=2, max_value=100, value=30, step=1, key="tlc_binom_k"
        )

    # Simulación del TLC con Binomial
    matriz_binom = np.random.binomial(n=n_ensayos, p=p_teorica, size=(num_muestras, tam_muestra_tlc))
    promedios_muestrales = np.mean(matriz_binom, axis=1)
    
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.hist(promedios_muestrales, bins=25, density=True, color='#E04D98', alpha=0.7, edgecolor='white', label='Promedios Muestrales')
    
    # Curva teórica normal del TLC
    mu_tlc = n_ensayos * p_teorica
    sigma_tlc = np.sqrt(n_ensayos * p_teorica * (1.0 - p_teorica)) / np.sqrt(tam_muestra_tlc)
    
    xmin, xmax = ax.get_xlim()
    x_axis = np.linspace(xmin, xmax, 100)
    curve_teorica = (1 / (sigma_tlc * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_axis - mu_tlc) / sigma_tlc)**2)
    ax.plot(x_axis, curve_teorica, color='#31333F', linewidth=2.5, linestyle='--', label='Tendencia Normal Teórica')
    
    ax.set_title(f"Distribución de {num_muestras:,} Promedios Muestrales (Cada uno con k = {tam_muestra_tlc})", fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(loc='upper right', frameon=False, fontsize=8)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    
    col_graf, col_info = st.columns([1.8, 1.2], gap="large")
    with col_graf:
        st.pyplot(fig, use_container_width=True)
    with col_info:
        st.write("### Evidencia de TLC")
        st.markdown(f"* **Media Esperada:** {np.mean(promedios_muestrales):.4f} (Teórica: {mu_tlc:.4f})")
        st.markdown(f"* **Error Estándar Muestral:** {np.std(promedios_muestrales):.4f} (Teórico: {sigma_tlc:.4f})")
        st.info("La aproximación de la curva normal sobre el histograma valida la convergencia asintótica del teorema.")

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

    renderizar_controles_parametros()
    
    p_teorica = st.session_state['p_binom_base']
    n_ensayos = st.session_state['n_ensayos_base']
    N_global = st.session_state['N_global_base']

    st.markdown("---")

    tipo_grafica_seleccionada = st.radio(
        "Selecciona el enfoque visual de la gráfica:",
        ["Muestra Simulada", "Distribucion Teorica", "Superponer Ambas"],
        index=0, horizontal=True, key="radio_binom"
    )

    datos_raw = generar_muestra_datos_binomial(n_ensayos, p_teorica, N_global)
    
    media_sim, var_sim, desv_sim = renderizar_bloque_visualizacion_binomial(
        n_ensayos, p_teorica, N_global, datos_raw, tipo_grafica_seleccionada
    )

    st.markdown("##") 
    st.divider()

    renderizar_analisis_y_reportes_binomial(
        n_ensayos, p_teorica, N_global, media_sim, var_sim, desv_sim, datos_raw
    )

    renderizar_tlc_binomial(n_ensayos, p_teorica)