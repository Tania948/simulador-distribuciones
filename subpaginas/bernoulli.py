# subpaginas/bernoulli.py
import streamlit as st
import numpy as np
import matplotlib.subplots as plots  # Cambiado para evitar conflictos de nombres
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_bernoulli():
    """Muestra el título de la página y la introducción teórica."""
    titulo_rosa("Distribución de Bernoulli")
    parrafo_adaptable(
        "Un experimento de Bernoulli es un proceso estadístico con dos posibles resultados: "
        "<strong>Éxito</strong> (1) o <strong>Fracaso</strong> (0). Es la base para distribuciones más complejas."
    )

def inicializar_estado():
    """Garantiza que la variable central exista en el session_state."""
    if 'p_bernoulli' not in st.session_state:
        st.session_state['p_bernoulli'] = 0.30

def renderizar_controles():
    """
    Muestra el slider y el input numérico amarrados a la misma llave.
    Retorna el valor actual de p seleccionado.
    """
    st.subheader("⚙️ Parámetros de la distribución")
    parrafo_adaptable("Ajusta la probabilidad de éxito (p):")

    # CONTROL A: Slider (Comparte la misma key exacta)
    st.slider(
        "Selecciona con la barra:",
        min_value=0.0, max_value=1.0, step=0.01,
        key='p_bernoulli',  # <-- LLAVE IDÉNTICA
        label_visibility="collapsed"
    )
    
    # CONTROL B: Entrada manual discreta (Comparte la misma key exacta)
    col_txt, col_inp = st.columns([2, 1])
    with col_txt:
        st.write("**O ingresa p manualmente:**")
    with col_inp:
        st.number_input(
            "Input numérico discreto",
            min_value=0.0, max_value=1.0, step=0.01,
            key='p_bernoulli',  # <-- LLAVE IDÉNTICA
            label_visibility="collapsed"
        )
    
    # Retornamos el valor unificado directo de la memoria
    return st.session_state['p_bernoulli']

def mostrar_indicadores(p, q, varianza):
    """Renderiza las tarjetas con las métricas teóricas calculadas."""
    st.markdown("### 📊 Indicadores Teóricos")
    col_ind1, col_ind2, col_ind3 = st.columns(3)
    with col_ind1:
        st.metric(label="Pr. Fracaso (q)", value=f"{q:.4f}")
    with col_ind2:
        st.metric(label="Esperanza (μ)", value=f"{p:.4f}")
    with col_ind3:
        st.metric(label="Varianza (σ²)", value=f"{varianza:.4f}")

def generar_grafica(p, q):
    """Crea la simulación estadística y dibuja la gráfica de barras."""
    st.subheader("📈 Simulación Visual")
    
    # Recuperamos la muestra global N de app.py
    n_muestra = st.session_state.get('tamano_muestra', 1000)
    
    # Simulación aleatoria
    datos_simulados = np.random.choice([0, 1], size=n_muestra, p=[q, p])
    exitos = np.sum(datos_simulados == 1)
    fracasos = np.sum(datos_simulados == 0)
    
    # Construcción del gráfico con Matplotlib
    fig, ax = plots.subplots(figsize=(5, 3.8))
    categorias = ['Fracaso (0)', 'Éxito (1)']
    conteos = [fracasos, exitos]
    
    ax.bar(categorias, conteos, color=['#31333F', '#FF69B4'], width=0.45)
    ax.set_ylabel('Frecuencia Absoluta', fontsize=10)
    ax.set_title(f'Resultados para N = {n_muestra}', fontsize=11, fontweight='bold')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plots.tight_layout()
    st.pyplot(fig)

def inicializar_bernoulli():
    """Función principal que coordina los módulos de la página."""
    # 1. Cabecera e inicialización
    intro_bernoulli()
    st.markdown("---")
    inicializar_estado()
    
    # 2. Render de estructura de dos columnas de Streamlit
    col_izquierda, col_derecha = st.columns([1.2, 1], gap="large")
    
    with col_izquierda:
        # Ejecuta controles y extrae el valor unificado de p
        p_final = renderizar_controles()
        
        # Cálculos matemáticos básicos
        q_final = 1.0 - p_final
        varianza = p_final * q_final
        
        # Muestra métricas
        mostrar_indicadores(p_final, q_final, varianza)

    with col_derecha:
        # Dibuja la gráfica a la misma altura
        generar_grafica(p_final, q_final)