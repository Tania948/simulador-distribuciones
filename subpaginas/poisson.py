# subpaginas/poisson.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import poisson
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_poisson():
    titulo_rosa("Distribución de Poisson")
    parrafo_adaptable(
        "La distribución de Poisson expresa la probabilidad de que ocurra un número determinado de "
        "eventos discretos en un **intervalo fijo de tiempo o espacio**, conociendo de antemano su "
        "tasa promedio de ocurrencia (<strong>&lambda;</strong>) y bajo la condición de que estos "
        "eventos ocurren de forma independiente."
    )

def inicializar_estado_poisson():
    # lambda: Tasa promedio de eventos por intervalo
    if 'poisson_lambda' not in st.session_state:
        st.session_state['poisson_lambda'] = 4.0
    if 'slider_poisson_lambda' not in st.session_state:
        st.session_state['slider_poisson_lambda'] = st.session_state['poisson_lambda']
    if 'input_poisson_lambda' not in st.session_state:
        st.session_state['input_poisson_lambda'] = st.session_state['poisson_lambda']
        
    # N_global: Número de intervalos independientes simulados
    if 'N_poisson_global_base' not in st.session_state:
        st.session_state['N_poisson_global_base'] = 1000
    if 'slider_N_poisson_global' not in st.session_state:
        st.session_state['slider_N_poisson_global'] = st.session_state['N_poisson_global_base']
    if 'input_N_poisson_global' not in st.session_state:
        st.session_state['input_N_poisson_global'] = st.session_state['N_poisson_global_base']

# --- Callbacks de Sincronización ---
def actualizar_poisson_lambda_desde_slider():
    st.session_state['poisson_lambda'] = st.session_state['slider_poisson_lambda']
    st.session_state['input_poisson_lambda'] = st.session_state['slider_poisson_lambda']

def actualizar_poisson_lambda_desde_input():
    valor = max(float(st.session_state['input_poisson_lambda']), 0.1)
    st.session_state['poisson_lambda'] = valor
    st.session_state['slider_poisson_lambda'] = valor

def actualizar_N_poisson_global_desde_slider():
    st.session_state['N_poisson_global_base'] = st.session_state['slider_N_poisson_global']
    st.session_state['input_N_poisson_global'] = st.session_state['slider_N_poisson_global']

def actualizar_N_poisson_global_desde_input():
    valor = min(max(int(st.session_state['input_N_poisson_global']), 5), 100000)
    st.session_state['N_poisson_global_base'] = valor
    st.session_state['slider_N_poisson_global'] = valor

def callback_muestra_aleatoria_poisson():
    lambda_aleatorio = round(float(np.random.uniform(1.0, 15.0)), 1)
    N_global = int(np.random.randint(500, 4000))
    
    st.session_state['poisson_lambda'] = lambda_aleatorio
    st.session_state['slider_poisson_lambda'] = lambda_aleatorio
    st.session_state['input_poisson_lambda'] = lambda_aleatorio

    st.session_state['N_poisson_global_base'] = N_global
    st.session_state['slider_N_poisson_global'] = N_global
    st.session_state['input_N_poisson_global'] = N_global

def generar_muestra_datos_poisson(lam, N_global):
    datos_simulados = np.random.poisson(lam=lam, size=N_global)
    return datos_simulados

def renderizar_controles_parametros():
    st.subheader("Parámetros de la distribución")
    col_lam, col_N = st.columns(2, gap="large")
    
    with col_lam:
        st.write("**Tasa promedio de ocurrencia (&lambda;):**")
        st.slider(
            "Poisson Lambda slider", min_value=0.1, max_value=30.0, step=0.1,
            key='slider_poisson_lambda', on_change=actualizar_poisson_lambda_desde_slider, label_visibility="collapsed"
        )
        col_t, col_i = st.columns([1.5, 1])
        with col_t: st.write("O ingresa &lambda; manual:")
        with col_i:
            st.number_input(
                "Poisson Lambda input", min_value=0.1, max_value=30.0, step=0.1,
                key='input_poisson_lambda', on_change=actualizar_poisson_lambda_desde_input, label_visibility="collapsed"
            )

    with col_N:
        st.write("**Intervalos totales a simular (N):**")
        st.slider(
            "Poisson Global slider", min_value=5, max_value=50000, step=10,
            key='slider_N_poisson_global', on_change=actualizar_N_poisson_global_desde_slider, label_visibility="collapsed"
        )
        col_t, col_i = st.columns([1.5, 1])
        with col_t: st.write("O ingresa N manual:")
        with col_i:
            st.number_input(
                "Poisson Global input", min_value=5, max_value=50000, step=10,
                key='input_N_poisson_global', on_change=actualizar_N_poisson_global_desde_input, label_visibility="collapsed"
            )
            
    st.button(
        "Generar datos aleatorios de muestra", 
        key="btn_generar_poisson", 
        use_container_width=True, 
        on_click=callback_muestra_aleatoria_poisson
    )

def generar_grafica_poisson(lam, N_global, datos_raw, tipo_grafica):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    
    # Poisson teóricamente no tiene límite superior, recortamos visualmente en el percentil 99.5
    max_visible = int(np.percentile(datos_raw, 99.5))
    max_visible = max(max_visible, int(lam + 4)) # Asegurar que quepa la joroba de la curva si lambda es pequeña
    x_valores = np.arange(0, max_visible + 1)
    
    # Frecuencias simuladas reales
    valores_sim, conteos_sim = np.unique(datos_raw, return_counts=True)
    frecuencias_simuladas = np.zeros(len(x_valores))
    for v, c in zip(valores_sim, conteos_sim):
        if v <= max_visible:
            frecuencias_simuladas[v] = c

    # Frecuencias teóricas usando PMF de SciPy
    frecuencias_teoricas = poisson.pmf(x_valores, lam) * N_global

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

    ax.set_xlabel('Número de eventos en el intervalo (k)', fontsize=11)
    ax.set_title(f'Distribución de Poisson (&lambda; = {lam}, N = {N_global})', fontsize=11, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    return fig

def renderizar_bloque_visualizacion_poisson(lam, N_global, datos_raw, tipo_grafica):
    st.subheader("Resultados de la Simulación")
    col_izq, col_der = st.columns([1.2, 1.8], gap="large")
    
    figura = generar_grafica_poisson(lam, N_global, datos_raw, tipo_grafica)
    
    media_sim = np.mean(datos_raw)
    var_sim = np.var(datos_raw, ddof=1)
    desv_sim = np.sqrt(var_sim)
    
    # La teoría dicta que en Poisson: Media = Varianza = Lambda
    media_teo = lam
    var_teo = lam
    desv_teo = np.sqrt(lam)

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

def renderizar_analisis_y_reportes_poisson(lam, N_global, media_sim, var_sim, desv_sim, datos_raw):
    col_izq_inf, col_der_inf = st.columns([1.4, 1.6], gap="large")
    
    media_teo = lam
    var_teo = lam
    desv_teo = np.sqrt(lam)

    with col_izq_inf:
        st.write("### Interpretación y Comparación")
        st.write(f"Tasa promedio teórica configurada (&lambda;): **{lam}** sucesos/intervalo")
        st.write(f"Número total de intervalos evaluados (N): **{N_global:,}**")
        
        st.write("**Tabla de Resultados Analizados:**")
        datos_tabla = {
            "Concepto": ["Media (Sucesos)", "Varianza", "Desviación estándar", "Intervalos Totales"],
            "Valor teórico": [f"{media_teo:.4f}", f"{var_teo:.4f}", f"{desv_teo:.4f}", f"{N_global:,}"],
            "Valor simulado": [f"{media_sim:.4f}", f"{var_sim:.4f}", f"{desv_sim:.4f}", f"{N_global:,}"],
            "Diferencia": [f"{abs(media_teo - media_sim):.4f}", f"{abs(var_teo - var_sim):.4f}", f"{abs(desv_teo - desv_sim):.4f}", "-"]
        }
        df_comparativo = pd.DataFrame(datos_tabla)
        st.dataframe(df_comparativo, hide_index=True, use_container_width=True)
        
        # Elemento de valor para el reporte científico
        st.info("📌 **Propiedad de Equidistribución:** Una característica única de Poisson es que su media es exactamente igual a su varianza ($\mu = \sigma^2 = \lambda$). Puedes ver que en los datos simulados los valores de x̄ y s² se persiguen muy de cerca.")

    with col_der_inf:
        st.write("### Herramientas y Reportes")
        
        with st.expander("Ver Fórmulas Teóricas"):
            st.latex(r"\mu = \lambda")
            st.latex(r"\sigma^2 = \lambda \quad \lhd \quad \sigma = \sqrt{\lambda}")
            st.latex(r"P(X = k) = \frac{e^{-\lambda} \cdot \lambda^k}{k!}")

        with st.expander("Inspeccionar Muestra Cruda Generada"):
            df_inspeccion = pd.DataFrame({"Eventos en Intervalo (X)": datos_raw})
            df_inspeccion.index.name = "ID_Intervalo"
            st.dataframe(df_inspeccion.head(10), use_container_width=True)

        df_descarga = pd.DataFrame(datos_raw, columns=["Conteo_Eventos_Poisson"])
        csv_data = df_descarga.to_csv(index=True, index_label="Intervalo")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                label="Descargar CSV", data=csv_data,
                key="dl_csv_poisson", file_name=f"simulacion_poisson_lambda{lam}.csv", mime="text/csv", use_container_width=True
            )
            
        with col_btn2:
            reporte_texto = (
                f"REPORTE DE LABORATORIO - DISTRIBUCION DE POISSON\n"
                f"--------------------------------------------------\n"
                f"Parámetro: Tasa de ocurrencia (lambda) = {lam}\n"
                f"Concepto                Valor Teórico   Valor Simulado   Diferencia\n"
                f"Media (mu):              {media_teo:.4f}          {media_sim:.4f}           {abs(media_teo - media_sim):.4f}\n"
                f"Varianza (sigma2):       {var_teo:.4f}          {var_sim:.4f}           {abs(var_teo - var_sim):.4f}\n"
                f"Desv. Estándar (sigma):  {desv_teo:.4f}          {desv_sim:.4f}           {abs(desv_teo - desv_sim):.4f}\n"
                f"Intervalos Totales (N):  {N_global}            {N_global}             -"
            )
            st.download_button(
                label="Descargar TXT", data=reporte_texto,
                key="dl_txt_poisson", file_name=f"reporte_poisson_lambda{lam}.txt", mime="text/plain", use_container_width=True
            )

def renderizar_tlc_poisson(lam):
    st.markdown("---")
    st.subheader("🔬 Demostración del Teorema del Límite Central (TLC)")
    
    parrafo_adaptable(
        "Cuando recolectamos los conteos de múltiples intervalos independientes de Poisson y calculamos su promedio, "
        "la distribución resultante rompe el sesgo asimétrico inicial y adopta la silueta de la campana de Gauss."
    )
    
    col_c1, col_c2 = st.columns(2, gap="large")
    with col_c1:
        num_muestras = st.slider(
            "Número de promedios calculados (m):", 
            min_value=100, max_value=5000, value=2000, step=100, key="tlc_poisson_m"
        )
    with col_c2:
        tam_muestra_tlc = st.slider(
            "Tamaño de cada muestra agrupada (k):", 
            min_value=2, max_value=100, value=30, step=1, key="tlc_poisson_k"
        )

    # Simulación real del TLC con variables Poisson
    matriz_poisson = np.random.poisson(lam=lam, size=(num_muestras, tam_muestra_tlc))
    promedios_muestrales = np.mean(matriz_poisson, axis=1)
    
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.hist(promedios_muestrales, bins=25, density=True, color='#E04D98', alpha=0.7, edgecolor='white', label='Promedios Muestrales')
    
    # Ecuaciones teóricas de la Normal derivada del TLC
    mu_tlc = lam
    sigma_tlc = np.sqrt(lam) / np.sqrt(tam_muestra_tlc)
    
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

def inicializar_poisson():
    st.markdown("""
    <style>
    .main .block-container{
        max-width: 1100px;
        margin: auto;
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    intro_poisson()
    st.markdown("---")
    inicializar_estado_poisson()

    renderizar_controles_parametros()
    
    lam_teorica = st.session_state['poisson_lambda']
    N_global = st.session_state['N_poisson_global_base']

    st.markdown("---")

    tipo_grafica_seleccionada = st.radio(
        "Selecciona el enfoque visual de la gráfica:",
        ["Muestra Simulada", "Distribucion Teorica", "Superponer Ambas"],
        index=0, horizontal=True, key="radio_poisson"
    )

    datos_raw = generar_muestra_datos_poisson(lam_teorica, N_global)
    
    media_sim, var_sim, desv_sim = renderizar_bloque_visualizacion_poisson(
        lam_teorica, N_global, datos_raw, tipo_grafica_seleccionada
    )

    st.markdown("##") 
    st.divider()

    renderizar_analisis_y_reportes_poisson(
        lam_teorica, N_global, media_sim, var_sim, desv_sim, datos_raw
    )

    renderizar_tlc_poisson(lam_teorica)