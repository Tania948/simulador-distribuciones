# subpaginas/normal.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_normal():
    titulo_rosa("Distribución Normal o Gaussiana")
    parrafo_adaptable(
        "La distribución Normal es la más importante de la probabilidad y la estadística. "
        "Modela fenómenos naturales, sociales y técnicos donde la mayoría de los datos se agrupan "
        "en torno a un valor central conocido como <strong>media (μ)</strong>, disminuyendo de forma simétrica "
        "a medida que nos alejamos de él, dibujando la famosa <strong>Campana de Gauss</strong>."
    )

def inicializar_estado_normal():
    if 'normal_mu' not in st.session_state:
        st.session_state['normal_mu'] = 0.0
    if 'slider_normal_mu' not in st.session_state:
        st.session_state['slider_normal_mu'] = st.session_state['normal_mu']
    if 'input_normal_mu' not in st.session_state:
        st.session_state['input_normal_mu'] = st.session_state['normal_mu']
        
    if 'normal_sigma' not in st.session_state:
        st.session_state['normal_sigma'] = 1.0
    if 'slider_normal_sigma' not in st.session_state:
        st.session_state['slider_normal_sigma'] = st.session_state['normal_sigma']
    if 'input_normal_sigma' not in st.session_state:
        st.session_state['input_normal_sigma'] = st.session_state['normal_sigma']

    if 'N_normal_global_base' not in st.session_state:
        st.session_state['N_normal_global_base'] = 1000
    if 'slider_N_normal_global' not in st.session_state:
        st.session_state['slider_N_normal_global'] = st.session_state['N_normal_global_base']
    if 'input_N_normal_global' not in st.session_state:
        st.session_state['input_N_normal_global'] = st.session_state['N_normal_global_base']

def actualizar_normal_mu_desde_slider():
    st.session_state['normal_mu'] = st.session_state['slider_normal_mu']
    st.session_state['input_normal_mu'] = st.session_state['slider_normal_mu']

def actualizar_normal_mu_desde_input():
    st.session_state['normal_mu'] = float(st.session_state['input_normal_mu'])
    st.session_state['slider_normal_mu'] = float(st.session_state['input_normal_mu'])

def actualizar_normal_sigma_desde_slider():
    st.session_state['normal_sigma'] = st.session_state['slider_normal_sigma']
    st.session_state['input_normal_sigma'] = st.session_state['slider_normal_sigma']

def actualizar_normal_sigma_desde_input():
    valor = max(float(st.session_state['input_normal_sigma']), 0.1) # Evitar sigma = 0
    st.session_state['normal_sigma'] = valor
    st.session_state['slider_normal_sigma'] = valor

def actualizar_N_normal_desde_slider():
    st.session_state['N_normal_global_base'] = st.session_state['slider_N_normal_global']
    st.session_state['input_N_normal_global'] = st.session_state['slider_N_normal_global']

def actualizar_N_normal_desde_input():
    valor = min(max(int(st.session_state['input_N_normal_global']), 5), 100000)
    st.session_state['N_normal_global_base'] = valor
    st.session_state['slider_N_normal_global'] = valor

def callback_muestra_aleatoria_normal():
    mu_aleatorio = round(float(np.random.uniform(-20.0, 20.0)), 1)
    sigma_aleatorio = round(float(np.random.uniform(0.5, 15.0)), 1)
    N_global = int(np.random.randint(500, 4000))
    
    st.session_state['normal_mu'] = mu_aleatorio
    st.session_state['slider_normal_mu'] = mu_aleatorio
    st.session_state['input_normal_mu'] = mu_aleatorio

    st.session_state['normal_sigma'] = sigma_aleatorio
    st.session_state['slider_normal_sigma'] = sigma_aleatorio
    st.session_state['input_normal_sigma'] = sigma_aleatorio

    st.session_state['N_normal_global_base'] = N_global
    st.session_state['slider_N_normal_global'] = N_global
    st.session_state['input_N_normal_global'] = N_global

def generar_muestra_datos_normal(mu, sigma, N_global):
    datos_simulados = np.random.normal(loc=mu, scale=sigma, size=N_global)
    return datos_simulados

def renderizar_controles_parametros():
    st.subheader("Parámetros de la distribución")
    
    col_mu, col_sigma, col_N = st.columns(3, gap="medium")
    
    with col_mu:
        st.write("**Media (mu):**")
        st.slider(
            "Normal mu slider", min_value=-100.0, max_value=100.0, step=0.5,
            key='slider_normal_mu', on_change=actualizar_normal_mu_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Normal mu input", min_value=-100.0, max_value=100.0, step=0.5,
            key='input_normal_mu', on_change=actualizar_normal_mu_desde_input, label_visibility="collapsed"
        )

    with col_sigma:
        st.write("**Desviación Estándar (sigma):**")
        st.slider(
            "Normal sigma slider", min_value=0.1, max_value=50.0, step=0.1,
            key='slider_normal_sigma', on_change=actualizar_normal_sigma_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Normal sigma input", min_value=0.1, max_value=50.0, step=0.1,
            key='input_normal_sigma', on_change=actualizar_normal_sigma_desde_input, label_visibility="collapsed"
        )

    with col_N:
        st.write("**Muestras continuas (N):**")
        st.slider(
            "Normal Global slider", min_value=10, max_value=50000, step=10,
            key='slider_N_normal_global', on_change=actualizar_N_normal_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Normal Global input", min_value=10, max_value=50000, step=10,
            key='input_N_normal_global', on_change=actualizar_N_normal_desde_input, label_visibility="collapsed"
        )
            
    st.button(
        "Generar datos aleatorios de muestra", 
        key="btn_generar_normal", 
        use_container_width=True, 
        on_click=callback_muestra_aleatoria_normal
    )

def generar_grafica_normal(mu, sigma, N_global, datos_raw, tipo_grafica):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    
    x_eje = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 300)
    pdf_teorica = norm.pdf(x_eje, loc=mu, scale=sigma)
    num_bins = 30

    if tipo_grafica == "Muestra Simulada":
        ax.hist(datos_raw, bins=num_bins, color='#31333F', alpha=0.85, edgecolor='white', label='Simulado')
        ax.set_ylabel('Frecuencia Absoluta (Conteos)', fontsize=11)
        
    elif tipo_grafica == "Distribucion Teorica":
        ax.plot(x_eje, pdf_teorica, color='#E04D98', linewidth=3, label='Teorico (PDF)')
        ax.fill_between(x_eje, pdf_teorica, color='#E04D98', alpha=0.2)
        ax.set_ylabel('Densidad de Probabilidad f(x)', fontsize=11)
        
    elif tipo_grafica == "Superponer Ambas":
        ax.hist(datos_raw, bins=num_bins, density=True, color='#31333F', alpha=0.7, edgecolor='white', label='Simulado (Densidad)')
        ax.plot(x_eje, pdf_teorica, color='#FF69B4', linewidth=2.5, label='Teorico (PDF)')
        ax.set_ylabel('Densidad Escalada', fontsize=11)
        ax.legend(loc='upper right', frameon=False)

    ax.set_xlabel('Valor de la Variable Continua (X)', fontsize=11)
    ax.set_title(f'Distribución Normal (mu = {mu}, sigma = {sigma})', fontsize=11, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    return fig

def renderizar_bloque_visualizacion_normal(mu, sigma, N_global, datos_raw, tipo_grafica):
    st.subheader("Resultados de la Simulación")
    col_izq, col_der = st.columns([1.2, 1.8], gap="large")
    
    figura = generar_grafica_normal(mu, sigma, N_global, datos_raw, tipo_grafica)
    
    media_sim = np.mean(datos_raw)
    var_sim = np.var(datos_raw, ddof=1)
    desv_sim = np.sqrt(var_sim)
    
    media_teo = mu
    var_teo = sigma ** 2
    desv_teo = sigma

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

def renderizar_analisis_y_reportes_normal(mu, sigma, N_global, media_sim, var_sim, desv_sim, datos_raw):
    col_izq_inf, col_der_inf = st.columns([1.4, 1.6], gap="large")
    
    media_teo = mu
    var_teo = sigma ** 2
    desv_teo = sigma

    with col_izq_inf:
        st.write("### Interpretación y Comparación")
        st.write(f"Centro teórico configurado: **{mu}**")
        st.write(f"Dispersión promedio (Desviación): **{sigma}**")
        
        st.write("**Tabla de Resultados Analizados:**")
        datos_tabla = {
            "Concepto": ["Media (Centroide)", "Varianza", "Desviación estándar", "Muestras Totales"],
            "Valor teórico": [f"{media_teo:.4f}", f"{var_teo:.4f}", f"{desv_teo:.4f}", f"{N_global:,}"],
            "Valor simulado": [f"{media_sim:.4f}", f"{var_sim:.4f}", f"{desv_sim:.4f}", f"{N_global:,}"],
            "Diferencia": [f"{abs(media_teo - media_sim):.4f}", f"{abs(var_teo - var_sim):.4f}", f"{abs(desv_teo - desv_sim):.4f}", "-"]
        }
        df_comparativo = pd.DataFrame(datos_tabla)
        st.dataframe(df_comparativo, hide_index=True, use_container_width=True)
        
        st.info("**Nota Teórica de Densidad:** Al superponer las gráficas, se puede apreciar la regla empírica. Aproximadamente el 68% de los datos experimentales caerán de manera natural dentro del rango de una desviación estándar respecto al centro.")

    with col_der_inf:
        st.write("### Herramientas y Reportes")
        
        with st.expander("Ver Fórmulas Teóricas Normales"):
            st.latex(r"f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}")
            st.markdown("**Regla de Probabilidad Empírica:**")
            st.latex(r"P(\mu - \sigma \le X \le \mu + \sigma) \approx 0.6827")

        with st.expander("Inspeccionar Muestra Cruda Generada"):
            df_inspeccion = pd.DataFrame({"Valores Continuos (X)": datos_raw})
            df_inspeccion.index.name = "ID_Muestra"
            st.dataframe(df_inspeccion.head(10), use_container_width=True)

        df_descarga = pd.DataFrame(datos_raw, columns=["Valores_Normal_Gaussiana"])
        csv_data = df_descarga.to_csv(index=True, index_label="ID")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                label="Descargar CSV", data=csv_data,
                key="dl_csv_norm", file_name=f"simulacion_normal_mu{mu}_sigma{sigma}.csv", mime="text/csv", use_container_width=True
            )
            
        with col_btn2:
            reporte_texto = (
                f"REPORTE DE LABORATORIO - DISTRIBUCION NORMAL GAUSSIANA\n"
                f"--------------------------------------------------\n"
                f"Configuración Inicial: mu = {mu} | sigma = {sigma}\n"
                f"Concepto                Valor Teórico   Valor Simulado   Diferencia\n"
                f"Media (mu):              {media_teo:.4f}          {media_sim:.4f}           {abs(media_teo - media_sim):.4f}\n"
                f"Varianza (sigma2):       {var_teo:.4f}          {var_sim:.4f}           {abs(var_teo - var_sim):.4f}\n"
                f"Desv. Estándar (sigma):  {desv_teo:.4f}          {desv_sim:.4f}           {abs(desv_teo - desv_sim):.4f}\n"
                f"Datos Totales (N):       {N_global}            {N_global}             -"
            )
            st.download_button(
                label="Descargar TXT", data=reporte_texto,
                key="dl_txt_norm", file_name=f"reporte_normal_mu{mu}_sigma{sigma}.txt", mime="text/plain", use_container_width=True
            )

def inicializar_normal():
    st.markdown("""
    <style>
    .main .block-container{
        max-width: 1100px;
        margin: auto;
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    intro_normal()
    st.markdown("---")
    inicializar_estado_normal()

    renderizar_controles_parametros()
    
    mu_val = st.session_state['normal_mu']
    sigma_val = st.session_state['normal_sigma']
    N_global = st.session_state['N_normal_global_base']

    st.markdown("---")

    tipo_grafica_seleccionada = st.radio(
        "Selecciona el enfoque visual de la gráfica:",
        ["Muestra Simulada", "Distribucion Teorica", "Superponer Ambas"],
        index=0, horizontal=True, key="radio_norm"
    )

    datos_raw = generar_muestra_datos_normal(mu_val, sigma_val, N_global)
    
    media_sim, var_sim, desv_sim = renderizar_bloque_visualizacion_normal(
        mu_val, sigma_val, N_global, datos_raw, tipo_grafica_seleccionada
    )

    st.markdown("##") 
    st.divider()

    renderizar_analisis_y_reportes_normal(
        mu_val, sigma_val, N_global, media_sim, var_sim, desv_sim, datos_raw
    )