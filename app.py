import streamlit as st
import ifcopenshell
import os

st.set_page_config(page_title="Visor BIM", layout="wide")
st.title("🏗️ Visor de Modelos BIM")
st.markdown("Comparte este enlace con tu equipo. Los modelos se ven directo en el celular.")

# ============================================
# FUNCIONES
# ============================================

def get_archivos_disponibles():
    """Lista todos los archivos en la carpeta modelos"""
    modelos_dir = "modelos"
    if not os.path.exists(modelos_dir):
        os.makedirs(modelos_dir)
        return []
    # Aceptamos .ifc, .pdf y .u3d
    archivos = [f for f in os.listdir(modelos_dir) 
                if f.endswith(('.ifc', '.pdf', '.u3d'))]
    return sorted(archivos)

def get_ifc_info(file_path):
    """Obtiene estadísticas de un archivo IFC"""
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
        st.error(f"Error al leer el archivo IFC: {e}")
        return None

def mostrar_pdf_3d(url_raw, archivo_nombre):
    """Muestra un PDF 3D con instrucciones"""
    st.success("✅ **PDF 3D detectado** - Ideal para ver en celular")
    
    st.markdown("""
    ### 📱 Cómo ver el modelo 3D:
    1. **Haz clic** en "Abrir PDF" (abajo)
    2. El PDF se abrirá en tu navegador
    3. **Toca el modelo** con un dedo para rotarlo
    4. **Pellizca** con dos dedos para acercar/alejar
    
    *No necesitas instalar nada. El visor 3D está dentro del PDF.*
    """)
    
    # Botón grande para abrir
    st.markdown(f"""
    <div style="text-align: center; margin: 30px 0;">
        <a href="{url_raw}" target="_blank" style="
            background-color: #4CAF50;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 50px;
            font-size: 20px;
            font-weight: bold;
            display: inline-block;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        ">📄 ABRIR PDF 3D</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Visor embebido de Google
    st.markdown("### Vista previa:")
    st.components.v1.html(f"""
    <iframe 
        src="https://docs.google.com/viewer?url={url_raw}&embedded=true" 
        width="100%" 
        height="600px" 
        style="border: 2px solid #ddd; border-radius: 10px;">
    </iframe>
    """, height=620)
    
    # Descarga
    with open(os.path.join("modelos", archivo_nombre), "rb") as f:
        pdf_bytes = f.read()
    
    st.download_button(
        label="📥 Descargar PDF para ver sin internet",
        data=pdf_bytes,
        file_name=archivo_nombre,
        mime="application/pdf"
    )

def mostrar_u3d(url_raw, archivo_nombre):
    """Muestra instrucciones para archivos U3D"""
    st.info("🎯 **Archivo U3D detectado**")
    
    st.markdown("""
    ### Para ver este modelo 3D:
    
    **Opción 1 (recomendada): Convertir a PDF**
    1. Descarga el archivo .u3d
    2. Ábrelo con **Nitro PDF** (Crear PDF → Desde archivo)
    3. Sube el PDF resultante a GitHub
    
    **Opción 2 (rápida): Visor online**
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"[Abrir en U3D Viewer Online](https://www.creators3d.com/online-viewer?file={url_raw})")
    with col2:
        st.markdown(f"[Descargar .u3d]({url_raw})")
    
    with open(os.path.join("modelos", archivo_nombre), "rb") as f:
        st.download_button("📥 Descargar archivo U3D", f, archivo_nombre)

def mostrar_ifc(info, url_raw):
    """Muestra opciones para archivos IFC"""
    st.markdown("### 🏗️ Modelo IFC")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Elementos", info["elementos"])
        st.metric("Pisos", info["pisos"])
    with col2:
        st.metric("Puertas", info["puertas"])
        st.metric("Ventanas", info["ventanas"])
    
    st.markdown("#### 🌐 Ver online:")
    st.markdown(f"""
    - [IFC.js Viewer](https://ifcjs.github.io/ifcjs-crash-course/sample.html?load={url_raw})
    - [That Open Company](https://platform.thatopen.com/apps/ifc-viewer?load={url_raw})
    - [Descargar IFC]({url_raw}) (para BIMvision)
    """)

# ============================================
# INTERFAZ PRINCIPAL
# ============================================

with st.sidebar:
    st.header("📁 Modelos disponibles")
    archivos = get_archivos_disponibles()
    
    if not archivos:
        st.warning("No hay archivos en 'modelos'")
        st.info("Sube archivos .ifc, .pdf o .u3d a GitHub")
        archivo_seleccionado = None
    else:
        archivo_seleccionado = st.selectbox("Elige un modelo:", archivos)
        
        if archivo_seleccionado:
            st.caption(f"Tipo: **.{archivo_seleccionado.split('.')[-1]}**")
            
            # Si es IFC, mostrar estadísticas en sidebar
            if archivo_seleccionado.endswith('.ifc'):
                ruta = os.path.join("modelos", archivo_seleccionado)
                info = get_ifc_info(ruta)
            else:
                info = None

# Área principal
if archivos and archivo_seleccionado:
    st.header(f"📐 {archivo_seleccionado}")
    
    # URL raw
    url_raw = f"https://raw.githubusercontent.com/jorgejuarez85/visor-ifc/refs/heads/main/modelos/{archivo_seleccionado}"
    
    # Detectar tipo y mostrar
    if archivo_seleccionado.endswith('.pdf'):
        mostrar_pdf_3d(url_raw, archivo_seleccionado)
    elif archivo_seleccionado.endswith('.u3d'):
        mostrar_u3d(url_raw, archivo_seleccionado)
    elif archivo_seleccionado.endswith('.ifc') and info:
        mostrar_ifc(info, url_raw)
    else:
        st.error("Tipo de archivo no soportado o error al leer")

else:
    # Pantalla de bienvenida
    st.info("👈 Selecciona un modelo del panel lateral")
    st.markdown("""
    ## 📱 Cómo compartir modelos con tu equipo
    
    1. **Sube tus archivos** a la carpeta `modelos` en GitHub
    2. **Comparte este enlace** por WhatsApp
    3. **Ellos abren y ven** directo en el celular
    
    ### Formatos soportados:
    - **.pdf** → PDF 3D (recomendado, mejor experiencia)
    - **.u3d** → Modelo 3D puro (requiere conversión o visor online)
    - **.ifc** → Modelo IFC (para expertos)
    """)

# Footer
st.markdown("---")
st.caption("Visor BIM para equipo - Hecho con Streamlit")
