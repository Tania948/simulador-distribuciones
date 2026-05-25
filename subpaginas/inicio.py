import streamlit as st

# El secreto: El punto antes de 'css' le dice a Python: 
# "Salte de la carpeta 'subpaginas' y busca la carpeta 'css' en la raíz"
from ..css.estilos import aplicar_estilos_inicio, titulo_rosa, parrafo_adaptable

def textoIntro():
    # Cero HTML aquí. Solo llamadas limpias pasando el texto.
    titulo_rosa("Inicio")
    
    parrafo_adaptable(
        "Seleccione la distribución que desea simular en las pestañas superiores. "
        "Ajuste el tamaño de la muestra en la barra lateral para ver cómo afecta a las distribuciones."
    )
    
    parrafo_adaptable(
        "Seleccione <strong>Guardar</strong> para ver o descargar aquí las simulaciones deseadas."
    )

def inicioMostrar():
    aplicar_estilos_inicio()  # Prepara los estilos de la página
    textoIntro()             # Imprime los textos