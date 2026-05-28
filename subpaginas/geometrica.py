import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import geom
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_geometrica():
    titulo_rosa("Distribución Geométrica")
    parrafo_adaptable(
        "La distribución Geométrica modela el número de <strong>ensayos independientes de Bernoulli necesarios "
        "para obtener el primer éxito</strong>. Es una distribución discreta 'sin memoria', donde la probabilidad "
        "de éxito en cada intento es constantemente <strong>p</strong>."
    )

def inicializar_estado_geometrica():
    if 'p_geom_base' not in st.session_state:
        st.session_state['p_geom_base'] = 0.25
    if 'slider_geom_p' not in st.session_state:
        st.session_state['slider_geom_p'] = st.session_state['p_geom_base']
    if 'input_geom_p' not in st.session_state:
        st.session_state['input_geom_p'] = st.session_state['p_geom_base']
        
    if 'N_geom_global_base' not in st.session_state:
        st.session_state['N_geom_global_base'] = 1000
    if 'slider_N_geom_global' not in st.session_state:
        st.session_state['slider_N_geom_global'] = st.session_state['N_geom_global_base']
    if 'input_N_geom_global' not in st.session_state:
        st.session_state['input_N_geom_global'] = st.session_state['N_geom_global_base']

def actualizar_geom_p_desde_slider():
    st.session_state['p_geom_base'] = st.session_state['slider_geom_p']
    st.session_state['input_geom_p'] = st.session_state['slider_geom_p']

def actualizar_geom_p_desde_input():
    valor = st.session_state['input_geom_p']
    valor_validado = min(max(valor, 0.01), 1.0)
    st.session_state['p_geom_base'] = valor_validado
    st.session_state['slider_geom_p'] = valor_validado

def actualizar_N_geom_global_desde_slider():
    st.session_state['N_geom_global_base'] = st.session_state['slider_N_geom_global']
    st.session_state['input_N_geom_global'] = st.session_state['slider_N_geom_global']

def actualizar_N_geom_global_desde_input():
    valor = st.session_state['input_N_geom_global']
    valor_validado = min(max(int(valor), 5), 100000)
    st.session_state['N_geom_global_base'] = valor_validado
    st.session_state['slider_N_geom_global'] = valor_validado

def callback_muestra_aleatoria_geometrica():
    p_aleatorio = round(float(np.random.uniform(0.1, 0.8)), 2)
    st.session_state['p_geom_base'] = p_aleatorio
    st.session_state['slider_geom_p'] = p_aleatorio
    st.session_state['input_geom_p'] = p_aleatorio
    
    N_aleatorio = int(np.random.randint(200, 4000))
    st.session_state['N_geom_global_base'] = N_aleatorio
    st.session_state['slider_N_geom_global'] = N_aleatorio
    st.session_state['input_N_geom_global'] = N_aleatorio

def generar_muestra_datos_geometrica(p, N_global):
    datos_simulados = np.random.geometric(p=p, size=N_global)
    return datos_simulados

def renderizar_controles_parametros():
    st.subheader("Parámetros de la distribución")
    col_p, col_N = st.columns(2, gap="large")
    
    with col_p:
        st.write("**Probabilidad de éxito en cada ensayo (p):**")
        st.slider(
            "Geom Prob slider", min_value=0.01, max_value=1.0, step=0.01,
            key='slider_geom_p', on_change=actualizar_geom_p_desde_slider, label_visibility="collapsed"
        )
        col_t, col_i = st.columns([1.5, 1])
        with col_t: st.write("O ingresa p manual:")
        with col_i:
            st.number_input(
                "Geom Prob input", min_value=0.01, max_value=1.0, step=0.01,
                key='input_geom_p', on_change=actualizar_geom_p_desde_input, label_visibility="collapsed"
            )

    with col_N:
        st.write("**Número total de experimentos (N):**")
        st.slider(
            "Geom Global slider", min_value=5, max_value=50000, step=1,
            key='slider_N_geom_global', on_change=actualizar_N_geom_global_desde_slider, label_visibility="collapsed"
        )
        col_t, col_i = st.columns([1.5, 1])
        with col_t: st.write("O ingresa N manual:")
        with col_i:
            st.number_input(
                "Geom Global input", min_value=5, max_value=50000, step=1,
                key='input_N_geom_global', on_change=actualizar_N_geom_global_desde_input, label_visibility="collapsed"
            )
            
    st.button(
        "Generar datos aleatorios de muestra", 
        key="btn_generar_geometrica",  
        use_container_width=True, 
        on_click=callback_muestra_aleatoria_geometrica
    )

def generar_grafica_geometrica(p, N_global, datos_raw, tipo_grafica):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    
    max_intentos = int(np.percentile(datos_raw, 98)) 
    max_intentos = max(max_intentos, 5)
    
    x_valores = np.arange(1, max_intentos + 1)
    
    valores_sim, conteos_sim = np.unique(datos_raw, return_counts=True)
    frecuencias_simuladas = np.zeros(max_intentos)
    for v, c in zip(valores_sim, conteos_sim):
        if v <= max_intentos:
            frecuencias_simuladas[v - 1] = c

    frecuencias_teoricas = geom.pmf(x_valores, p) * N_global

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

    ax.set_xlabel('Intentos necesarios hasta primer éxito (k)', fontsize=11)
    ax.set_title(f'Distribución Geométrica (p = {p}, N = {N_global})', fontsize=11, fontweight='bold')
    ax.set_xticks(x_valores if max_intentos <= 20 else np.arange(1, max_intentos + 1, max(1, max_intentos // 15)))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    return fig

def renderizar_bloque_visualizacion_geometrica(p, N_global, datos_raw, tipo_grafica):
    st.subheader("Resultados de la Simulación")
    col_izq, col_der = st.columns([1.2, 1.8], gap="large")
    
    figura = generar_grafica_geometrica(p, N_global, datos_raw, tipo_grafica)
    
    media_sim = np.mean(datos_raw)
    var_sim = np.var(datos_raw, ddof=1)
    desv_sim = np.sqrt(var_sim)
    
    media_teo = 1.0 / p
    var_teo = (1.0 - p) / (p ** 2)
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

def renderizar_analisis_y_reportes_geometrica(p, N_global, media_sim, var_sim, desv_sim, datos_raw):
    col_izq_inf, col_der_inf = st.columns([1.4, 1.6], gap="large")
    
    media_teo = 1.0 / p
    var_teo = (1.0 - p) / (p ** 2)
    desv_teo = np.sqrt(var_teo)

    pmf_valores = geom.pmf(datos_raw, p)

    with col_izq_inf:
        st.write("### Interpretación y Comparación")
        st.write(f"Cada dato representa cuántos tiros tomó conseguir **1 Éxito**.")
        st.write(f"Probabilidad asignada al éxito (p): **{p:.2%}**")
        st.write(f"Experimentos corridos completos (N): **{N_global:,}**")
        
        st.write("**Tabla de Resultados Analizados:**")
        datos_tabla = {
            "Concepto": ["Media (Tiros al éxito)", "Varianza", "Desviación estándar", "Repeticiones totales"],
            "Valor teórico": [f"{media_teo:.4f}", f"{var_teo:.4f}", f"{desv_teo:.4f}", f"{N_global:,}"],
            "Valor simulado": [f"{media_sim:.4f}", f"{var_sim:.4f}", f"{desv_sim:.4f}", f"{N_global:,}"],
            "Diferencia": [f"{abs(media_teo - media_sim):.4f}", f"{abs(var_teo - var_sim):.4f}", f"{abs(desv_teo - desv_sim):.4f}", "-"]
        }
        df_comparativo = pd.DataFrame(datos_tabla)
        st.dataframe(df_comparativo, hide_index=True, use_container_width=True)
        
        if N_global >= 5000:
            st.info("🔬 **Evidencia Decisiva:** Al tratarse de una curva decreciente asimétrica, requiere de números de muestra grandes ($N$) para estabilizar la varianza experimental frente al modelo ideal.")

    with col_der_inf:
        st.write("### Herramientas y Reportes")
        
        with st.expander("Ver Fórmulas Teóricas Geométricas"):
            st.latex(r"\mu = \frac{1}{p}")
            st.latex(r"\sigma^2 = \frac{1 - p}{p^2} \quad \lhd \quad \sigma = \frac{\sqrt{1 - p}}{p}")
            st.latex(r"P(X = k) = (1-p)^{k-1} \cdot p")

        with st.expander("Inspeccionar Muestra Cruda y PMF Teórica"):
            df_inspeccion = pd.DataFrame({
                "Intentos Totales (X)": datos_raw,
                "PMF Teórica P(X=k)": pmf_valores
            })
            df_inspeccion.index.name = "ID_Experimento"
            st.dataframe(df_inspeccion.head(10), use_container_width=True)
            st.caption(f"Visualización de los primeros 10 cierres de éxito junto a su probabilidad de masa (PMF) teórica.")

        df_descarga = pd.DataFrame({
            "Intentos_Hasta_Exito": datos_raw,
            "PMF_Teorica": pmf_valores
        })
        csv_data = df_descarga.to_csv(index=True, index_label="ID")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                label="Descargar CSV", data=csv_data,
                key="dl_csv_geom", file_name=f"simulacion_geometrica_p{p:.2f}.csv", mime="text/csv", use_container_width=True
            )
            
        with col_btn2:
            reporte_texto = (
                f"REPORTE DE LABORATORIO - DISTRIBUCION GEOMETRICA\n"
                f"--------------------------------------------------\n"
                f"Parámetro: Prob. Éxito de base (p) = {p:.4f}\n"
                f"Concepto                Valor Teórico   Valor Simulado   Diferencia\n"
                f"Media (mu / x-barra):    {media_teo:.4f}          {media_sim:.4f}           {abs(media_teo - media_sim):.4f}\n"
                f"Varianza (sigma2 / s2):  {var_teo:.4f}          {var_sim:.4f}           {abs(var_teo - var_sim):.4f}\n"
                f"Desv. Estándar (sigma):  {desv_teo:.4f}          {desv_sim:.4f}           {abs(desv_teo - desv_sim):.4f}\n"
                f"Experimentos Totales (N): {N_global}            {N_global}             -"
            )
            st.download_button(
                label="Descargar TXT", data=reporte_texto,
                key="dl_txt_geom", file_name=f"reporte_geometrica_p{p:.2f}.txt", mime="text/plain", use_container_width=True
            )

def renderizar_tlc_geometrica(p_teorica):
    st.markdown("---")
    st.subheader("Demostración del Teorema del Límite Central (TLC)")
    
    parrafo_adaptable(
        "Aunque la distribución geométrica original es totalmente asimétrica y sesgada a la izquierda (con forma de L invertida), "
        "cuando agrupamos varias de estas muestras independientes y calculamos su promedio, la combinación "
        "de valores genera una hermosa curva <strong>Normal simétrica</strong>."
    )
    
    col_c1, col_c2 = st.columns(2, gap="large")
    with col_c1:
        num_muestras = st.slider(
            "Número de promedios calculados (m):", 
            min_value=100, max_value=5000, value=2000, step=100, key="tlc_geom_m"
        )
    with col_c2:
        tam_muestra_tlc = st.slider(
            "Tamaño de cada muestra agrupada (k):", 
            min_value=2, max_value=100, value=30, step=1, key="tlc_geom_k"
        )

    matriz_geom = np.random.geometric(p=p_teorica, size=(num_muestras, tam_muestra_tlc))
    promedios_muestrales = np.mean(matriz_geom, axis=1)
    
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.hist(promedios_muestrales, bins=25, density=True, color='#E04D98', alpha=0.7, edgecolor='white', label='Promedios Muestrales')
    
    mu_tlc = 1.0 / p_teorica
    sigma_tlc = (np.sqrt(1.0 - p_teorica) / p_teorica) / np.sqrt(tam_muestra_tlc)
    
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
        st.info("Una distribución que originalmente tenía forma de rampa descendente se convierte en una campana perfectamente simétrica gracias al TLC.")

def inicializar_geometrica():
    st.markdown("""
    <style>
    .main .block-container{
        max-width: 1100px;
        margin: auto;
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    intro_geometrica()
    st.markdown("---")
    inicializar_estado_geometrica()

    renderizar_controles_parametros()
    
    p_teorica = st.session_state['p_geom_base']
    N_global = st.session_state['N_geom_global_base']

    st.markdown("---")

    tipo_grafica_seleccionada = st.radio(
        "Selecciona el enfoque visual de la gráfica:",
        ["Muestra Simulada", "Distribucion Teorica", "Superponer Ambas"],
        index=0, horizontal=True, key="radio_geom"
    )

    datos_raw = generar_muestra_datos_geometrica(p_teorica, N_global)
    
    media_sim, var_sim, desv_sim = renderizar_bloque_visualizacion_geometrica(
        p_teorica, N_global, datos_raw, tipo_grafica_seleccionada
    )

    st.markdown("##") 
    st.divider()

    renderizar_analisis_y_reportes_geometrica(
        p_teorica, N_global, media_sim, var_sim, desv_sim, datos_raw
    )

    renderizar_tlc_geometrica(p_teorica)