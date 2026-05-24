import streamlit as st

# Fondo
st.set_page_config(page_title="Simulador Estadístico", layout="wide")
st.title("Simulador de Distribuciones - Probabilidad y estadistica")

# Menu de opciones
st.sidebar.title("Selecciona una distribución")
distribucion = st.sidebar.selectbox
("Tipo de distribución", ["Bernoulli", 
                          "Binomial",
                          "Geometrica",
                          "Hipergeometrica",
                          "Poisson"])



