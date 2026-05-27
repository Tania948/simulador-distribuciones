# subpaginas/hipergeometrica.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import hypergeom
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_hipergeometrica():
    titulo_rosa("Distribución Hipergeométrica")
    parrafo_adaptable(
        "La distribución Hipergeométrica modela el número de éxitos en una muestra de tamaño "
        "<strong>n</strong> extraída <strong>sin reemplazo</strong> de una población total "
        "<strong>N</strong> que contiene exactamente <strong>K</strong> elementos considerados como éxitos. "
        "Al no haber reemplazo, la probabilidad cambia en cada extracción."
    )

def inicializar_estado_hipergeometrica():
    if 'hiper_N_pob' not in st.session_state:
        st.session_state['hiper_N_pob'] = 100
    if 'slider_hiper_N' not in st.session_state:
        st.session_state['slider_hiper_N'] = st.session_state['hiper_N_pob']
    if 'input_hiper_N' not in st.session_state:
        st.session_state['input_hiper_N'] = st.session_state['hiper_N_pob']
        
    if 'hiper_K_exitos' not in st.session_state:
        st.session_state['hiper_K_exitos'] = 30
    if 'slider_hiper_K' not in st.session_state:
        st.session_state['slider_hiper_K'] = st.session_state['hiper_K_exitos']
    if 'input_hiper_K' not in st.session_state:
        st.session_state['input_hiper_K'] = st.session_state['hiper_K_exitos']

    if 'hiper_n_muestra' not in st.session_state:
        st.session_state['hiper_n_muestra'] = 20
    if 'slider_hiper_n' not in st.session_state:
        st.session_state['slider_hiper_n'] = st.session_state['hiper_n_muestra']
    if 'input_hiper_n' not in st.session_state:
        st.session_state['input_hiper_n'] = st.session_state['hiper_n_muestra']

    if 'N_hiper_global_base' not in st.session_state:
        st.session_state['N_hiper_global_base'] = 1000
    if 'slider_N_hiper_global' not in st.session_state:
        st.session_state['slider_N_hiper_global'] = st.session_state['N_hiper_global_base']
    if 'input_N_hiper_global' not in st.session_state:
        st.session_state['input_N_hiper_global'] = st.session_state['N_hiper_global_base']

def actualizar_hiper_N_desde_slider():
    st.session_state['hiper_N_pob'] = st.session_state['slider_hiper_N']
    st.session_state['input_hiper_N'] = st.session_state['slider_hiper_N']

def actualizar_hiper_N_desde_input():
    valor = max(int(st.session_state['input_hiper_N']), 10)
    st.session_state['hiper_N_pob'] = valor
    st.session_state['slider_hiper_N'] = valor

def actualizar_hiper_K_desde_slider():
    st.session_state['hiper_K_exitos'] = st.session_state['slider_hiper_K']
    st.session_state['input_hiper_K'] = st.session_state['slider_hiper_K']

def actualizar_hiper_K_desde_input():
    valor = max(int(st.session_state['input_hiper_K']), 1)
    st.session_state['hiper_K_exitos'] = valor
    st.session_state['slider_hiper_K'] = valor

def actualizar_hiper_n_desde_slider():
    st.session_state['hiper_n_muestra'] = st.session_state['slider_hiper_n']
    st.session_state['input_hiper_n'] = st.session_state['slider_hiper_n']

def actualizar_hiper_n_desde_input():
    valor = max(int(st.session_state['input_hiper_n']), 1)
    st.session_state['hiper_n_muestra'] = valor
    st.session_state['slider_hiper_n'] = valor

def actualizar_N_hiper_global_desde_slider():
    st.session_state['N_hiper_global_base'] = st.session_state['slider_N_hiper_global']
    st.session_state['input_N_hiper_global'] = st.session_state['slider_N_hiper_global']

def actualizar_N_hiper_global_desde_input():
    valor = min(max(int(st.session_state['input_N_hiper_global']), 5), 100000)
    st.session_state['N_hiper_global_base'] = valor
    st.session_state['slider_N_hiper_global'] = valor

def callback_muestra_aleatoria_hipergeometrica():
    N_pob = int(np.random.randint(50, 501))
    K_exitos = int(np.random.randint(5, int(N_pob * 0.7)))
    n_muestra = int(np.random.randint(5, int(N_pob * 0.4)))
    N_global = int(np.random.randint(500, 3001))
    
    st.session_state['hiper_N_pob'] = N_pob
    st.session_state['slider_hiper_N'] = N_pob
    st.session_state['input_hiper_N'] = N_pob

    st.session_state['hiper_K_exitos'] = K_exitos
    st.session_state['slider_hiper_K'] = K_exitos
    st.session_state['input_hiper_K'] = K_exitos

    st.session_state['hiper_n_muestra'] = n_muestra
    st.session_state['slider_hiper_n'] = n_muestra
    st.session_state['input_hiper_n'] = n_muestra

    st.session_state['N_hiper_global_base'] = N_global
    st.session_state['slider_N_hiper_global'] = N_global
    st.session_state['input_N_hiper_global'] = N_global

def generar_muestra_datos_hipergeometrica(N_pob, K_exitos, n_muestra, N_global):
    ngood = K_exitos
    nbad = N_pob - K_exitos
    datos_simulados = np.random.hypergeometric(ngood=ngood, nbad=nbad, nsample=n_muestra, size=N_global)
    return datos_simulados

def renderizar_controles_parametros():
    st.subheader("Parámetros de la distribución")
    
    N_pob_actual = st.session_state['hiper_N_pob']
    
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    with col1:
        st.write("**Población (N):**")
        st.slider(
            "Hiper N slider", min_value=10, max_value=1000, step=5,
            key='slider_hiper_N', on_change=actualizar_hiper_N_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Hiper N input", min_value=10, max_value=1000, step=5,
            key='input_hiper_N', on_change=actualizar_hiper_N_desde_input, label_visibility="collapsed"
        )

    with col2:
        st.write("**Éxitos en Pob (K):**")
        st.slider(
            "Hiper K slider", min_value=1, max_value=int(N_pob_actual), step=1,
            key='slider_hiper_K', on_change=actualizar_hiper_K_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Hiper K input", min_value=1, max_value=int(N_pob_actual), step=1,
            key='input_hiper_K', on_change=actualizar_hiper_K_desde_input, label_visibility="collapsed"
        )

    with col3:
        st.write("**Muestra (n):**")
        st.slider(
            "Hiper n slider", min_value=1, max_value=int(N_pob_actual), step=1,
            key='slider_hiper_n', on_change=actualizar_hiper_n_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Hiper n input", min_value=1, max_value=int(N_pob_actual), step=1,
            key='input_hiper_n', on_change=actualizar_hiper_n_desde_input, label_visibility="collapsed"
        )

    with col4:
        st.write("**Simulaciones (N_glob):**")
        st.slider(
            "Hiper Glob slider", min_value=5, max_value=50000, step=10,
            key='slider_N_hiper_global', on_change=actualizar_N_hiper_global_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Hiper Glob input", min_value=5, max_value=50000, step=10,
            key='input_N_hiper_global', on_change=actualizar_N_hiper_global_desde_input, label_visibility="collapsed"
        )
            
    st.button(
        "Generar datos aleatorios de muestra", 
        key="btn_generar_hipergeometrica", 
        use_container_width=True, 
        on_click=callback_muestra_aleatoria_hipergeometrica
    )

def generar_grafica_hipergeometrica(N_pob, K_exitos, n_muestra, N_global, datos_raw, tipo_grafica):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    
    min_posible = max(0, n_muestra - (N_pob - K_exitos))
    max_posible = min(n_muestra, K_exitos)
    x_valores = np.arange(min_posible, max_posible + 1)
    
    valores_sim, conteos_sim = np.unique(datos_raw, return_counts=True)
    frecuencias_simuladas = np.zeros(len(x_valores))
    for v, c in zip(valores_sim, conteos_sim):
        if min_posible <= v <= max_posible:
            frecuencias_simuladas[v - min_posible] = c

    frecuencias_teoricas = hypergeom.pmf(x_valores, N_pob, K_exitos, n_muestra) * N_global

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

    ax.set_xlabel('Número de éxitos en la muestra (k)', fontsize=11)
    ax.set_title(f'Hipergeométrica (N={N_pob}, K={K_exitos}, n={n_muestra})', fontsize=11, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    return fig

def renderizar_bloque_visualizacion_hipergeometrica(N_pob, K_exitos, n_muestra, N_global, datos_raw, tipo_grafica):
    st.subheader("Resultados de la Simulación")
    col_izq, col_der = st.columns([1.2, 1.8], gap="large")
    
    figura = generar_grafica_hipergeometrica(N_pob, K_exitos, n_muestra, N_global, datos_raw, tipo_grafica)
    
    media_sim = np.mean(datos_raw)
    var_sim = np.var(datos_raw, ddof=1)
    desv_sim = np.sqrt(var_sim)
    
    p_equivalente = K_exitos / N_pob
    media_teo = n_muestra * p_equivalente
    factor_correccion = (N_pob - n_muestra) / (N_pob - 1) if N_pob > 1 else 1
    var_teo = n_muestra * p_equivalente * (1.0 - p_equivalente) * factor_correccion
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

def renderizar_analisis_y_reportes_hipergeometrica(N_pob, K_exitos, n_muestra, N_global, media_sim, var_sim, desv_sim, datos_raw):
    col_izq_inf, col_der_inf = st.columns([1.4, 1.6], gap="large")
    
    p_equivalente = K_exitos / N_pob
    media_teo = n_muestra * p_equivalente
    factor_correccion = (N_pob - n_muestra) / (N_pob - 1) if N_pob > 1 else 1
    var_teo = n_muestra * p_equivalente * (1.0 - p_equivalente) * factor_correccion
    desv_teo = np.sqrt(var_teo)

    with col_izq_inf:
        st.write("### Interpretación y Comparación")
        st.write(f"Proporción de éxitos inicial en población ($K/N$): **{p_equivalente:.2%}**")
        st.write(f"Tamaño del subgrupo extraído sin reemplazo ($n$): **{n_muestra}**")
        
        st.write("**Tabla de Resultados Analizados:**")
        datos_tabla = {
            "Concepto": ["Media Éxitos", "Varianza", "Desviación estándar", "Simulaciones realizadas"],
            "Valor teórico": [f"{media_teo:.4f}", f"{var_teo:.4f}", f"{desv_teo:.4f}", f"{N_global:,}"],
            "Valor simulado": [f"{media_sim:.4f}", f"{var_sim:.4f}", f"{desv_sim:.4f}", f"{N_global:,}"],
            "Diferencia": [f"{abs(media_teo - media_sim):.4f}", f"{abs(var_teo - var_sim):.4f}", f"{abs(desv_teo - desv_sim):.4f}", "-"]
        }
        df_comparativo = pd.DataFrame(datos_tabla)
        st.dataframe(df_comparativo, hide_index=True, use_container_width=True)
        
        if N_pob >= 500 and (n_muestra / N_pob) < 0.05:
            st.info("💡 **Dato de Laboratorio:** Como el tamaño de muestra ($n$) es menor al 5% de la población ($N$), el factor de corrección se acerca a 1. En este punto, la Hipergeométrica se comporta casi idéntica a una Binomial.")

    with col_der_inf:
        st.write("### Herramientas y Reportes")
        
        with st.expander("Ver Fórmulas Teóricas"):
            st.latex(r"\mu = n \cdot \frac{K}{N}")
            st.latex(r"\sigma^2 = n \cdot \frac{K}{N} \cdot \left(1 - \frac{K}{N}\right) \cdot \frac{N - n}{N - 1}")
            st.latex(r"P(X = k) = \frac{\binom{K}{k} \binom{N - K}{n - k}}{\binom{N}{n}}")

        with st.expander("Inspeccionar Muestra Cruda Generada"):
            df_inspeccion = pd.DataFrame({"Éxitos en Muestra (X)": datos_raw})
            df_inspeccion.index.name = "ID_Simulacion"
            st.dataframe(df_inspeccion.head(10), use_container_width=True)

        df_descarga = pd.DataFrame(datos_raw, columns=["Exitos_Hipergeometrica"])
        csv_data = df_descarga.to_csv(index=True, index_label="ID")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                label="Descargar CSV", data=csv_data,
                key="dl_csv_hiper", file_name=f"simulacion_hipergeometrica.csv", mime="text/csv", use_container_width=True
            )
            
        with col_btn2:
            reporte_texto = (
                f"REPORTE DE LABORATORIO - DISTRIBUCION HIPERGEOMETRICA\n"
                f"--------------------------------------------------\n"
                f"Población (N)={N_pob} | Éxitos (K)={K_exitos} | Muestra (n)={n_muestra}\n"
                f"Concepto                Valor Teórico   Valor Simulado   Diferencia\n"
                f"Media:                   {media_teo:.4f}          {media_sim:.4f}           {abs(media_teo - media_sim):.4f}\n"
                f"Varianza:                {var_teo:.4f}          {var_sim:.4f}           {abs(var_teo - var_sim):.4f}\n"
                f"Desv. Estándar:          {desv_teo:.4f}          {desv_sim:.4f}           {abs(desv_teo - desv_sim):.4f}\n"
                f"Simulaciones Totales:    {N_global}            {N_global}             -"
            )
            st.download_button(
                label="Descargar TXT", data=reporte_texto,
                key="dl_txt_hiper", file_name=f"reporte_hipergeometrica.txt", mime="text/plain", use_container_width=True
            )

def renderizar_tlc_hipergeometrica(N_pob, K_exitos, n_muestra):
    st.markdown("---")
    st.subheader("Demostración del Teorema del Límite Central (TLC)")
    
    parrafo_adaptable(
        "Al promediar múltiples conjuntos independientes de variables hipergeométricas, las fluctuaciones "
        "tienden a estabilizarse y alinearse armónicamente con la campana continua de Gauss."
    )
    
    col_c1, col_c2 = st.columns(2, gap="large")
    with col_c1:
        num_muestras = st.slider(
            "Número de promedios calculados (m):", 
            min_value=100, max_value=5000, value=2000, step=100, key="tlc_hiper_m"
        )
    with col_c2:
        tam_muestra_tlc = st.slider(
            "Tamaño de cada muestra agrupada (k):", 
            min_value=2, max_value=100, value=30, step=1, key="tlc_hiper_k"
        )

    ngood = K_exitos
    nbad = N_pob - K_exitos
    matriz_hiper = np.random.hypergeometric(ngood=ngood, nbad=nbad, nsample=n_muestra, size=(num_muestras, tam_muestra_tlc))
    promedios_muestrales = np.mean(matriz_hiper, axis=1)
    
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.hist(promedios_muestrales, bins=25, density=True, color='#E04D98', alpha=0.7, edgecolor='white', label='Promedios Muestrales')
    
    p_eq = K_exitos / N_pob
    factor_c = (N_pob - n_muestra) / (N_pob - 1) if N_pob > 1 else 1
    mu_tlc = n_muestra * p_eq
    sigma_tlc = (np.sqrt(n_muestra * p_eq * (1.0 - p_eq) * factor_c)) / np.sqrt(tam_muestra_tlc)
    
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

def inicializar_hipergeometrica():
    st.markdown("""
    <style>
    .main .block-container{
        max-width: 1100px;
        margin: auto;
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    intro_hipergeometrica()
    st.markdown("---")
    inicializar_estado_hipergeometrica()

    renderizar_controles_parametros()
    
    N_pob = st.session_state['hiper_N_pob']
    K_exitos = st.session_state['hiper_K_exitos']
    n_muestra = st.session_state['hiper_n_muestra']
    N_global = st.session_state['N_hiper_global_base']

    if K_exitos > N_pob: K_exitos = N_pob
    if n_muestra > N_pob: n_muestra = N_pob

    st.markdown("---")

    tipo_grafica_seleccionada = st.radio(
        "Selecciona el enfoque visual de la gráfica:",
        ["Muestra Simulada", "Distribucion Teorica", "Superponer Ambas"],
        index=0, horizontal=True, key="radio_hiper"
    )

    datos_raw = generar_muestra_datos_hipergeometrica(N_pob, K_exitos, n_muestra, N_global)
    
    media_sim, var_sim, desv_sim = renderizar_bloque_visualizacion_hipergeometrica(
        N_pob, K_exitos, n_muestra, N_global, datos_raw, tipo_grafica_seleccionada
    )

    st.markdown("##") 
    st.divider()

    renderizar_analisis_y_reportes_hipergeometrica(
        N_pob, K_exitos, n_muestra, N_global, media_sim, var_sim, desv_sim, datos_raw
    )

    renderizar_tlc_hipergeometrica(N_pob, K_exitos, n_muestra)