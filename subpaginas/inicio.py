import os
import sys

# Esto encuentra la ruta raíz del proyecto y le dice a Python que busque ahí
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Ahora sí, puedes importar sin que el servidor se pierda
from css.estilos import titulo_rosa, parrafo_adaptable
def mostrar_inicio():
    # Usamos la función para el título
    titulo_rosa("Inicio")
    
    # Usamos la función para los párrafos
    parrafo_adaptable("Seleccione la distribución que desea simular en las pestañas superiores. Ajuste el tamaño de la muestra en la barra lateral para ver cómo afecta a las distribuciones.")
    
    parrafo_adaptable("Seleccione <strong>Guardar</strong> para ver o descargar aquí las simulaciones deseadas.")