import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import gamma
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_gamma():
    titulo_rosa("Distribución Gamma")
    parrafo_adaptable(
        "La distribución Gamma es una distribución continua con dos parámetros que incluye a las "
        "distribuciones Exponencial y Chi-cuadrada como casos particulares. Se utiliza ampliamente "
        "para modelar variables que son asimétricas a la derecha, como el tiempo de espera hasta "
        "que ocurren <strong>α</strong> eventos independientes en un proceso con tasa constante."
    )

def inicializar_estado_gamma():
    if 'gamma_alpha' not in st.session_state:
        st.session_state['gamma_alpha'] = 2.0
    if 'slider_gamma_alpha' not in st.session_state:
        st.session_state['slider_gamma_alpha'] = st.session_state['gamma_alpha']
    if 'input_gamma_alpha' not in st.session_state:
        st.session_state['input_gamma_alpha'] = st.session_state['gamma_alpha']
        
    if 'gamma_beta' not in st.session_state:
        st.session_state['gamma_beta'] = 2.0
    if 'slider_gamma_beta' not in st.session_state:
        st.session_state['slider_gamma_beta'] = st.session_state['gamma_beta']
    if 'input_gamma_beta' not in st.session_state:
        st.session_state['input_gamma_beta'] = st.session_state['gamma_beta']

    if 'N_gamma_global_base' not in st.session_state:
        st.session_state['N_gamma_global_base'] = 1000
    if 'slider_N_gamma_global' not in st.session_state:
        st.session_state['slider_N_gamma_global'] = st.session_state['N_gamma_global_base']
    if 'input_N_gamma_global' not in st.session_state:
        st.session_state['input_N_gamma_global'] = st.session_state['N_gamma_global_base']

def actualizar_gamma_alpha_desde_slider():
    st.session_state['gamma_alpha'] = st.session_state['slider_gamma_alpha']
    st.session_state['input_gamma_alpha'] = st.session_state['slider_gamma_alpha']

def actualizar_gamma_alpha_desde_input():
    valor = max(float(st.session_state['input_gamma_alpha']), 0.1) # Evitar alpha <= 0
    st.session_state['gamma_alpha'] = valor
    st.session_state['slider_gamma_alpha'] = valor

def actualizar_gamma_beta_desde_slider():
    st.session_state['gamma_beta'] = st.session_state['slider_gamma_beta']
    st.session_state['input_gamma_beta'] = st.session_state['slider_gamma_beta']

def actualizar_gamma_beta_desde_input():
    valor = max(float(st.session_state['input_gamma_beta']), 0.1) # Evitar beta <= 0
    st.session_state['gamma_beta'] = valor
    st.session_state['slider_gamma_beta'] = valor

def actualizar_N_gamma_desde_slider():
    st.session_state['N_gamma_global_base'] = st.session_state['slider_N_gamma_global']
    st.session_state['input_N_gamma_global'] = st.session_state['slider_N_gamma_global']

def actualizar_N_gamma_desde_input():
    valor = min(max(int(st.session_state['input_N_gamma_global']), 5), 100000)
    st.session_state['N_gamma_global_base'] = valor
    st.session_state['slider_N_gamma_global'] = valor

def callback_muestra_aleatoria_gamma():
    alpha_aleatorio = round(float(np.random.uniform(1.0, 9.0)), 1)
    beta_aleatorio = round(float(np.random.uniform(0.5, 5.0)), 1)
    N_global = int(np.random.randint(500, 4000))
    
    st.session_state['gamma_alpha'] = alpha_aleatorio
    st.session_state['slider_gamma_alpha'] = alpha_aleatorio
    st.session_state['input_gamma_alpha'] = alpha_aleatorio

    st.session_state['gamma_beta'] = beta_aleatorio
    st.session_state['slider_gamma_beta'] = beta_aleatorio
    st.session_state['input_gamma_beta'] = beta_aleatorio

    st.session_state['N_gamma_global_base'] = N_global
    st.session_state['slider_N_gamma_global'] = N_global
    st.session_state['input_N_gamma_global'] = N_global

def generar_muestra_datos_gamma(alpha, beta, N_global):
    datos_simulados = np.random.gamma(shape=alpha, scale=beta, size=N_global)
    return datos_simulados

def renderizar_controles_parametros():
    st.subheader("Parámetros de la distribución")
    
    col_alpha, col_beta, col_N = st.columns(3, gap="medium")
    
    with col_alpha:
        st.write("**Forma (alpha / k):**")
        st.slider(
            "Gamma alpha slider", min_value=0.1, max_value=20.0, step=0.1,
            key='slider_gamma_alpha', on_change=actualizar_gamma_alpha_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Gamma alpha input", min_value=0.1, max_value=20.0, step=0.1,
            key='input_gamma_alpha', on_change=actualizar_gamma_alpha_desde_input, label_visibility="collapsed"
        )

    with col_beta:
        st.write("**Escala (beta / theta):**")
        st.slider(
            "Gamma beta slider", min_value=0.1, max_value=20.0, step=0.1,
            key='slider_gamma_beta', on_change=actualizar_gamma_beta_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Gamma beta input", min_value=0.1, max_value=20.0, step=0.1,
            key='input_gamma_beta', on_change=actualizar_gamma_beta_desde_input, label_visibility="collapsed"
        )

    with col_N:
        st.write("**Muestras continuas (N):**")
        st.slider(
            "Gamma Global slider", min_value=10, max_value=50000, step=10,
            key='slider_N_gamma_global', on_change=actualizar_N_gamma_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Gamma Global input", min_value=10, max_value=50000, step=10,
            key='input_N_gamma_global', on_change=actualizar_N_gamma_desde_input, label_visibility="collapsed"
        )
            
    st.button(
        "Generar datos aleatorios de muestra", 
        key="btn_generar_gamma", 
        use_container_width=True, 
        on_click=callback_muestra_aleatoria_gamma
    )

def generar_grafica_gamma(alpha, beta, N_global, datos_raw, tipo_grafica):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    
    max_x = float(np.percentile(datos_raw, 99))
    x_eje = np.linspace(0, max_x, 300)
    
    pdf_teorica = gamma.pdf(x_eje, a=alpha, scale=beta)
    num_bins = 30

    if tipo_grafica == "Muestra Simulada":
        ax.hist(datos_raw, bins=num_bins, range=(0, max_x), color='#31333F', alpha=0.85, edgecolor='white', label='Simulado')
        ax.set_ylabel('Frecuencia Absoluta (Conteos)', fontsize=11)
        
    elif tipo_grafica == "Distribucion Teorica":
        ax.plot(x_eje, pdf_teorica, color='#E04D98', linewidth=3, label='Teorico (PDF)')
        ax.fill_between(x_eje, pdf_teorica, color='#E04D98', alpha=0.2)
        ax.set_ylabel('Densidad de Probabilidad f(x)', fontsize=11)
        
    elif tipo_grafica == "Superponer Ambas":
        ax.hist(datos_raw, bins=num_bins, range=(0, max_x), density=True, color='#31333F', alpha=0.7, edgecolor='white', label='Simulado (Densidad)')
        ax.plot(x_eje, pdf_teorica, color='#FF69B4', linewidth=2.5, label='Teorico (PDF)')
        ax.set_ylabel('Densidad Escalada', fontsize=11)
        ax.legend(loc='upper right', frameon=False)

    ax.set_xlabel('Valor de la Variable Continua (X)', fontsize=11)
    ax.set_title(f'Distribución Gamma (alpha = {alpha}, beta = {beta})', fontsize=11, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    return fig

def renderizar_bloque_visualizacion_gamma(alpha, beta, N_global, datos_raw, tipo_grafica):
    st.subheader("Resultados de la Simulación")
    col_izq, col_der = st.columns([1.2, 1.8], gap="large")
    
    figura = generar_grafica_gamma(alpha, beta, N_global, datos_raw, tipo_grafica)
    
    media_sim = np.mean(datos_raw)
    var_sim = np.var(datos_raw, ddof=1)
    desv_sim = np.sqrt(var_sim)
    
    media_teo = alpha * beta
    var_teo = alpha * (beta ** 2)
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

def renderizar_analisis_y_reportes_gamma(alpha, beta, N_global, media_sim, var_sim, desv_sim, datos_raw):
    col_izq_inf, col_der_inf = st.columns([1.4, 1.6], gap="large")
    
    media_teo = alpha * beta
    var_teo = alpha * (beta ** 2)
    desv_teo = np.sqrt(var_teo)

    # Cálculo matemático explícito de la altura de la PDF teórica individual
    pdf_valores = gamma.pdf(datos_raw, a=alpha, scale=beta)

    with col_izq_inf:
        st.write("### Interpretación y Comparación")
        st.write(f"Forma configurada ($\\alpha$): **{alpha}** | Escala configurada ($\\beta$): **{beta}**")
        
        st.write("**Tabla de Resultados Analizados:**")
        datos_tabla = {
            "Concepto": ["Media (Esperanza)", "Varianza", "Desviación estándar", "Muestras Totales"],
            "Valor teórico": [f"{media_teo:.4f}", f"{var_teo:.4f}", f"{desv_teo:.4f}", f"{N_global:,}"],
            "Valor simulado": [f"{media_sim:.4f}", f"{var_sim:.4f}", f"{desv_sim:.4f}", f"{N_global:,}"],
            "Diferencia": [f"{abs(media_teo - media_sim):.4f}", f"{abs(var_teo - var_sim):.4f}", f"{abs(desv_teo - desv_sim):.4f}", "-"]
        }
        df_comparativo = pd.DataFrame(datos_tabla)
        st.dataframe(df_comparativo, hide_index=True, use_container_width=True)
        
        st.info("**Efecto Teórico:** Observa cómo al cambiar $\\alpha$ a valores grandes, el histograma se vuelve más simétrico y se asemeja paulatinamente a una distribución Normal, cumpliendo con el Teorema Central del Límite.")

    with col_der_inf:
        st.write("### Herramientas y Reportes")
        
        with st.expander("Ver Fórmulas Teóricas Gamma"):
            st.latex(r"f(x) = \frac{1}{\beta^\alpha \Gamma(\alpha)} x^{\alpha-1} e^{-\frac{x}{\beta}} \quad \text{para } x > 0")
            st.latex(r"\mu = \alpha\beta")
            st.latex(r"\sigma^2 = \alpha\beta^2")

        with st.expander("Inspeccionar Muestra Cruda y PDF Teórica"):
            df_inspeccion = pd.DataFrame({
                "Valores Gamma (X)": datos_raw,
                "PDF Teórica f(X)": pdf_valores
            })
            df_inspeccion.index.name = "ID_Muestra"
            st.dataframe(df_inspeccion.head(10), use_container_width=True)
            st.caption("Visualización de los primeros 10 registros numéricos continuos junto a su densidad analítica.")

        df_descarga = pd.DataFrame({
            "Valores_Gamma": datos_raw,
            "PDF_Teorica": pdf_valores
        })
        csv_data = df_descarga.to_csv(index=True, index_label="ID")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                label="Descargar CSV", data=csv_data,
                key="dl_csv_gamma", file_name=f"simulacion_gamma_a{alpha}_b{beta}.csv", mime="text/csv", use_container_width=True
            )
            
        with col_btn2:
            reporte_texto = (
                f"REPORTE DE LABORATORIO - DISTRIBUCION GAMMA\n"
                f"--------------------------------------------------\n"
                f"Configuración: alpha = {alpha} | beta = {beta}\n"
                f"Concepto                Valor Teórico   Valor Simulado   Diferencia\n"
                f"Media (mu):              {media_teo:.4f}          {media_sim:.4f}           {abs(media_teo - media_sim):.4f}\n"
                f"Varianza (sigma2):       {var_teo:.4f}          {var_sim:.4f}           {abs(var_teo - var_sim):.4f}\n"
                f"Desv. Estándar (sigma):  {desv_teo:.4f}          {desv_sim:.4f}           {abs(desv_teo - desv_sim):.4f}\n"
                f"Datos Totales (N):       {N_global}            {N_global}             -"
            )
            st.download_button(
                label="Descargar TXT", data=reporte_texto,
                key="dl_txt_gamma", file_name=f"reporte_gamma_a{alpha}_b{beta}.txt", mime="text/plain", use_container_width=True
            )

def renderizar_tlc_gamma(alpha, beta):
    st.markdown("---")
    st.subheader("Demostración del Teorema del Límite Central (TLC)")
    
    parrafo_adaptable(
        "El TLC postula que la suma o promedio de un conjunto de <strong>k</strong> variables aleatorias "
        "independientes e idénticamente distribuidas (i.i.d.) convergerá hacia una distribución Normal "
        "a medida que el tamaño de agrupación aumente, independientemente de la asimetría original de la función origen."
    )
    
    col_c1, col_c2 = st.columns(2, gap="large")
    with col_c1:
        num_muestras = st.slider(
            "Número de promedios calculados (m):", 
            min_value=100, max_value=5000, value=2000, step=100, key="tlc_gamma_m"
        )
    with col_c2:
        tam_muestra_tlc = st.slider(
            "Tamaño de cada muestra agrupada (k):", 
            min_value=2, max_value=100, value=30, step=1, key="tlc_gamma_k"
        )

    # Generación matricial optimizada (m experimentos de muestras tamaño k)
    matriz_gamma = np.random.gamma(shape=alpha, scale=beta, size=(num_muestras, tam_muestra_tlc))
    promedios_muestrales = np.mean(matriz_gamma, axis=1)
    
    # Renderizado gráfico de los promedios frente a la Campana Gaussiana teórica
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.hist(promedios_muestrales, bins=25, density=True, color='#E04D98', alpha=0.7, edgecolor='white', label='Promedios Muestrales')
    
    # Parámetros esperados según el TLC
    mu_teo_tlc = alpha * beta
    sigma_teo_tlc = (np.sqrt(alpha) * beta) / np.sqrt(tam_muestra_tlc)
    
    xmin, xmax = ax.get_xlim()
    x_axis = np.linspace(xmin, xmax, 100)
    curve_teorica = (1 / (sigma_teo_tlc * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_axis - mu_teo_tlc) / sigma_teo_tlc)**2)
    ax.plot(x_axis, curve_teorica, color='#31333F', linewidth=2.5, linestyle='--', label='Campana Gaussiana Límite')
    
    ax.set_title(f"Distribución de {num_muestras:,} Promedios (Muestras de tamaño k = {tam_muestra_tlc})", fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(loc='upper right', frameon=False, fontsize=8)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    
    col_graf, col_info = st.columns([1.8, 1.2], gap="large")
    with col_graf:
        st.pyplot(fig, use_container_width=True)
    with col_info:
        st.write("### Convergencia Estadística")
        st.markdown(f"* **Media de Promedios:** {np.mean(promedios_muestrales):.4f} (Teórica: {mu_teo_tlc:.4f})")
        st.markdown(f"* **Error Estándar Muestral:** {np.std(promedios_muestrales):.4f} (Teórico: {sigma_teo_tlc:.4f})")
        st.info("💡 Observa cómo incluso si fijas una forma $\\alpha$ pequeña (muy asimétrica), al incrementar **k** en el slider, los promedios se amoldan con asombrosa precisión bajo la campana discontinua.")

def inicializar_gamma():
    st.markdown("""
    <style>
    .main .block-container{
        max-width: 1100px;
        margin: auto;
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    intro_gamma()
    st.markdown("---")
    inicializar_estado_gamma()

    renderizar_controles_parametros()
    
    alpha_val = st.session_state['gamma_alpha']
    beta_val = st.session_state['gamma_beta']
    N_global = st.session_state['N_gamma_global_base']

    st.markdown("---")

    tipo_grafica_seleccionada = st.radio(
        "Selecciona el enfoque visual de la gráfica:",
        ["Muestra Simulada", "Distribucion Teorica", "Superponer Ambas"],
        index=0, horizontal=True, key="radio_gamma"
    )

    datos_raw = generar_muestra_datos_gamma(alpha_val, beta_val, N_global)
    
    media_sim, var_sim, desv_sim = renderizar_bloque_visualizacion_gamma(
        alpha_val, beta_val, N_global, datos_raw, tipo_grafica_seleccionada
    )

    st.markdown("##") 
    st.divider()

    renderizar_analisis_y_reportes_gamma(
        alpha_val, beta_val, N_global, media_sim, var_sim, desv_sim, datos_raw
    )

    # Invocación final interactiva del TLC
    renderizar_tlc_gamma(alpha_val, beta_val)