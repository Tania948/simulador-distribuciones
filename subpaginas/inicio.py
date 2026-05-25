import streamlit as st
# Importamos las herramientas de diseño desde el módulo centralizado
from css.estilos import preparar_pantalla, titulo_rosa, parrafo_adaptable

def textoIntro():
    # Usamos las funciones de diseño pasándole solo el texto limpio
    titulo_rosa("Inicio")
    
    parrafo_adaptable(
        "Seleccione la distribución que desea simular en las pestañas superiores. "
        "Ajuste el tamaño de la muestra en la barra lateral para ver cómo afecta a las distribuciones."
    )
    
    parrafo_adaptable(
        "Seleccione <strong>Guardar</strong> para ver o descargar aquí las simulaciones deseadas."
    )

def inicioMostrar():
    preparar_pantalla()  # Carga las reglas CSS de fondo
    textoIntro()         # Pinta la información