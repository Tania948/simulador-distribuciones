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
    intro_bernoulli()
    st.markdown("---")
    
    # 1. INICIALIZAR EL ESTADO GLOBAL DE P (Si no existe)
    if 'p_bernoulli' not in st.session_state:
        st.session_state['p_bernoulli'] = 0.30

    # 2. FUNCIONES REACTIVAS (Aseguran que un control mueva al otro al instante)
    def cambiar_desde_slider():
        st.session_state['p_bernoulli'] = st.session_state['slider_p']

    def cambiar_desde_numero():
        val = st.session_state['num_p']
        # Validamos que no se salga del rango estadístico [0.0, 1.0]
        st.session_state['p_bernoulli'] = min(max(val, 0.0), 1.0)

    # El valor unificado que usaremos para renderizar y calcular
    p_actual = st.session_state['p_bernoulli']

    # 3. DISEÑO DE COLUMNAS (Sin forzar el agrupamiento en móviles)
    # Al no usar banderas raras, Streamlit por defecto baja la columna derecha si el espacio es poco
    col_izquierda, col_derecha = st.columns([1.2, 1], gap="large")
    
    with col_izquierda:
        st.subheader("⚙️ Parámetros de la distribución")
        parrafo_adaptable("Ajusta la probabilidad de éxito (p):")

        # DESLIZADOR (Su valor depende estrictamente de p_actual)
        st.slider(
            "Selecciona con la barra:",
            min_value=0.0, max_value=1.0, step=0.01,
            key='slider_p',
            value=p_actual,             # <-- Conectado al estado
            on_change=cambiar_desde_slider,
            label_visibility="collapsed"
        )
        
        # ENTRADA MANUAL (Su valor también depende estrictamente de p_actual)
        col_txt, col_inp = st.columns([2, 1])
        with col_txt:
            st.write("**O ingresa p manualmente:**")
        with col_inp:
            st.number_input(
                "Input numérico discreto",
                min_value=0.0, max_value=1.0, step=0.01,
                key='num_p',
                value=p_actual,             # <-- Conectado al estado
                on_change=cambiar_desde_numero,
                label_visibility="collapsed"
            )

        # Cálculos matemáticos limpios basados en el valor unificado
        q_final = 1.0 - p_actual
        varianza = p_actual * q_final
        
        # INDICADORES TEÓRICOS
        st.markdown("### 📊 Indicadores Teóricos")
        
        # Para evitar que las métricas se corten en "0.7..." cuando la pantalla se encoge,
        # usamos un truco: si el espacio es pequeño, mostramos las métricas de forma vertical u organizada.
        # Una excelente opción para que no se arruine el diseño es usar columnas tradicionales:
        col_ind1, col_ind2, col_ind3 = st.columns(3)
        with col_ind1:
            st.metric(label="Pr. Fracaso (q)", value=f"{q_final:.4f}")
        with col_ind2:
            st.metric(label="Esperanza (μ)", value=f"{p_actual:.4f}")
        with col_ind3:
            st.metric(label="Varianza (σ²)", value=f"{varianza:.4f}")

    with col_derecha:
        st.subheader("📈 Simulación Visual")
        
        # Recuperamos la muestra global N de la barra lateral de app.py
        n_muestra = st.session_state.get('tamano_muestra', 1000)
        
        # Simulación probabilística usando NumPy
        datos_simulados = np.random.choice([0, 1], size=n_muestra, p=[q_final, p_actual])
        exitos = np.sum(datos_simulados == 1)
        fracasos = np.sum(datos_simulados == 0)
        
        # Configuración limpia de la gráfica de barras
        fig, ax = plt.subplots(figsize=(5, 3.8))
        categorias = ['Fracaso (0)', 'Éxito (1)']
        conteos = [fracasos, exitos]
        
        # Aplicamos tus colores (Gris oscuro y Rosa ESCOM/Materia)
        ax.bar(categorias, conteos, color=['#31333F', '#FF69B4'], width=0.45)
        ax.set_ylabel('Frecuencia Absoluta', fontsize=10)
        ax.set_title(f'Resultados para N = {n_muestra}', fontsize=11, fontweight='bold')
        
        # Limpieza estética de bordes
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        st.pyplot(fig)