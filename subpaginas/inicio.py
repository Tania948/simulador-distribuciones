import streamlit as st
# IMPORTACIÓN CORREGIDA: Ruta directa desde la raíz que entiende Streamlit Cloud
from css.estilos import aplicar_estilos_inicio, titulo_rosa, parrafo_adaptable

def textoIntro():
    # Usamos tus funciones de estilos pasándole solo el texto
    titulo_rosa("Inicio")
    
    parrafo_adaptable(
        "Seleccione la distribución que desea simular en las pestañas superiores. "
        "Ajuste el tamaño de la muestra en la barra lateral para ver cómo afecta a las distribuciones."
    )
    
    parrafo_adaptable(
        "Seleccione <strong>Guardar</strong> para ver o descargar aquí las simulaciones deseadas."
    )

def inicioMostrar():
    aplicar_estilos_inicio()  # Prepara la tipografía y el modo oscuro
    textoIntro()             # Muestra tus textos limpios