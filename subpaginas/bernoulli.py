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
    if 'p_base' not in st.session_state:
        st.session_state['p_base'] = 0.30
    if 'slider_p' not in st.session_state:
        st.session_state['slider_p'] = st.session_state['p_base']
    if 'input_p' not in st.session_state:
        st.session_state['input_p'] = st.session_state['p_base']
        
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
    valor_validado = min(max(int(valor), 2), 100000)
    st.session_state['n_base'] = valor_validado
    st.session_state['slider_n'] = valor_validado

def generar_muestra_datos(p, q, n_muestra):
    datos_simulados = np.random.choice([0, 1], size=n_muestra, p=[q, p])
    exitos = np.sum(datos_simulados == 1)
    fracasos = np.sum(datos_simulados == 0)
    return datos_simulados, exitos, fracasos

def generar_grafica_seleccionada(p, q, n_muestra, exitos, fracasos, tipo_grafica):
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
        barras_sim = ax.bar(x - ancho_barra/2, conteos_simulados, width=ancho_barra, color='#31333F', alpha=0.85, label='Simulado')
        barras_teo = ax.bar(x + ancho_barra/2, conteos_teoricos, width=ancho_barra, color='#FF69B4', alpha=0.85, label='Teorico')
        
        for barra in barras_sim:
            altura = barra.get_height()
            ax.annotate(f'{altura:,}', xy=(barra.get_x() + barra.get_width() / 2, altura),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)
            
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
            min_value=2, max_value=100000, step=1,
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
                min_value=2, max_value=100000, step=1,
                key='input_n',
                on_change=actualizar_n_desde_input,
                label_visibility="collapsed"
            )
        
        if st.button("Generar datos aleatorios de muestra", use_container_width=True):
            n_aleatorio = int(np.random.randint(2, 10001))
            st.session_state['n_base'] = n_aleatorio
            st.session_state['slider_n'] = n_aleatorio
            st.session_state['input_n'] = n_aleatorio
            st.rerun()

    p_teorica = st.session_state['p_base']
    q_teorica = 1.0 - p_teorica
    media_teorica = p_teorica
    var_teorica = p_teorica * q_teorica
    desv_teorica = np.sqrt(var_teorica)
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

    col_izq_sup, col_der_sup = st.columns([1.2, 1.8], gap="large")
    
    datos_raw, exitos_sim, fracasos_sim = generar_muestra_datos(p_teorica, q_teorica, n_muestra_final)
    figura = generar_grafica_seleccionada(p_teorica, q_teorica, n_muestra_final, exitos_sim, fracasos_sim, tipo_grafica_seleccionada)

    media_simulada = np.mean(datos_raw)
    var_simulada = np.var(datos_raw, ddof=1)
    desv_simulada = np.sqrt(var_simulada)

    with col_izq_sup:
        if tipo_grafica_seleccionada == "Muestra Simulada":
            st.write("### Indicadores Simulados")
            st.metric("Media Muestral (x̄)", f"{media_simulada:.4f}")
            st.metric("Varianza Muestral (s²)", f"{var_simulada:.4f}")
            st.metric("Desviación Estándar (s)", f"{desv_simulada:.4f}")
            
        elif tipo_grafica_seleccionada == "Distribucion Teorica":
            st.write("### Indicadores Teoricos")
            st.metric("Esperanza Matemática (μ)", f"{media_teorica:.4f}")
            st.metric("Varianza Teórica (σ²)", f"{var_teorica:.4f}")
            st.metric("Desviación Estándar (σ)", f"{desv_teorica:.4f}")
            
        elif tipo_grafica_seleccionada == "Superponer Ambas":
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

    st.markdown("##") 
    st.divider()

    # ==========================================
    # SECCIÓN 3: TABLA COMPARATIVA Y REPORTES
    # ==========================================
    col_izq_inf, col_der_inf = st.columns([1.4, 1.6], gap="large")

    with col_izq_inf:
        st.write("### Interpretación y Comparación")
        
        # Bloque de interpretación unificada (Teórica + Simulada)
        p_simulada_porcentaje = (exitos_sim / n_muestra_final)
        q_simulada_porcentaje = (fracasos_sim / n_muestra_final)
        
        st.write(f"Probabilidad de éxito (p): Teórica **{p_teorica:.2%}** | Simulada **{p_simulada_porcentaje:.2%}**")
        st.write(f"Probabilidad de fracaso (q): Teórica **{q_teorica:.2%}** | Simulada **{q_simulada_porcentaje:.2%}**")
        st.write(f"Tamaño de muestra global activo (N): **{n_muestra_final:,}**")
        
        st.write("**Tabla de Resultados Analizados:**")
        
        # Modificación para unificar la fila final sin restar diferencias innecesarias
        datos_tabla = {
            "Concepto": ["Media", "Varianza", "Desviación estándar", "Tamaño de muestra"],
            "Valor teórico": [f"{media_teorica:.4f}", f"{var_teorica:.4f}", f"{desv_teorica:.4f}", f"{n_muestra_final:,}"],
            "Valor simulado": [f"{media_simulada:.4f}", f"{var_simulada:.4f}", f"{desv_simulada:.4f}", f"{n_muestra_final:,}"],
            "Diferencia": [f"{abs(media_teorica - media_simulada):.4f}", f"{abs(var_teorica - var_simulada):.4f}", f"{abs(desv_teorica - desv_simulada):.4f}", "-"]
        }
        df_comparativo = pd.DataFrame(datos_tabla)
        st.dataframe(df_comparativo, hide_index=True, use_container_width=True)

    with col_der_inf:
        st.write("### Herramientas y Reportes")

        with st.expander("Ver Formulas Teoricas"):
            st.latex(r"p + q = 1 \quad \lhd \quad \mu = p")
            st.latex(r"\sigma^2 = p \cdot q \quad \lhd \quad \sigma = \sqrt{p \cdot q}")

        df_descarga = pd.DataFrame(datos_raw, columns=["Resultado_Simulacion"])
        csv_data = df_descarga.to_csv(index=True, index_label="Iteracion")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                label="Descargar CSV",
                data=csv_data,
                file_name=f"simulacion_bernoulli_{p_teorica:.2f}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col_btn2:
            reporte_texto = (
                f"REPORTE DE LABORATORIO - DISTRIBUCION DE BERNOULLI\n"
                f"--------------------------------------------------\n"
                f"Concepto                Valor Teorico   Valor Simulado   Diferencia\n"
                f"Media (mu / x-barra):    {media_teorica:.4f}          {media_simulada:.4f}           {abs(media_teorica - media_simulada):.4f}\n"
                f"Varianza (sigma2 / s2):  {var_teorica:.4f}          {var_simulada:.4f}           {abs(var_teorica - var_simulada):.4f}\n"
                f"Desv. Estándar (sigma):  {desv_teorica:.4f}          {desv_simulada:.4f}           {abs(desv_teorica - desv_simulada):.4f}\n"
                f"Tamaño de Muestra (N):   {n_muestra_final}                         "
            )
            st.download_button(
                label="Descargar TXT",
                data=reporte_texto,
                file_name=f"reporte_bernoulli_{p_teorica:.2f}.txt",
                mime="text/plain",
                use_container_width=True
            )