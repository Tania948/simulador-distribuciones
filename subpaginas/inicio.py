# subpaginas/inicio.py
import streamlit as st
from css.estilos import titulo_rosa, parrafo_adaptable

def mostrar_inicio():
    # Usamos la función para el título
    titulo_rosa("Inicio")
    
    # Usamos la función para los párrafos
    parrafo_adaptable("Seleccione la distribución que desea simular en las pestañas superiores. Ajuste el tamaño de la muestra en la barra lateral para ver cómo afecta a las distribuciones.")
    
    parrafo_adaptable("Seleccione <strong>Guardar</strong> para ver o descargar aquí las simulaciones deseadas.")