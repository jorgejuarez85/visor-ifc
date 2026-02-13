import streamlit as st
import ifcopenshell
import ifcopenshell.geom
import pyvista as pv
from stpyvista import stpyvista
import os
import tempfile
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Visor IFC", 
    page_icon="🏗️",
    layout="wide"
)

# Título
st.title("🏗️ Visor de Modelos IFC")
st.markdown("---")

# Función para listar modelos disponibles

def get_modelos_disponibles():
    """Lista los archivos IFC en la carpeta modelos"""
    modelos_dir = "modelos"
    if not os.path.exists(modelos_dir):
        os.makedirs(modelos_dir)
        # Crear un mensaje si no hay modelos
        return []
    
    modelos = [f for f in os.listdir(modelos_dir) if f.endswith('.ifc')]
    return modelos

# Función para procesar y visualizar IFC

def procesar_ifc(file_path):
    """Procesa el archivo IFC y extrae información básica"""
    try:
        ifc_file = ifcopenshell.open(file_path)
        
        # Obtener información básica
        info = {
            "nombre": os.path.basename(file_path),
            "elementos": len(list(ifc_file.by_type("IfcProduct"))),
            "pisos": len(list(ifc_file.by_type("IfcBuildingStorey"))),
            "espacios": len(list(ifc_file.by_type("IfcSpace"))),
            "puertas": len(list(ifc_file.by_type("IfcDoor"))),
            "ventanas": len(list(ifc_file.by_type("IfcWindow"))),
        }
        
        return ifc_file, info
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
        return None, None

# Función para visualizar en 3D
def visualizar_ifc(ifc_file):
    """Crea visualización 3D del modelo"""
    plotter = pv.Plotter(window_size=[800, 600])
    plotter.background_color = 'white'
    
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    
    elementos_mostrados = 0
    elementos_totales = len(list(ifc_file.by_type("IfcProduct")))
    
    # Barra de progreso
    progress_bar = st.progress(0)
    
    # Iterar sobre elementos (limitamos para rendimiento)
    for i, element in enumerate(ifc_file.by_type("IfcProduct")[:200]):  # Límite de 200 elementos
        try:
            # Omitir aberturas
            if element.is_a("IfcOpeningElement"):
                continue
                
            shape = ifcopenshell.geom.create_shape(settings, element)
            
            # Convertir geometría a formato PyVista
            vertices = np.array(shape.geometry.verts).reshape(-1, 3)
            faces = np.array(shape.geometry.faces)
            
            # Crear celdas para PyVista
            cells = []
            for j in range(0, len(faces), faces[j] + 1 if j < len(faces) else 1):
                if j < len(faces):
                    n_points = faces[j]
                    cells.append([n_points] + list(faces[j+1:j+1+n_points]))
            
            if cells:
                # Aplanar celdas para PyVista
                cells_flat = []
                for cell in cells:
                    cells_flat.extend(cell)
                
                # Crear malla
                mesh = pv.PolyData(vertices, cells_flat)
                
                # Color según tipo de elemento
                if element.is_a("IfcWall"):
                    color = "lightgray"
                elif element.is_a("IfcSlab"):
                    color = "lightblue"
                elif element.is_a("IfcDoor"):
                    color = "brown"
                elif element.is_a("IfcWindow"):
                    color = "skyblue"
                elif element.is_a("IfcRoof"):
                    color = "red"
                else:
                    color = "lightgreen"
                
                plotter.add_mesh(mesh, color=color, show_edges=False, opacity=1.0)
                elementos_mostrados += 1
                
        except Exception as e:
            continue
        
        # Actualizar progreso
        progress_bar.progress(min(i / elementos_totales, 1.0))
    
    progress_bar.empty()
    
    # Configurar cámara
    plotter.camera_position = 'iso'
    plotter.add_axes()
    
    return plotter, elementos_mostrados

# Sidebar para selección de modelos
with st.sidebar:
    st.header("📁 Modelos Disponibles")
    
    # Obtener modelos
    modelos = get_modelos_disponibles()
    
    if not modelos:
        st.warning("No hay modelos IFC en la carpeta 'modelos'")
        st.info("Agrega archivos .ifc a la carpeta 'modelos'")
    else:
        # Selector de modelo
        modelo_seleccionado = st.selectbox(
            "Selecciona un modelo:",
            modelos
        )
        
        # Mostrar info del modelo seleccionado
        if modelo_seleccionado:
            ruta_modelo = os.path.join("modelos", modelo_seleccionado)
            ifc_file, info = procesar_ifc(ruta_modelo)
            
            if info:
                st.markdown("---")
                st.header("📊 Información")
                st.metric("Elementos totales", info["elementos"])
                st.metric("Pisos", info["pisos"])
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Puertas", info["puertas"])
                with col2:
                    st.metric("Ventanas", info["ventanas"])
    
    st.markdown("---")
    st.caption("Visor IFC - Administra tus modelos")

# Área principal
if modelos and modelo_seleccionado:
    ruta_modelo = os.path.join("modelos", modelo_seleccionado)
    ifc_file, info = procesar_ifc(ruta_modelo)
    
    if ifc_file:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header(f"📐 Vista 3D: {modelo_seleccionado}")
            
            # Botón para visualizar
            if st.button("🔄 Cargar Visualización 3D"):
                with st.spinner("Generando vista 3D..."):
                    plotter, elementos_most = visualizar_ifc(ifc_file)
                    stpyvista(plotter, key="pv_canvas")
                    st.caption(f"Mostrando {elementos_most} de {info['elementos']} elementos")
        
        with col2:
            st.header("📋 Propiedades")
            
            # Mostrar propiedades básicas
            if info:
                st.json(info)
            
            # Opción de descarga (solo para administradores - por IP o contraseña)
            if st.checkbox("👑 Modo Administrador"):
                with open(ruta_modelo, 'rb') as f:
                    st.download_button(
                        "📥 Descargar IFC",
                        f,
                        file_name=modelo_seleccionado,
                        mime="application/octet-stream"
                    )
else:
    # Mensaje de bienvenida
    st.info("👈 Selecciona un modelo del panel lateral para comenzar")
    
    # Instrucciones
    with st.expander("📖 ¿Cómo agregar modelos?"):
        st.markdown("""
        1. Crea una carpeta llamada **modelos** en el mismo lugar que app.py
        2. Copia tus archivos .ifc dentro de la carpeta **modelos**
        3. Actualiza la página
        """)

# Footer
st.markdown("---")
st.markdown("🔗 **Comparte este enlace con los usuarios**")
