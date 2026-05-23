import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Configuración de la página del simulador
st.set_page_config(page_title="Simulador de Distribuciones", layout="wide")

st.title("📊 Simulador de Distribuciones de Probabilidad y Visualizaciones Gráficas")
st.markdown("""
Este simulador permite generar datos aleatorios basados en diferentes distribuciones de probabilidad, 
calculando sus estadísticos empíricos y comparándolos directamente con el modelo teórico.
""")

# ==========================================
# BARRA LATERAL: ENTRADA DE DATOS GENERALES
# ==========================================
st.sidebar.header("⚙️ Configuración General")
distribucion = st.sidebar.selectbox(
    "Selecciona una Distribución",
    ["Binomial (Discreta)", "Poisson (Discreta)", "Geométrica (Discreta)", 
     "Uniforme (Continua)", "Normal (Continua)", "Exponencial (Continua)"]
)

tamano_muestra = st.sidebar.number_input("Tamaño de Muestra (n)", min_value=1, max_value=100000, value=1000, step=500)

# Inicialización de variables para evitar errores de compilación
datos = None
m_teorica, v_teorica = 0.0, 0.0
es_discreta = True

# ==========================================
# CONFIGURACIÓN ESPECÍFICA DE CADA DISTRIBUCIÓN
# ==========================================
st.sidebar.subheader("🎯 Parámetros de la Distribución")

if "Binomial" in distribucion:
    es_discreta = True
    n_ensayos = st.sidebar.number_input("Número de ensayos (n)", min_value=1, value=10)
    p_exito = st.sidebar.slider("Probabilidad de éxito (p)", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    
    # Simulación y Teoría
    datos = np.random.binomial(n_ensayos, p_exito, tamano_muestra)
    m_teorica = n_ensayos * p_exito
    v_teorica = n_ensayos * p_exito * (1 - p_exito)
    
    # Curva Teórica (PMF)
    x_teorico = np.arange(0, n_ensayos + 1)
    linea_teorica = stats.binom.pmf(x_teorico, n_ensayos, p_exito)

elif "Poisson" in distribucion:
    es_discreta = True
    lam = st.sidebar.number_input("Parámetro Lambda (λ)", min_value=0.01, value=4.0, step=0.5)
    
    datos = np.random.poisson(lam, tamano_muestra)
    m_teorica = lam
    v_teorica = lam
    
    x_teorico = np.arange(0, int(lam + 4 * np.sqrt(lam)))
    linea_teorica = stats.poisson.pmf(x_teorico, lam)

elif "Geométrica" in distribucion:
    es_discreta = True
    p_geom = st.sidebar.slider("Probabilidad de éxito (p)", min_value=0.01, max_value=1.0, value=0.3, step=0.01)
    
    datos = np.random.geometric(p_geom, tamano_muestra)
    m_teorica = 1 / p_geom
    v_teorica = (1 - p_geom) / (p_geom ** 2)
    
    x_teorico = np.arange(1, int(m_teorica + 4 * np.sqrt(v_teorica)))
    linea_teorica = stats.geom.pmf(x_teorico, p_geom)

elif "Uniforme" in distribucion:
    es_discreta = False
    a = st.sidebar.number_input("Límite inferior (a)", value=0.0)
    b = st.sidebar.number_input("Límite superior (b)", value=10.0)
    
    if a >= b:
        st.error("⚠️ El límite superior (b) debe ser estrictamente mayor que el límite inferior (a).")
    else:
        datos = np.random.uniform(a, b, tamano_muestra)
        m_teorica = (a + b) / 2
        v_teorica = ((b - a) ** 2) / 12
        x_teorico = np.linspace(a - 1, b + 1, 500)
        linea_teorica = stats.uniform.pdf(x_teorico, a, b - a)

elif "Normal" in distribucion:
    es_discreta = False
    mu = st.sidebar.number_input("Media (μ)", value=0.0)
    sigma = st.sidebar.number_input("Desviación Estándar (σ)", min_value=0.01, value=1.0, step=0.1)
    
    datos = np.random.normal(mu, sigma, tamano_muestra)
    m_teorica = mu
    v_teorica = sigma ** 2
    x_teorico = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 500)
    linea_teorica = stats.norm.pdf(x_teorico, mu, sigma)

elif "Exponencial" in distribucion:
    es_discreta = False
    beta = st.sidebar.number_input("Parámetro de escala Beta (β = 1/λ)", min_value=0.01, value=2.0, step=0.5)
    
    datos = np.random.exponential(beta, tamano_muestra)
    m_teorica = beta
    v_teorica = beta ** 2
    x_teorico = np.linspace(0, max(datos) if datos is not None else 10, 500)
    linea_teorica = stats.expon.pdf(x_teorico, scale=beta)

# ==========================================
# RENDERIZADO DE RESULTADOS EN LA INTERFAZ
# ==========================================
if datos is not None:
    # Cálculos empíricos (Simulados)
    m_simulada = np.mean(datos)
    v_simulada = np.var(datos)
    std_teorica = np.sqrt(v_teorica)
    std_simulada = np.sqrt(v_simulada)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📈 Comparación Gráfica")
        fig, ax = plt.subplots(figsize=(7, 4.5))
        
        if es_discreta:
            # Gráfica para discretas: Barras para simulación, Stem para teoría
            valores, cuentas = np.unique(datos, return_counts=True)
            ax.bar(valores, cuentas / len(datos), alpha=0.5, color="#1f77b4", edgecolor="black", label="Simulado (Empírico)")
            ax.stem(x_teorico, linea_teorica, linefmt="#d62728", markerfmt="o", basefmt=" ", label="Teórico (PMF)")        
        else:
            # Gráfica para continuas: Histograma normalizado y curva PDF
            ax.hist(datos, bins=30, density=True, alpha=0.5, color="#2ca02c", edgecolor="black", label="Simulado (Histograma)")
            ax.plot(x_teorico, linea_teorica, color="#d62728", linewidth=2.5, label="Teórico (PDF)")
            ax.set_ylabel("Densidad de Probabilidad")
            
        ax.set_title(f"Distribución {distribucion}", fontsize=12, fontweight='bold')
        ax.set_xlabel("Variable Aleatoria (X)")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
    with col2:
        st.subheader("📋 Resultados Numéricos")
        # Tabla estructurada exactamente como la pide la rúbrica del PDF
        st.table({
            "Concepto": ["Media (Esperanza)", "Varianza", "Desviación Estándar", "Tamaño de Muestra"],
            "Valor Teórico": [round(m_teorica, 4), round(v_teorica, 4), round(std_teorica, 4), "-"],
            "Valor Simulado": [round(m_simulada, 4), round(v_simulada, 4), round(std_simulada, 4), tamano_muestra],
            "Diferencia Absorber": [round(abs(m_teorica - m_simulada), 4), round(abs(v_teorica - v_simulada), 4), round(abs(std_teorica - std_simulada), 4), "-"]
        })
        
        # Bloque automático de interpretación breve exigido por el reporte
        st.subheader("💡 Interpretación Estadística Corta")
        st.info(f"""
        Al observar la **Media Teórica ({round(m_teorica,2)})** frente a la **Media Simulada ({round(m_simulada,2)})**, 
        se comprueba la **Ley de los Grandes Números**: a medida que el tamaño de muestra aumenta ({tamano_muestra}), 
        los estadísticos de la simulación se aproximan de forma asintótica a los valores teóricos verdaderos del modelo, 
        reduciendo el error de fluctuación aleatoria.
        """)
