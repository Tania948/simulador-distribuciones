# subpaginas/bernoulli.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_bernoulli():
    titulo_rosa("Distribución de Bernoulli")
    parrafo_adaptable(
        "Un experimento de Bernoulli es un proceso estadístico con dos posibles resultados: "
        "<strong>Éxito</strong> (1) o <strong>Fracaso</strong> (0). Es la base para distribuciones más complejas."
    )

def inicializar_bernoulli():
    # 1. Introducción
    intro_bernoulli()
    st.markdown("---")
    
    # 2. Sincronización bidireccional para el parámetro 'p' en session_state
    if 'p_bernoulli' not in st.session_state:
        st.session_state['p_bernoulli'] = 0.5  # Valor inicial por defecto

    # Funciones Callback para mantener ambos controles iguales
    def cambiar_slider():
        st.session_state['p_bernoulli'] = st.session_state['slider_p']

    def cambiar_numero():
        # Limitar el valor entre 0 y 1 por seguridad
        val = st.session_state['num_p']
        st.session_state['p_bernoulli'] = min(max(val, 0.0), 1.0)

    # 3. SECCIÓN DE PARÁMETROS (ARRIBA)
    # Centramos un contenedor para que no se vea tan estirado en pantallas gigantes
    with st.container():
        col_centro_params = st.columns([1, 4, 1]) # Columnas para centrar el bloque de parámetros
        with col_centro_params[1]:
            st.subheader("⚙️ Parámetros de la distribución")
            
            parrafo_adaptable("Ajusta la probabilidad de éxito (p). Es más probable que uses la barra:")

            # CONTROL PRINCIPAL: Deslizador (Slider) - Ahora arriba
            st.slider(
                "**Selecciona con la barra:**",
                min_value=0.0, max_value=1.0, step=0.01,
                key='slider_p', on_change=cambiar_slider,
                value=st.session_state['p_bernoulli']
            )
            
            # CONTROL SECUNDARIO: Entrada manual (Pequeño cuadradito) - Ahora abajo y discreto
            # Usamos un contenedor horizontal pequeño para meter el label y el input juntos
            col_label_discreto, col_input_discreto = st.columns([2, 1])
            with col_label_discreto:
                # Usamos st.write en lugar de la etiqueta del input para un control total
                st.write("**O ingresa p manualmente:**")
            
            with col_input_discreto:
                # El truco es 'label_visibility="collapsed"' para quitar la etiqueta ostentosa
                st.number_input(
                    "O ingresa p manualmente (etiqueta colapsada):", # El texto aquí ya no se ve
                    min_value=0.0, max_value=1.0, step=0.01,
                    key='num_p', on_change=cambiar_numero,
                    value=st.session_state['p_bernoulli'],
                    label_visibility="collapsed" # <-- ESTE ES EL TRUCO
                )

            # Cálculos teóricos finales
            p_final = st.session_state['p_bernoulli']
            q_final = 1.0 - p_final
            varianza = p_final * q_final
            
            # Indicadores Teóricos
            st.markdown("### 📊 Indicadores Teóricos")
            col_ind1, col_ind2, col_ind3 = st.columns(3)
            with col_ind1:
                st.metric(label="Pr. de Fracaso (q)", value=f"{q_final:.4f}")
            with col_ind2:
                # Esperanza = Media = p
                st.metric(label="Esperanza (E[X] / μ)", value=f"{p_final:.4f}")
            with col_ind3:
                st.metric(label="Varianza (σ²)", value=f"{varianza:.4f}")

    st.markdown("---")
    
    # 4. SECCIÓN DE GRÁFICA (ABAJO)
    with st.container():
        st.subheader("📈 Simulación Visual")
        
        # Recuperamos el tamaño de muestra global (N) de app.py
        n_muestra = st.session_state.get('tamano_muestra', 1000)
        
        # Simulación de datos
        datos_simulados = np.random.choice([0, 1], size=n_muestra, p=[q_final, p_final])
        exitos = np.sum(datos_simulados == 1)
        fracasos = np.sum(datos_simulados == 0)
        
        # Construcción de la gráfica
        fig, ax = plt.subplots(figsize=(6, 4)) # Un tamaño un poco mayor para que se vea bien apilada
        categorias = ['Fracaso (0)', 'Éxito (1)']
        conteos = [fracasos, exitos]
        
        # Usamos tus colores corporativos (gris oscuro y rosa)
        ax.bar(categorias, conteos, color=['#31333F', '#FF69B4'], width=0.5)
        ax.set_ylabel('Frecuencia Absoluta')
        ax.set_title(f'Resultados de la simulación para N = {n_muestra}')
        
        # Centrar la gráfica y evitar recortes
        plt.tight_layout() 
        
        # Usamos columnas fantasmas para centrar la gráfica en la página
        col_centro_grafica = st.columns([1, 4, 1])
        with col_centro_grafica[1]:
            st.pyplot(fig)