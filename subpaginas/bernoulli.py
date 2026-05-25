# subpaginas/bernoulli.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_bernoulli():
    """Muestra el título de la página y la introducción teórica."""
    titulo_rosa("Distribución de Bernoulli")
    parrafo_adaptable(
        "Un experimento de Bernoulli es un proceso estadístico con dos posibles resultados: "
        "<strong>Éxito</strong> (1) o <strong>Fracaso</strong> (0). Es la base para distribuciones más complejas."
    )

def inicializar_estado():
    """Garantiza que las variables de control existan con el valor inicial base."""
    if 'p_base' not in st.session_state:
        st.session_state['p_base'] = 0.30
    
    # Sincronizamos las variables del slider e input por primera vez
    if 'slider_p' not in st.session_state:
        st.session_state['slider_p'] = st.session_state['p_base']
    if 'input_p' not in st.session_state:
        st.session_state['input_p'] = st.session_state['p_base']

def actualizar_desde_slider():
    """Se ejecuta al mover la barra: actualiza la base y el cuadro numérico."""
    st.session_state['p_base'] = st.session_state['slider_p']
    st.session_state['input_p'] = st.session_state['slider_p']

def actualizar_desde_input():
    """Se ejecuta al teclear un número: actualiza la base y desplaza la barra."""
    val = st.session_state['input_p']
    # Restringimos de forma segura al rango de probabilidad [0.0, 1.0]
    val_validado = min(max(val, 0.0), 1.0)
    
    st.session_state['p_base'] = val_validado
    st.session_state['slider_p'] = val_validado

def renderizar_controles():
    """
    Dibuja los controles enlazados de forma cruzada.
    Retorna el valor final coordinado.
    """
    st.subheader("⚙️ Parámetros de la distribución")
    parrafo_adaptable("Ajusta la probabilidad de éxito (p):")

    # CONTROL A: Slider con llave única y callback de actualización
    st.slider(
        "Selecciona con la barra:",
        min_value=0.0, max_value=1.0, step=0.01,
        key='slider_p',
        on_change=actualizar_desde_slider,
        label_visibility="collapsed"
    )
    
    # CONTROL B: Entrada manual con otra llave única y callback de actualización
    col_txt, col_inp = st.columns([2, 1])
    with col_txt:
        st.write("**O ingresa p manualmente:**")
    with col_inp:
        st.number_input(
            "Input numérico discreto",
            min_value=0.0, max_value=1.0, step=0.01,
            key='input_p',
            on_change=actualizar_desde_input,
            label_visibility="collapsed"
        )
    
    # Retornamos el valor madre unificado
    return st.session_state['p_base']

def mostrar_indicadores(p, q, varianza):
    """Renderiza las tarjetas con las métricas teóricas."""
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
    
    # Gráfica en Matplotlib
    fig, ax = plt.subplots(figsize=(5, 3.8))
    categorias = ['Fracaso (0)', 'Éxito (1)']
    conteos = [fracasos, exitos]
    
    ax.bar(categorias, conteos, color=['#31333F', '#FF69B4'], width=0.45)
    ax.set_ylabel('Frecuencia Absoluta', fontsize=10)
    ax.set_title(f'Resultados para N = {n_muestra}', fontsize=11, fontweight='bold')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def inicializar_bernoulli():
    """Función principal con comportamiento responsivo tipo Media Query mediante Flexbox."""
    intro_bernoulli()
    st.markdown("---")
    inicializar_estado()
    
    # 1. Calculamos los datos primero (Lógica pura)
    p_final = renderizar_controles()
    q_final = 1.0 - p_final
    varianza = p_final * q_final

    # 2. Maquetación Responsiva con CSS Flexbox
    # Creamos un contenedor que permite que sus hijos se bajen (wrap) si el espacio mide menos de 450px
    st.markdown("""
        <style>
        .contenedor-responsivo {
            display: flex;
            flex-wrap: wrap;
            gap: 40px;
            width: 100%;
        }
        .columna-bloque {
            flex: 1 1 450px; /* Crece si hay espacio, pero si baja de 450px se envuelve abajo */
            min-width: 300px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Abrimos el contenedor flex principal
    st.markdown('<div class="contenedor-responsivo">', unsafe_allow_html=True)
    
    # --- COLUMNA IZQUIERDA (Controles e Indicadores) ---
    st.markdown('<div class="columna-bloque">', unsafe_allow_html=True)
    # Volvemos a llamar a renderizar_controles pero de forma visual en la columna izquierda
    # (Como ya se ejecutó arriba, session_state ya está al día, aquí solo se dibuja)
    mostrar_indicadores(p_final, q_final, varianza)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- COLUMNA DERECHA (Gráfica) ---
    st.markdown('<div class="columna-bloque">', unsafe_allow_html=True)
    generar_grafica(p_final, q_final)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Cerramos el contenedor principal
    st.markdown('</div>', unsafe_allow_html=True)