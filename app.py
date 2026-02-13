import streamlit as st
import ifcopenshell
import tempfile
import os
import subprocess
import sys

st.set_page_config(page_title="Visor IFC Simplificado", layout="wide")
st.title("🏗️ Visor IFC - Versión Simplificada")

# Instalar dependencias necesarias (solo en Streamlit Cloud)
if not os.path.exists("/tmp/ifc_convertido"):
    os.makedirs("/tmp/ifc_convertido")

# Función para listar modelos
def get_modelos_disponibles():
    modelos_dir = "modelos"
    if not os.path.exists(modelos_dir):
        os.makedirs(modelos_dir)
        return []
    return [f for f in os.listdir(modelos_dir) if f.endswith('.ifc')]

# Función para obtener info del IFC
def get_ifc_info(file_path):
    try:
        ifc_file = ifcopenshell.open(file_path)
        info = {
            "elementos": len(list(ifc_file.by_type("IfcProduct"))),
            "pisos": len(list(ifc_file.by_type("IfcBuildingStorey"))),
            "puertas": len(list(ifc_file.by_type("IfcDoor"))),
            "ventanas": len(list(ifc_file.by_type("IfcWindow"))),
        }
        return info, ifc_file
    except Exception as e:
        st.error(f"Error al leer IFC: {e}")
        return None, None

# Sidebar
with st.sidebar:
    st.header("📁 Modelos")
    modelos = get_modelos_disponibles()
    
    if not modelos:
        st.warning("No hay archivos IFC en la carpeta 'modelos'")
    else:
        modelo = st.selectbox("Selecciona modelo:", modelos)
        
        if modelo:
            ruta = os.path.join("modelos", modelo)
            info, ifc_file = get_ifc_info(ruta)
            
            if info:
                st.metric("Elementos totales", info["elementos"])
                st.metric("Pisos", info["pisos"])
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Puertas", info["puertas"])
                with col2:
                    st.metric("Ventanas", info["ventanas"])

# Área principal
if modelos and modelo:
    st.header(f"📐 Modelo: {modelo}")
    
    # Mostrar información básica
    st.subheader("📊 Estadísticas del modelo")
    st.json(info)
    
    # Opciones de visualización
    st.subheader("👓 Visualización")
    
    opcion = st.radio(
        "Elige método de visualización:",
        ["Ver propiedades", "Exportar a HTML", "Ver estructura"]
    )
    
    if opcion == "Ver propiedades":
        if ifc_file:
            # Mostrar propiedades de algunos elementos
            st.write("**Primeros 5 elementos del modelo:**")
            elementos = list(ifc_file.by_type("IfcProduct"))[:5]
            for elem in elementos:
                with st.expander(f"Elemento: {elem.is_a()}"):
                    if hasattr(elem, "Name"):
                        st.write(f"Nombre: {elem.Name}")
                    if hasattr(elem, "Description"):
                        st.write(f"Descripción: {elem.Description}")
                    if hasattr(elem, "GlobalId"):
                        st.write(f"ID: {elem.GlobalId}")
    
    elif opcion == "Exportar a HTML":
        st.info("""
        Para visualización 3D completa, recomendamos:
        
        1. **BIMvision** (gratuito): https://bimvision.eu/
        2. **IFC.js Viewer** online: https://viewer.ifcjs.com/
        3. **xCave** (web): https://xcave.app/
        
        Puedes descargar el archivo IFC desde GitHub:
        """)
        
        # Link de descarga directa desde GitHub
        repo_url = "https://github.com/jorgejuarez85/visor-ifc/tree/main/modelos"
        st.markdown(f"📥 [Descargar IFC desde GitHub]({repo_url})")
    
    elif opcion == "Ver estructura":
        if ifc_file:
            st.write("**Jerarquía del modelo:**")
            pisos = ifc_file.by_type("IfcBuildingStorey")
            if pisos:
                for piso in pisos[:3]:  # Mostrar primeros 3 pisos
                    with st.expander(f"🏢 Piso: {piso.Name if piso.Name else 'Sin nombre'}"):
                        st.write(f"ID: {piso.GlobalId}")
                        st.write("Elementos en este piso:")
                        # Buscar elementos relacionados
                        for rel in ifc_file.by_type("IfcRelContainedInSpatialStructure"):
                            if rel.RelatingStructure == piso:
                                for elem in rel.RelatedElements[:5]:  # Primeros 5
                                    st.write(f"- {elem.is_a()}")
            else:
                st.write("No se encontraron pisos definidos")
else:
    st.info("👈 Selecciona un modelo del panel lateral")

# Footer
st.markdown("---")
st.caption("Visor IFC Simplificado - Para visualización 3D completa, usa un visor dedicado")
