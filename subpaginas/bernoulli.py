# subpaginas/bernoulli.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_bernoulli():
    titulo_rosa("Distribución de Bernoulli")
    parrafo_adaptable(
        "Un experimento de Bernoulli es un proceso estadístico con dos posibles resultados: "
        "<strong>Éxito</strong> (1) o <strong>Fracaso</strong> (0)."
    )

def mostrar_bernoulli():
    intro_bernoulli()
    st.markdown("---")
    
    # 1. Sincronización bidireccional para el parámetro 'p'
    if 'p_bernoulli' not in st.session_state:
        st.session_state['p_bernoulli'] = 0.5

    # Funciones Callback para mantener ambos controles iguales
    def cambiar_slider():
        st.session_state['p_bernoulli'] = st.session_state['slider_p']

    def cambiar_numero():
        # Limitar el valor entre 0 y 1 por seguridad
        val = st.session_state['num_p']
        st.session_state['p_bernoulli'] = min(max(val, 0.0), 1.0)

    # 2. CREAR COLUMNAS RESPONSIVAS (Izquierda: Parámetros, Derecha: Gráfica)
    col_izquierda, col_derecha = st.columns([1, 1])
    
    with col_izquierda:
        st.subheader("⚙️ Parámetros")
        
        # Entrada manual (Input numérico)
        p_num = st.number_input(
            "**Ingresa p manualmente (0.0 a 1.0):**",
            min_value=0.0, max_value=1.0, step=0.01,
            key='num_p', on_change=cambiar_numero,
            value=st.session_state['p_bernoulli']
        )
        
        # Deslizador (Slider)
        p_slide = st.slider(
            "**O selecciona con la barra:**",
            min_value=0.0, max_value=1.0, step=0.01,
            key='slider_p', on_change=cambiar_slider,
            value=st.session_state['p_bernoulli']
        )
        
        # El valor final que usaremos para los cálculos
        p_final = st.session_state['p_bernoulli']
        q_final = 1.0 - p_final
        varianza = p_final * q_final
        
        st.markdown("### 📊 Indicadores Teóricos")
        st.write(f"**Probabilidad de Fracaso ($q$):** {q_final:.4f}")
        st.write(f"**Esperanza Matemática ($E[X]$ / $\mu$):** {p_final:.4f}")
        st.write(f"**Varianza ($\sigma^2$):** {varianza:.4f}")

    with col_derecha:
        st.subheader("📈 Simulación Visual")
        
        # Recuperamos el tamaño de muestra global
        n_muestra = st.session_state.get('tamano_muestra', 1000)
        
        # Simulación de datos
        datos_simulados = np.random.choice([0, 1], size=n_muestra, p=[q_final, p_final])
        exitos = np.sum(datos_simulados == 1)
        fracasos = np.sum(datos_simulados == 0)
        
        # Construcción de la gráfica
        fig, ax = plt.subplots(figsize=(5, 3.8))
        categorias = ['Fracaso (0)', 'Éxito (1)']
        conteos = [fracasos, exitos]
        
        ax.bar(categorias, conteos, color=['#31333F', '#FF69B4'], width=0.4)
        ax.set_ylabel('Frecuencia Absoluta')
        ax.set_title(f'Resultados para N = {n_muestra}')
        
        # Asegura que las etiquetas no se corten
        plt.tight_layout() 
        st.pyplot(fig)