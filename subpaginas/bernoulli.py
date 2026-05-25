# subpaginas/bernoulli.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_bernoulli():
    titulo_rosa("Distribución de Bernoulli")
    parrafo_adaptable(
        "Un experimento de Bernoulli es un proceso estadístico con dos posibles resultados: "
        "<strong>Éxito</strong> (1) o <strong>Fracaso</strong> (0). Es la base para distribuciones más complejas "
        "como la Binomial."
    )

def mostrar_grafica_y_metricas(p, q, n_muestra):
    # 1. Cálculos teóricos básicos
    media = p
    varianza = p * q
    
    # Mostrar métricas en tarjetas bonitas lado a lado
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Probabilidad de Fracaso (q)", value=f"{q:.4f}")
    with col2:
        st.metric(label="Media (μ)", value=f"{media:.4f}")
    with col3:
        st.metric(label="Varianza (σ²)", value=f"{varianza:.4f}")
        
    st.markdown("---")
    
    # 2. Simulación con el tamaño de muestra de la barra lateral
    # Generamos los datos simulados (0s y 1s) basados en la probabilidad p
    datos_simulados = np.random.choice([0, 1], size=n_muestra, p=[q, p])
    
    # Contamos cuántos éxitos y fracasos hubo en la simulación
    exitos = np.sum(datos_simulados == 1)
    fracasos = np.sum(datos_simulados == 0)
    
    # Crear gráfica de barras con Matplotlib (o Plotly/Altair si prefieren)
    fig, ax = plt.subplots(figsize=(6, 4))
    categorias = ['Fracaso (0)', 'Éxito (1)']
    conteos = [fracasos, exitos]
    
    # Diseñamos las barras con tu color rosa de identidad
    ax.bar(categorias, conteos, color=['#31333F', '#FF69B4'], width=0.5)
    ax.set_ylabel('Frecuencia Absoluta')
    ax.set_title(f'Simulación de Bernoulli con N = {n_muestra}')
    
    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)

def mostrar_bernoulli():
    # Mandamos a llamar la introducción
    intro_bernoulli()
    
    st.markdown("---")
    
    # Solicitar parámetros de forma segura
    st.subheader("⚙️ Parámetros de la distribución")
    p = st.slider("**Selecciona la probabilidad de éxito (p):**", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    q = 1.0 - p
    
    # Recuperamos el tamaño de muestra global que guardaste en app.py
    n_muestra = st.session_state.get('tamano_muestra', 1000)
    
    # Mostramos los resultados visuales y matemáticos
    mostrar_grafica_y_metricas(p, q, n_muestra)