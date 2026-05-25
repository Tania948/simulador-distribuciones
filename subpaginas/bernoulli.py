import streamlit as st
from css.estilos import titulo_rosa, parrafo_adaptable

def intro_bernoulli():
    titulo_rosa("Distribución de Bernoulli")
    parrafo_adaptable("La distribución de Bernoulli es una distribución de probabilidad discreta que describe un experimento con dos posibles resultados: éxito (1) o fracaso (0). Es la base para otras distribuciones como la binomial y la geométrica.")

def inicializar_bernoulli():
    intro_bernoulli()