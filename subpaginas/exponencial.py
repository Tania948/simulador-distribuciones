# subpaginas/exponencial.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import expon
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_exponencial():
    titulo_rosa("Distribución Exponencial")
    parrafo_adaptable(
        "La distribución Exponencial es una distribución continua que modela el <strong>tiempo o espacio</strong> "
        "que transcurre entre dos eventos consecutivos en un proceso de Poisson. Es muy utilizada "
        "en ingeniería y fiabilidad para calcular la vida útil de componentes o tiempos de espera, "
        "caracterizándose por su famosa propiedad de <strong>falta de memoria</strong>."
    )

def inicializar_estado_exponencial():
    # lambda_tasa: Tasa de eventos (frecuencia de ocurrencia)
    if 'exponencial_lambda' not in st.session_state:
        st.session_state['exponencial_lambda'] = 1.0
    if 'slider_exponencial_lambda' not in st.session_state:
        st.session_state['slider_exponencial_lambda'] = st.session_state['exponencial_lambda']
    if 'input_exponencial_lambda' not in st.session_state:
        st.session_state['input_exponencial_lambda'] = st.session_state['exponencial_lambda']

    # N_global: Cantidad de datos en la muestra
    if 'N_exponencial_global_base' not in st.session_state:
        st.session_state['N_exponencial_global_base'] = 1000
    if 'slider_N_exponencial_global' not in st.session_state:
        st.session_state['slider_N_exponencial_global'] = st.session_state['N_exponencial_global_base']
    if 'input_N_exponencial_global' not in st.session_state:
        st.session_state['input_N_exponencial_global'] = st.session_state['N_exponencial_global_base']

# --- Callbacks de Sincronización ---
def actualizar_exponencial_lambda_desde_slider():
    st.session_state['exponencial_lambda'] = st.session_state['slider_exponencial_lambda']
    st.session_state['input_exponencial_lambda'] = st.session_state['slider_exponencial_lambda']

def actualizar_exponencial_lambda_desde_input():
    valor = max(float(st.session_state['input_exponencial_lambda']), 0.01) # Evitar lambda <= 0
    st.session_state['exponencial_lambda'] = valor
    st.session_state['slider_exponencial_lambda'] = valor

def actualizar_N_exponencial_desde_slider():
    st.session_state['N_exponencial_global_base'] = st.session_state['slider_N_exponencial_global']
    st.session_state['input_N_exponencial_global'] = st.session_state['slider_N_exponencial_global']

def actualizar_N_exponencial_desde_input():
    valor = min(max(int(st.session_state['input_N_exponencial_global']), 5), 100000)
    st.session_state['N_exponencial_global_base'] = valor
    st.session_state['slider_N_exponencial_global'] = valor

def callback_muestra_aleatoria_exponencial():
    lambda_aleatorio = round(float(np.random.uniform(0.1, 8.0)), 2)
    N_global = int(np.random.randint(500, 4000))
    
    st.session_state['exponencial_lambda'] = lambda_aleatorio
    st.session_state['slider_exponencial_lambda'] = lambda_aleatorio
    st.session_state['input_exponencial_lambda'] = lambda_aleatorio

    st.session_state['N_exponencial_global_base'] = N_global
    st.session_state['slider_N_exponencial_global'] = N_global
    st.session_state['input_N_exponencial_global'] = N_global

def generar_muestra_datos_exponencial(lambda_tasa, N_global):
    # IMPORTANTE: NumPy usa el parámetro 'scale' que es el inverso de lambda (1 / lambda)
    tiempo_promedio = 1.0 / lambda_tasa
    datos_simulados = np.random.exponential(scale=tiempo_promedio, size=N_global)
    return datos_simulados

def renderizar_controles_parametros():
    st.subheader("Parámetros de la distribución")
    
    col_lambda, col_vacio, col_N = st.columns(3, gap="medium")
    
    with col_lambda:
        st.write("**Tasa de Ocurrencia (lambda):**")
        st.slider(
            "Exponencial lambda slider", min_value=0.05, max_value=20.0, step=0.05,
            key='slider_exponencial_lambda', on_change=actualizar_exponencial_lambda_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Exponencial lambda input", min_value=0.05, max_value=20.0, step=0.05,
            key='input_exponencial_lambda', on_change=actualizar_exponencial_lambda_desde_input, label_visibility="collapsed"
        )

    with col_vacio:
        # Columna estética para balancear la visualización y mostrar el parámetro derivado (Tiempo promedio)
        lambda_actual = st.session_state['exponencial_lambda']
        st.write("**Tiempo Promedio Esperado (1/lambda):**")
        st.info(f"Cada evento ocurre en promedio cada: **{1.0 / lambda_actual:.4f}** unidades de tiempo.")

    with col_N:
        st.write("**Muestras continuas (N):**")
        st.slider(
            "Exponencial Global slider", min_value=10, max_value=50000, step=10,
            key='slider_N_exponencial_global', on_change=actualizar_N_exponencial_desde_slider, label_visibility="collapsed"
        )
        st.number_input(
            "Exponencial Global input", min_value=10, max_value=50000, step=10,
            key='input_N_exponencial_global', on_change=actualizar_N_exponencial_desde_input, label_visibility="collapsed"
        )
            
    st.button(
        "Generar datos aleatorios de muestra", 
        key="btn_generar_exponencial", 
        use_container_width=True, 
        on_click=callback_muestra_aleatoria_exponencial
    )

def generar_grafica_exponencial(lambda_tasa, N_global, datos_raw, tipo_grafica):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    
    # Eje X va desde 0 hasta el valor máximo de la muestra para capturar el decaimiento
    max_x = float(np.percentile(datos_raw, 98)) # Cortamos en el percentil 98 para evitar que colas extremas arruinen el zoom
    x_eje = np.linspace(0, max_x, 300)
    pdf_teorica = expon.pdf(x_eje, scale=1.0/lambda_tasa)
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

    ax.set_xlabel('Tiempo / Espacio entre Eventos (X)', fontsize=11)
    ax.set_title(f'Distribución Exponencial (lambda = {lambda_tasa})', fontsize=11, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    return fig

def renderizar_bloque_visualizacion_exponencial(lambda_tasa, N_global, datos_raw, tipo_grafica):
    st.subheader("Resultados de la Simulación")
    col_izq, col_der = st.columns([1.2, 1.8], gap="large")
    
    figura = generar_grafica_exponencial(lambda_tasa, N_global, datos_raw, tipo_grafica)
    
    media_sim = np.mean(datos_raw)
    var_sim = np.var(datos_raw, ddof=1)
    desv_sim = np.sqrt(var_sim)
    
    media_teo = 1.0 / lambda_tasa
    var_teo = 1.0 / (lambda_tasa ** 2)
    desv_teo = 1.0 / lambda_tasa

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

def renderizar_analisis_y_reportes_exponencial(lambda_tasa, N_global, media_sim, var_sim, desv_sim, datos_raw):
    col_izq_inf, col_der_inf = st.columns([1.4, 1.6], gap="large")
    
    media_teo = 1.0 / lambda_tasa
    var_teo = 1.0 / (lambda_tasa ** 2)
    desv_teo = 1.0 / lambda_tasa

    with col_izq_inf:
        st.write("### Interpretación y Comparación")
        st.write(f"Tasa configurada ($\lambda$): **{lambda_tasa}** eventos por unidad de tiempo.")
        st.write(f"Tiempo promedio analítico ($1/\lambda$): **{media_teo:.4f}**")
        
        st.write("**Tabla de Resultados Analizados:**")
        datos_tabla = {
            "Concepto": ["Media Esperada", "Varianza", "Desviación estándar", "Muestras Totales"],
            "Valor teórico": [f"{media_teo:.4f}", f"{var_teo:.4f}", f"{desv_teo:.4f}", f"{N_global:,}"],
            "Valor simulado": [f"{media_sim:.4f}", f"{var_sim:.4f}", f"{desv_sim:.4f}", f"{N_global:,}"],
            "Diferencia": [f"{abs(media_teo - media_sim):.4f}", f"{abs(var_teo - var_sim):.4f}", f"{abs(desv_teo - desv_sim):.4f}", "-"]
        }
        df_comparativo = pd.DataFrame(datos_tabla)
        st.dataframe(df_comparativo, hide_index=True, use_container_width=True)
        
        st.info("**Propiedad Singular:** La **Media** y la **Desviación Estándar** teóricas son exactamente idénticas ($1/\lambda$). Puedes verificar en tu tabla cómo tus valores experimentales simulan esta igualdad.")

    with col_der_inf:
        st.write("### Herramientas y Reportes")
        
        with st.expander("Ver Fórmulas Teóricas Exponenciales"):
            st.latex(r"f(x) = \lambda e^{-\lambda x} \quad \text{para } x \ge 0")
            st.latex(r"\mu = \frac{1}{\lambda}")
            st.latex(r"\sigma^2 = \frac{1}{\lambda^2}")

        with st.expander("Inspeccionar Muestra Cruda Generada"):
            df_inspeccion = pd.DataFrame({"Tiempo Transcurrido (X)": datos_raw})
            df_inspeccion.index.name = "ID_Muestra"
            st.dataframe(df_inspeccion.head(10), use_container_width=True)

        df_descarga = pd.DataFrame(datos_raw, columns=["Valores_Tiempos_Exponenciales"])
        csv_data = df_descarga.to_csv(index=True, index_label="ID")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                label="Descargar CSV", data=csv_data,
                key="dl_csv_exp", file_name=f"simulacion_exponencial_lambda{lambda_tasa}.csv", mime="text/csv", use_container_width=True
            )
            
        with col_btn2:
            reporte_texto = (
                f"REPORTE DE LABORATORIO - DISTRIBUCION EXPONENCIAL\n"
                f"--------------------------------------------------\n"
                f"Configuración de Tasa: lambda = {lambda_tasa}\n"
                f"Concepto                Valor Teórico   Valor Simulado   Diferencia\n"
                f"Media (mu):              {media_teo:.4f}          {media_sim:.4f}           {abs(media_teo - media_sim):.4f}\n"
                f"Varianza (sigma2):       {var_teo:.4f}          {var_sim:.4f}           {abs(var_teo - var_sim):.4f}\n"
                f"Desv. Estándar (sigma):  {desv_teo:.4f}          {desv_sim:.4f}           {abs(desv_teo - desv_sim):.4f}\n"
                f"Datos Totales (N):       {N_global}            {N_global}             -"
            )
            st.download_button(
                label="Descargar TXT", data=reporte_texto,
                key="dl_txt_exp", file_name=f"reporte_exponencial_lambda{lambda_tasa}.txt", mime="text/plain", use_container_width=True
            )

def inicializar_exponencial():
    st.markdown("""
    <style>
    .main .block-container{
        max-width: 1100px;
        margin: auto;
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    intro_exponencial()
    st.markdown("---")
    inicializar_estado_exponencial()

    renderizar_controles_parametros()
    
    lambda_val = st.session_state['exponencial_lambda']
    N_global = st.session_state['N_exponencial_global_base']

    st.markdown("---")

    tipo_grafica_seleccionada = st.radio(
        "Selecciona el enfoque visual de la gráfica:",
        ["Muestra Simulada", "Distribucion Teorica", "Superponer Ambas"],
        index=0, horizontal=True, key="radio_exp"
    )

    datos_raw = generar_muestra_datos_exponencial(lambda_val, N_global)
    
    media_sim, var_sim, desv_sim = renderizar_bloque_visualizacion_exponencial(
        lambda_val, N_global, datos_raw, tipo_grafica_seleccionada
    )

    st.markdown("##") 
    st.divider()

    renderizar_analisis_y_reportes_exponencial(
        lambda_val, N_global, media_sim, var_sim, desv_sim, datos_raw
    )