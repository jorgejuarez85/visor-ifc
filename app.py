import streamlit as st
import ifcopenshell
import os

st.set_page_config(page_title="Visor IFC", layout="wide")
st.title("🏗️ Visor IFC - Enlaces a Visores Externos")
st.markdown("Comparte este enlace con quien quieras. El modelo se carga en visores web profesionales.")

# Función para listar modelos
def get_modelos_disponibles():
    modelos_dir = "modelos"
    if not os.path.exists(modelos_dir):
        os.makedirs(modelos_dir)
        return []
    return [f for f in os.listdir(modelos_dir) if f.endswith('.ifc')]

# Función para obtener información básica del IFC
def get_ifc_info(file_path):
    try:
        ifc_file = ifcopenshell.open(file_path)
        info = {
            "elementos": len(list(ifc_file.by_type("IfcProduct"))),
            "pisos": len(list(ifc_file.by_type("IfcBuildingStorey"))),
            "puertas": len(list(ifc_file.by_type("IfcDoor"))),
            "ventanas": len(list(ifc_file.by_type("IfcWindow"))),
            "muros": len(list(ifc_file.by_type("IfcWall"))),
            "losas": len(list(ifc_file.by_type("IfcSlab"))),
        }
        return info
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return None

# Sidebar
with st.sidebar:
    st.header("📁 Modelos disponibles")
    
    modelos = get_modelos_disponibles()
    
    if not modelos:
        st.warning("No hay archivos IFC en la carpeta 'modelos'")
        st.info("Agrega archivos .ifc a la carpeta 'modelos' en GitHub")
        modelo_seleccionado = None
        info = None
    else:
        # Selector de modelo
        modelo_seleccionado = st.selectbox(
            "Elige un modelo:",
            modelos,
            index=0
        )
        
        if modelo_seleccionado:
            ruta_modelo = os.path.join("modelos", modelo_seleccionado)
            info = get_ifc_info(ruta_modelo)
            
            if info:
                st.markdown("---")
                st.subheader("📊 Estadísticas")
                
                # Mostrar métricas en columnas
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Elementos totales", info["elementos"])
                    st.metric("Pisos", info["pisos"])
                    st.metric("Puertas", info["puertas"])
                with col2:
                    st.metric("Ventanas", info["ventanas"])
                    st.metric("Muros", info["muros"])
                    st.metric("Losas", info["losas"])

# Área principal - ESTO VA FUERA DEL SIDEBAR
if modelos and modelo_seleccionado and info:
    st.header(f"📐 {modelo_seleccionado}")
    
    # Generar URL raw del archivo en GitHub (CORREGIDA)
    usuario = "jorgejuarez85"
    repo = "visor-ifc"
    rama = "main"
    url_raw = f"https://raw.githubusercontent.com/{usuario}/{repo}/refs/heads/{rama}/modelos/{modelo_seleccionado}"
    
    # Información del archivo
    with st.expander("🔗 URL directa del archivo IFC"):
        st.code(url_raw, language="text")
        st.caption("Esta URL puede usarse en cualquier visor web que soporte IFC")
    
    # ENLACES A VISORES EXTERNOS
    st.markdown("## 🌐 Abrir en visor web profesional")
    st.markdown("Haz clic en cualquiera de estos enlaces para ver el modelo en 3D:")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏢 That Open Company (Recomendado)")
        st.markdown(f"""
        [![That Open Company](https://img.shields.io/badge/Abrir%20en-That%20Open%20Company-blue?style=for-the-badge&logo=ifc)](https://platform.thatopen.com/apps/ifc-viewer?load={url_raw})

        *Visor profesional muy completo y estable. Mejor opción actual.*
        """)

        st.markdown("### 🔷 IFC.js Viewer Oficial")
        st.markdown(f"""
        [![IFC.js](https://img.shields.io/badge/Abrir%20en-IFC.js%20Official-orange?style=for-the-badge&logo=javascript)](https://viewer.ifcjs.com/#?load={url_raw})

        *Visor de referencia del proyecto IFC.js. Más fiable que el demo anterior.*
        """)

    with col2:
        st.markdown("### ⚡ WebIFCViewer (Alternativo)")
        st.markdown(f"""
        [![WebIFCViewer](https://img.shields.io/badge/Abrir%20en-WebIFCViewer-green?style=for-the-badge&logo=three.js)](https://webifcviewer.com/?load={url_raw})

        *Visor muy ligero, rápido y que suele funcionar bien en móviles.*
        """)

        st.markdown("### 📥 Descargar archivo IFC")
        st.markdown(f"""
        [![Descargar](https://img.shields.io/badge/📥-Descargar%20IFC-red?style=for-the-badge)]({url_raw})

        *Si los visores web fallan, descarga el archivo para usar en programas de escritorio (como BIMvision, Solibri, etc.).*
        """)

    # Mensaje de ayuda contextual
    st.info("💡 **Nota sobre visores web**: Estos servicios son externos y su disponibilidad puede cambiar. Si uno no carga, prueba con otro. La descarga directa del archivo IFC es la opción más segura.")

else:
    # Mensaje de bienvenida cuando no hay modelo seleccionado
    st.info("👈 Selecciona un modelo del panel lateral para comenzar")
    
    st.markdown("""
    ## 🎯 Cómo usar esta aplicación
    
    1. **Selecciona un modelo** en el panel izquierdo
    2. **Revisa las estadísticas** del modelo
    3. **Elige un visor web** de los disponibles
    4. **Comparte el enlace** con quien quieras
    
    ### 📱 Funciona en:
    - PC (Windows, Mac, Linux)
    - Tablets (iPad, Android)
    - Celulares (cualquier navegador moderno)
    
    ### 📂 Modelos disponibles
    Los archivos IFC están almacenados en GitHub y se actualizan automáticamente.
    """)

# Footer (siempre visible)
st.markdown("---")
st.caption("Visor IFC - Modelos BIM accesibles vía web | Hecho con Streamlit y Python")
