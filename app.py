import streamlit as st

# 1. Configuración de la interfaz
st.set_page_config(page_title="Simulador Estadístico", layout="wide")
st.title("📊 Simulador de Distribuciones - Probabilidad y estadistica")

# 2. Menú de navegación en la barra lateral
st.sidebar.header("Navegación")
opcion = st.sidebar.selectbox(
    "Selecciona una Distribución",
    ["Inicio", "Binomial (Discreta)", "Poisson (Discreta)", "Normal (Continua)"]
)

# 3. Enrutador (Home)
if opcion == "Inicio":
    st.write("Bienvenido al simulador. Selecciona una distribución en el menú de la izquierda para comenzar.")

elif opcion == "Binomial (Discreta)":
    # Aquí llamaremos al módulo modular más adelante
    st.subheader("Módulo de la Distribución Binomial")
    st.info("Espacio para conectar el archivo binomial.py")

elif opcion == "Poisson (Discreta)":
    st.subheader("Módulo de la Distribución Poisson")
    st.info("Espacio para conectar el archivo poisson.py")

elif opcion == "Normal (Continua)":
    st.subheader("Módulo de la Distribución Normal")
    st.info("Espacio para conectar el archivo normal.py")
