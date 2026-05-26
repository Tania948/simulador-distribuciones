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
    if 'tamano_muestra' not in st.session_state:
        st.session_state['tamano_muestra'] = 1000

def actualizar_desde_slider():
    st.session_state['p_base'] = st.session_state['slider_p']
    st.session_state['input_p'] = st.session_state['slider_p']

def actualizar_desde_input():
    valor = st.session_state['input_p']
    valor_validado = min(max(valor, 0.0), 1.0)
    st.session_state['p_base'] = valor_validado
    st.session_state['slider_p'] = valor_validado

def generar_muestra_datos(p, q, n_muestra):
    """Genera la muestra simulada y computa las frecuencias."""
    datos_simulados = np.random.choice([0, 1], size=n_muestra, p=[q, p])
    exitos = np.sum(datos_simulados == 1)
    fracasos = np.sum(datos_simulados == 0)
    return datos_simulados, exitos, fracasos

def generar_grafica_seleccionada(p, q, n_muestra, exitos, fracasos, tipo_grafica):
    """Genera la figura de Matplotlib según la vista seleccionada por el usuario."""
    fig, ax = plt.subplots(figsize=(7, 4.2))
    categorias = ['Fracaso (0)', 'Éxito (1)']
    conteos_simulados = [fracasos, exitos]
    conteos_teoricos = [q * n_muestra, p * n_muestra]

    if tipo_grafica == "Muestra Simulada":
        barras = ax.bar(categorias, conteos_simulados, color=['#31333F', '#FF69B4'], width=0.45, alpha=0.85, label='Simulado')
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
        ax.plot(categorias, conteos_teoricos, color='#FF69B4', marker='o', linewidth=2.5, markersize=8, label='Teorico')
        for i, v in enumerate(conteos_teoricos):
            porcentaje = (v / n_muestra) * 100
            ax.annotate(f'{v:,.1f}\n({porcentaje:.1f}%)',
                        xy=(categorias[i], v),
                        xytext=(0, 7), textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
        ax.set_ylabel('Frecuencia Esperada (Teorica)', fontsize=11)
        ax.set_ylim(0, max(conteos_teoricos) * 1.15)

    elif tipo_grafica == "Superponer Ambas":
        # Barras de la simulación real
        ax.bar(categorias, conteos_simulados, color='#31333F', width=0.45, alpha=0.4, label='Simulado')
        # Línea de la tendencia teórica calculada
        ax.plot(categorias, conteos_teoricos, color='#FF69B4', marker='o', linewidth=2.5, markersize=8, label='Teorico')
        
        # Etiquetas combinadas breves para no saturar visualmente
        for i in range(2):
            ax.annotate(f'Sim: {conteos_simulados[i]:,}\nTeo: {conteos_teoricos[i]:,.0f}',
                        xy=(categorias[i], max(conteos_simulados[i], conteos_teoricos[i])),
                        xytext=(0, 8), textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
            
        ax.set_ylabel('Frecuencias Comparadas', fontsize=11)
        ax.set_ylim(0, max(max(conteos_simulados), max(conteos_teoricos)) * 1.2)
        ax.legend(loc='upper center', frameon=False, ncol=2)

    ax.set_title(f'Resultados en Base a Vista Seleccionada (N = {n_muestra})', fontsize=11, fontweight='bold')
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
    # SECCIÓN 1: PARÁMETROS Y CONTROL SÍNCRONO
    # ==========================================
    st.subheader("Parametros de la distribucion")
    
    col_izq_p, col_der_n = st.columns([1.5, 1.5], gap="large")
    
    with col_izq_p:
        parrafo_adaptable("Ajusta la probabilidad de exito (p):")
        st.slider(
            "Probabilidad",
            min_value=0.0, max_value=1.0, step=0.01,
            key='slider_p',
            on_change=actualizar_desde_slider,
            label_visibility="collapsed"
        )

        col_txt, col_inp = st.columns([1.5, 1])
        with col_txt:
            st.write("O ingresa p manualmente:")
        with col_inp:
            st.number_input(
                "Valor p",
                min_value=0.0, max_value=1.0, step=0.01,
                key='input_p',
                on_change=actualizar_desde_input,
                label_visibility="collapsed"
            )

    with col_der_n:
        parrafo_adaptable("Control de la muestra global:")
        # Input numérico para sincronizar con la variable global compartida en st.session_state
        n_actual = st.number_input(
            "Tamaño de muestra global (N)",
            min_value=10, max_value=100000, step=10,
            key='tamano_muestra'
        )
        
        # Botón para generar tamaño de muestra aleatorio coordinado
        if st.button("Generar datos aleatorios de muestra", use_container_width=True):
            n_aleatorio = int(np.random.randint(100, 10001))
            st.session_state['tamano_muestra'] = n_aleatorio
            st.rerun()

    p_final = st.session_state['p_base']
    q_final = 1.0 - p_final
    varianza = p_final * q_final
    n_muestra_final = st.session_state['tamano_muestra']

    st.markdown("---")

    # ==========================================
    # SECCIÓN 2: RESULTADOS Y SIMULACIÓN
    # ==========================================
    st.subheader("Resultados de la Simulación")
    
    # Menú de selección dinámico para alternar y trasponer gráficas
    tipo_grafica_seleccionada = st.radio(
        "Selecciona el enfoque visual de la grafica:",
        ["Muestra Simulada", "Distribucion Teorica", "Superponer Ambas"],
        index=0,
        horizontal=True
    )

    col_izq_sup, col_der_sup = st.columns([1.1, 1.9], gap="large")
    
    # Generamos los datos numéricos crudos indispensables
    datos_raw, exitos_sim, fracasos_sim = generar_muestra_datos(p_final, q_final, n_muestra_final)
    
    # Mandamos llamar la función para renderizar la gráfica específica elegida por el usuario
    figura = generar_grafica_seleccionada(p_final, q_final, n_muestra_final, exitos_sim, fracasos_sim, tipo_grafica_seleccionada)

    p_simulada = exitos_sim / n_muestra_final
    q_simulada = fracasos_sim / n_muestra_final

    dif_p = abs(p_final - p_simulada)
    dif_q = abs(q_final - q_simulada)

    with col_izq_sup:
        st.write("### Indicadores Teoricos")
        st.metric("Prob. Fracaso (q)", f"{q_final:.4f}")
        st.metric("Esperanza (mu)", f"{p_final:.4f}")
        st.metric("Varianza (sigma2)", f"{varianza:.4f}")

    with col_der_sup:
        st.write("### Simulacion Visual")
        st.pyplot(figura, use_container_width=True)

    st.markdown("##") 
    st.divider()

    # Fila inferior: Interpretación y Tabla comparativa frente a Herramientas
    col_izq_inf, col_der_inf = st.columns([1.3, 1.7], gap="large")

    with col_izq_inf:
        st.write("### Interpretación y Comparación")
        st.write(f"Probabilidad de exito (p): **{p_final:.2%}**")
        st.write(f"Probabilidad de fracaso (q): **{q_final:.2%}**")
        st.write(f"Tamaño de muestra activo (N): **{n_muestra_final:,}**")
        
        st.write("**Tabla Comparativa e Historial de Diferencias:**")
        datos_tabla = {
            "Metrica": ["Exito (p)", "Fracaso (q)"],
            "Valor Teorico": [f"{p_final:.4f}", f"{q_final:.4f}"],
            "Valor Simulado": [f"{p_simulada:.4f}", f"{q_simulada:.4f}"],
            "Diferencia Absoluta": [f"{dif_p:.4f}", f"{dif_q:.4f}"]
        }
        df_comparativo = pd.DataFrame(datos_tabla)
        st.dataframe(df_comparativo, hide_index=True, use_container_width=True)

    with col_der_inf:
        st.write("### Herramientas y Reportes")

        with st.expander("Ver Formulas Teoricas"):
            st.latex(r"p + q = 1 \quad \lhd \quad \mu = p")
            st.latex(r"\sigma^2 = p \cdot q \quad \lhd \quad P(X = x) = p^x q^{1-x}")

        df_descarga = pd.DataFrame(datos_raw, columns=["Resultado_Simulacion"])
        csv_data = df_descarga.to_csv(index=True, index_label="Iteracion")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                label="Descargar CSV",
                data=csv_data,
                file_name=f"simulacion_bernoulli_{p_final:.2f}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col_btn2:
            reporte_texto = (
                f"REPORTE DE LABORATORIO - DISTRIBUCION DE BERNOULLI\n"
                f"--------------------------------------------------\n"
                f"Probabilidad de Exito Teorica (p): {p_final:.4f}\n"
                f"Probabilidad de Fracaso Teorica (q): {q_final:.4f}\n"
                f"Esperanza Matematica (mu): {p_final:.4f}\n"
                f"Varianza Teorica (sigma2): {varianza:.4f}\n\n"
                f"RESULTADOS Y DESVIACIONES DE LA SIMULACION (N = {n_muestra_final})\n"
                f"--------------------------------------------------\n"
                f"Frecuencia Absoluta Exitos: {exitos_sim}\n"
                f"Frecuencia Absoluta Fracasos: {fracasos_sim}\n"
                f"Proporcion de Exitos Simulada: {p_simulada:.4f} (Diferencia: {dif_p:.4f})\n"
                f"Proporcion de Fracasos Simulada: {q_simulada:.4f} (Diferencia: {dif_q:.4f})"
            )
            st.download_button(
                label="Descargar TXT",
                data=reporte_texto,
                file_name=f"reporte_bernoulli_{p_final:.2f}.txt",
                mime="text/plain",
                use_container_width=True
            )