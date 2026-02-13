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

# Área principal
if modelos and modelo_seleccionado:
    st.header(f"📐 {modelo_seleccionado}")
    
    # Generar URL raw del archivo en GitHub
    usuario = "jorgejuarez85"
    repo = "visor-ifc"
    rama = "main"
    url_raw = f"https://raw.githubusercontent.com/{usuario}/{repo}/{rama}/modelos/{modelo_seleccionado}"
    
    # Información del archivo
    with st.expander("🔗 URL directa del archivo IFC"):
        st.code(url_raw, language="text")
        st.caption("Esta URL puede usarse en cualquier visor web que soporte IFC")
    
    # ENLACES A VISORES EXTERNOS (OPCIÓN 4 - LA MÁS SEGURA)
    st.markdown("## 🌐 Abrir en visor web profesional")
    st.markdown("Haz clic en cualquiera de estos enlaces para ver el modelo en 3D:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏢 That Open Company")
        st.markdown(f"""
        [![That Open Company](https://img.shields.io/badge/Abrir%20en-That%20Open%20Company-blue?style=for-the-badge&logo=ifc)](https://platform.thatopen.com/apps/ifc-viewer?load={url_raw})
        
        *Visor profesional con muchas herramientas*
        """)
        
        st.markdown("### 📱 BIM Surfer")
        st.markdown(f"""
        [![BIM Surfer](https://img.shields.io/badge/Abrir%20en-BIM%20Surfer-green?style=for-the-badge&logo=three.js)](https://bimsurfer.org/?load={url_raw})
        
        *Ligero y rápido, funciona bien en móvil*
        """)
    
    with col2:
        st.markdown("### 🔷 IFC.js")
        st.markdown(f"""
        [![IFC.js](https://img.shields.io/badge/Abrir%20en-IFC.js-orange?style=for-the-badge&logo=javascript)](https://ifcjs.github.io/ifcjs-crash-course/sample.html?load={url_raw})
        
        *Código abierto, muy personalizable*
        """)
        
        st.markdown("### 📥 Descargar")
        st.markdown(f"""
        [![Descargar](https://img.shields.io/badge/📥-Descargar%20IFC-red?style=for-the-badge)]({url_raw})
        
        *Para usar en BIMvision, Tekla, etc.*
        """)
    
    # Instrucciones para compartir
    st.markdown("---")
    st.subheader("📲 Compartir con otros usuarios")
    st.markdown(f"""
    Simplemente comparte este enlace:
    
    `https://visor-ifc-dxojck8pjjvkvf5wcrnk5g.streamlit.app/`
    
    Los usuarios podrán:
    1. Seleccionar el modelo
    2. Ver estadísticas básicas
    3. Elegir un visor web de su preferencia
    4. Ver el modelo en 3D sin instalar nada
    """)
    
    # Vista previa de propiedades
    with st.expander("📋 Ver todas las propiedades del modelo"):
        st.json(info)

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

# Footer
st.markdown("---")
st.caption("Visor IFC - Modelos BIM accesibles vía web | Hecho con Streamlit y Python")
