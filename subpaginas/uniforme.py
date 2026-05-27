# subpaginas/uniforme.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import uniform
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_uniforme():
    titulo_rosa("Distribución Uniforme Continua")
    parrafo_adaptable(
        "La distribución Uniforme Continua modela un escenario donde todos los resultados posibles "
        "dentro de un intervalo cerrado definido por un límite inferior <strong>a</strong> y un límite "
        "superior <strong>b</strong> son **igualmente probables**. Al ser una distribución continua, "
        "su función de densidad de probabilidad (PDF) dibuja un rectángulo perfecto."
    )

def inicializar_estado_uniforme():
    # a: Límite inferior
    if 'uniforme_a' not in st.session_state:
        st.session_state['uniforme_a'] = 0.0
    if 'slider_uniforme_a' not in st.session_state:
        st.session_state['slider_uniforme_a'] = st.session_state['uniforme_a']
    if 'input_uniforme_a' not in st.session_state:
        st.session_state['input_uniforme_a'] = st.session_state['uniforme_a']
        
    # b: Límite superior
    if 'uniforme_b' not in st.session_state:
        st.session_state['uniforme_b'] = 10.0
    if 'slider_uniforme_b' not in st.session_state:
        st.session_state['slider_uniforme_b'] = st.session_state['uniforme_b']
    if 'input_uniforme_b' not in st.session_state:
        st.session_state['input_uniforme_b'] = st.session_state['uniforme_b']

    # N_global: Cantidad de datos continuos en la muestra
    if 'N_uniforme_global_base' not in st.session_state:
        st.session_state['N_uniforme_global_base'] = 1000
    if 'slider_N_uniforme_global' not in st.session_state:
        st.session_state['slider_N_uniforme_global'] = st.session_state['N_uniforme_global_base']
    if 'input_N_uniforme_global' not in st.session_state:
        st.session_state['input_N_uniforme_global'] = st.session_state['N_uniforme_global_base']

# --- Callbacks de Sincronización ---
def actualizar_uniforme_a_desde_slider():
    st.session_state['uniforme_a'] = st.session_state['slider_uniforme_a']
    st.session_state['input_uniforme_a'] = st.session_state['slider_uniforme_a']

def actualizar_uniforme_a_desde_input():
    st.session_state['uniforme_a'] = float(st.session_state['input_uniforme_a'])
    st.session_state['slider_uniforme_a'] = float(st.session_state['input_uniforme_a'])

def actualizar_uniforme_b_desde_slider():
    st.session_state['uniforme_b'] = st.session_state['slider_uniforme_b']
    st.session_state['input_uniforme_b'] = st.session_state['slider_uniforme_b']

def actualizar_uniforme_b_desde_input():
    st.session_state['uniforme_b'] = float(st.session_state['input_uniforme_b'])
    st.session_state['slider_uniforme_b'] = float(st.session_state['input_uniforme_b'])

def actualizar_N_uniforme_desde_slider():
    st.session_state['N_uniforme_global_base'] = st.session_state['slider_N_uniforme_global']
    st.session_state['input_N_uniforme_global'] = st.session_state['slider_N_uniforme_global']

def actualizar_N_uniforme_desde_input():
    valor = min(max(int(st.session_state['input_N_uniforme_global']), 5), 100000)
    st.session_state['N_uniforme_global_base'] = valor
    st.session_state['slider_N_uniforme_global'] = valor

def callback_muestra_aleatoria_uniforme():
    a_aleatorio = round(float(np.random.uniform(-50.0, 20.0)), 1)
    b_aleatorio = round(float(a_aleatorio + np.random.uniform(5.0, 60.0)), 1)
    N_global = int(np.random.randint(500, 4000))
    
    st.session_state['uniforme_a'] = a_aleatorio
    st.session_state['slider_uniforme_a'] = a_aleatorio
    st.session_state['input_uniforme_a'] = a_aleatorio

    st.session_state['uniforme_b'] = b_aleatorio
    st.session_state['slider_uniforme_b'] = b_aleatorio
    st.session_state['input_uniforme_b'] = b_aleatorio

    st.session_state['N_uniforme_global_base'] = N_global
    st.session_state['slider_N_uniforme_global'] = N_global
    st.session_state['input_N_uniforme_global'] = N_global

def generar_muestra_datos_uniforme(a, b, N_global):
    # np.random.uniform toma los límites bajo (low) y alto (high)
    datos_simulados = np.random.uniform(low=a, high=b, size=N_global)
    return datos_simulados

def renderizar_controles_parametros():
    st.subheader("Parámetros de la distribución")
    
    # Lectura preventiva para asegurar consistencia de rangos en los controles
    a_actual = st.session_state['uniforme_a']
    b_actual = st.session_state['uniforme_b']
    
    col_a, col_b, col_N = st.columns(3, gap="medium")
    
    with col_a:
        st.write("**Límite Inferior (a):**")
        st.slider(
            "Uniforme a slider", min_value=-100.0, max_value=float(b_actual - 0.1), step=0.5,
            key='slider_uniforme_a', on_change=actualizar_uniforme_a_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Uniforme a input", min_value=-100.0, max_value=float(b_actual - 0.1), step=0.5,
            key='input_uniforme_a', on_change=actualizar_uniforme_a_desde_input, label_visibility="collapsed"
        )

    with col_b:
        st.write("**Límite Superior (b):**")
        st.slider(
            "Uniforme b slider", min_value=float(a_actual + 0.1), max_value=100.0, step=0.5,
            key='slider_uniforme_b', on_change=actualizar_uniforme_b_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Uniforme b input", min_value=float(a_actual + 0.1), max_value=100.0, step=0.5,
            key='input_uniforme_b', on_change=actualizar_uniforme_b_desde_input, label_visibility="collapsed"
        )

    with col_N:
        st.write("**Muestras continuas (N):**")
        st.slider(
            "Uniforme Global slider", min_value=10, max_value=50000, step=10,
            key='slider_N_uniforme_global', on_change=actualizar_N_uniforme_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Uniforme Global input", min_value=10, max_value=50000, step=10,
            key='input_N_uniforme_global', on_change=actualizar_N_uniforme_desde_input, label_visibility="collapsed"
        )
            
    st.button(
        "Generar datos aleatorios de muestra", 
        key="btn_generar_uniforme", 
        use_container_width=True, 
        on_click=callback_muestra_aleatoria_uniforme
    )

def generar_grafica_uniforme(a, b, N_global, datos_raw, tipo_grafica):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    
    # Al ser continua, usamos densidades de probabilidad e histogramas con bins de densidad
    rango_ancho = b - a
    num_bins = 20
    
    # Eje X extendido un 15% a los lados para apreciar dónde empieza y termina el rectángulo
    x_eje = np.linspace(a - (rango_ancho * 0.15), b + (rango_ancho * 0.15), 200)
    
    # Densidad teórica uniforme: 1 / (b - a) dentro del rango, 0 fuera
    pdf_teorica = uniform.pdf(x_eje, loc=a, scale=rango_ancho)

    if tipo_grafica == "Muestra Simulada":
        # Multiplicamos por la densidad del área real para escalar el conteo absoluto estimado
        ax.hist(datos_raw, bins=num_bins, color='#31333F', alpha=0.85, edgecolor='white', label='Simulado')
        ax.set_ylabel('Frecuencia Absoluta (Conteos)', fontsize=11)
        
    elif tipo_grafica == "Distribucion Teorica":
        ax.plot(x_eje, pdf_teorica, color='#E04D98', linewidth=3, label='Teórico (PDF)')
        ax.fill_between(x_eje, pdf_teorica, color='#E04D98', alpha=0.2)
        ax.set_ylabel('Densidad de Probabilidad $f(x)$', fontsize=11)
        
    elif tipo_grafica == "Superponer Ambas":
        # Para poder superponer un histograma continuo con una PDF teórica line, el histograma DEBE ser density=True
        # Para que sea entendible en términos de frecuencia, calculamos la escala en el eje derecho secundario si hiciera falta,
        # o normalizamos ambos sobre el mismo eje de densidad. Lo haremos sobre densidad para perfecta simetría científica.
        ax.hist(datos_raw, bins=num_bins, density=True, color='#31333F', alpha=0.7, edgecolor='white', label='Simulado (Densidad)')
        ax.plot(x_eje, pdf_teorica, color='#FF69B4', linewidth=2.5, label='Teórico (PDF)')
        ax.set_ylabel('Densidad Escalada', fontsize=11)
        ax.legend(loc='upper right', frameon=False)

    ax.set_xlabel('Valor de la Variable Continua (X)', fontsize=11)
    ax.set_title(f'Distribución Uniforme Continua ($a = {a}$, $b = {b}$)', fontsize=11, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    return fig

def renderizar_bloque_visualizacion_uniforme(a, b, N_global, datos_raw, tipo_grafica):
    st.subheader("Resultados de la Simulación")
    col_izq, col_der = st.columns([1.2, 1.8], gap="large")
    
    figura = generar_grafica_uniforme(a, b, N_global, datos_raw, tipo_grafica)
    
    media_sim = np.mean(datos_raw)
    var_sim = np.var(datos_raw, ddof=1)
    desv_sim = np.sqrt(var_sim)
    
    # Fórmulas analíticas teóricas de la uniforme continua
    media_teo = (a + b) / 2.0
    var_teo = ((b - a) ** 2) / 12.0
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

def renderizar_analisis_y_reportes_uniforme(a, b, N_global, media_sim, var_sim, desv_sim, datos_raw):
    col_izq_inf, col_der_inf = st.columns([1.4, 1.6], gap="large")
    
    media_teo = (a + b) / 2.0
    var_teo = ((b - a) ** 2) / 12.0
    desv_teo = np.sqrt(var_teo)

    with col_izq_inf:
        st.write("### Interpretación y Comparación")
        st.write(f"Rango de valores continuos permitidos: **[{a}, {b}]**")
        st.write(f"Ancho del intervalo experimental ($b - a$): **{b - a:.2f}**")
        
        st.write("**Tabla de Resultados Analizados:**")
        datos_tabla = {
            "Concepto": ["Media Centroide", "Varianza", "Desviación estándar", "Muestras Totales"],
            "Valor teórico": [f"{media_teo:.4f}", f"{var_teo:.4f}", f"{desv_teo:.4f}", f"{N_global:,}"],
            "Valor simulado": [f"{media_sim:.4f}", f"{var_sim:.4f}", f"{desv_sim:.4f}", f"{N_global:,}"],
            "Diferencia": [f"{abs(media_teo - media_sim):.4f}", f"{abs(var_teo - var_sim):.4f}", f"{abs(desv_teo - desv_sim):.4f}", "-"]
        }
        df_comparativo = pd.DataFrame(datos_tabla)
        st.dataframe(df_comparativo, hide_index=True, use_container_width=True)
        
        st.info("📊 **Nota Teórica de Altura:** En este modelo continuo, la altura máxima de la curva teórica es exactamente $1 / (b - a)$. Al superponer las gráficas, puedes notar cómo los bins de la muestra de datos crudos se alinean para rellenar equitativamente esa área unitaria.")

    with col_der_inf:
        st.write("### Herramientas y Reportes")
        
        with st.expander("Ver Fórmulas Teóricas Uniformes"):
            st.latex(r"\mu = \frac{a + b}{2}")
            st.latex(r"\sigma^2 = \frac{(b - a)^2}{12}")
            st.latex(r"f(x) = \frac{1}{b - a} \quad \text{para } a \le x \le b")

        with st.expander("Inspeccionar Muestra Cruda Generada"):
            df_inspeccion = pd.DataFrame({"Valores Continuos (X)": datos_raw})
            df_inspeccion.index.name = "ID_Muestra"
            st.dataframe(df_inspeccion.head(10), use_container_width=True)

        df_descarga = pd.DataFrame(datos_raw, columns=["Valores_Uniforme_Continua"])
        csv_data = df_descarga.to_csv(index=True, index_label="ID")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                label="Descargar CSV", data=csv_data,
                key="dl_csv_unif", file_name=f"simulacion_uniforme_a{a}_b{b}.csv", mime="text/csv", use_container_width=True
            )
            
        with col_btn2:
            reporte_texto = (
                f"REPORTE DE LABORATORIO - DISTRIBUCION UNIFORME CONTINUA\n"
                f"--------------------------------------------------\n"
                f"Rango Configurado: a = {a} | b = {b}\n"
                f"Concepto                Valor Teórico   Valor Simulado   Diferencia\n"
                f"Media (mu):              {media_teo:.4f}          {media_sim:.4f}           {abs(media_teo - media_sim):.4f}\n"
                f"Varianza (sigma2):       {var_teo:.4f}          {var_sim:.4f}           {abs(var_teo - var_sim):.4f}\n"
                f"Desv. Estándar (sigma):  {desv_teo:.4f}          {desv_sim:.4f}           {abs(desv_teo - desv_sim):.4f}\n"
                f"Datos Totales (N):       {N_global}            {N_global}             -"
            )
            st.download_button(
                label="Descargar TXT", data=reporte_texto,
                key="dl_txt_unif", file_name=f"reporte_uniforme_a{a}_b{b}.txt", mime="text/plain", use_container_width=True
            )

def renderizar_tlc_uniforme(a, b):
    st.markdown("---")
    st.subheader("🔬 Demostración del Teorema del Límite Central (TLC)")
    
    parrafo_adaptable(
        "Aunque una sola muestra uniforme se ve completamente plana y rectangular, al tomar grupos "
        "independientes de estas variables continuas y graficar el promedio de cada grupo, la forma plana "
        "desaparece por completo y renace como una **curva Gaussiana Normal**."
    )
    
    col_c1, col_c2 = st.columns(2, gap="large")
    with col_c1:
        num_muestras = st.slider(
            "Número de promedios calculados (m):", 
            min_value=100, max_value=5000, value=2000, step=100, key="tlc_unif_m"
        )
    with col_c2:
        tam_muestra_tlc = st.slider(
            "Tamaño de cada muestra agrupada (k):", 
            min_value=2, max_value=100, value=30, step=1, key="tlc_unif_k"
        )

    # Simulación del TLC con datos uniformes continuos
    matriz_unif = np.random.uniform(low=a, high=b, size=(num_muestras, tam_muestra_tlc))
    promedios_muestrales = np.mean(matriz_unif, axis=1)
    
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.hist(promedios_muestrales, bins=25, density=True, color='#E04D98', alpha=0.7, edgecolor='white', label='Promedios Muestrales')
    
    # Ecuaciones teóricas de la campana resultante por TLC
    mu_tlc = (a + b) / 2.0
    sigma_unif_individual = np.sqrt(((b - a) ** 2) / 12.0)
    sigma_tlc = sigma_unif_individual / np.sqrt(tam_muestra_tlc)
    
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
        st.markdown(f"* **Media de Promedios:** {np.mean(promedios_muestrales):.4f} (Teórica: {mu_tlc:.4f})")
        st.markdown(f"* **Error Estándar Muestral:** {np.std(promedios_muestrales):.4f} (Teórico: {sigma_tlc:.4f})")

def inicializar_uniforme():
    st.markdown("""
    <style>
    .main .block-container{
        max-width: 1100px;
        margin: auto;
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    intro_uniforme()
    st.markdown("---")
    inicializar_estado_uniforme()

    renderizar_controles_parametros()
    
    a_val = st.session_state['uniforme_a']
    b_val = st.session_state['uniforme_b']
    N_global = st.session_state['N_uniforme_global_base']

    # Blindaje lógico manual cruzado por si fallara la sincronización temporal en inputs
    if a_val >= b_val:
        b_val = a_val + 1.0

    st.markdown("---")

    tipo_grafica_seleccionada = st.radio(
        "Selecciona el enfoque visual de la gráfica:",
        ["Muestra Simulada", "Distribucion Teorica", "Superponer Ambas"],
        index=0, horizontal=True, key="radio_unif"
    )

    datos_raw = generar_muestra_datos_uniforme(a_val, b_val, N_global)
    
    media_sim, var_sim, desv_sim = renderizar_bloque_visualizacion_uniforme(
        a_val, b_val, N_global, datos_raw, tipo_grafica_seleccionada
    )

    st.markdown("##") 
    st.divider()

    renderizar_analisis_y_reportes_uniforme(
        a_val, b_val, N_global, media_sim, var_sim, desv_sim, datos_raw
    )

    renderizar_tlc_uniforme(a_val, b_val)