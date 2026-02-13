import streamlit as st
import ifcopenshell
import os
import base64

st.set_page_config(page_title="Visor BIM", layout="wide")
st.title("🏗️ Visor de Modelos BIM")
st.markdown("Comparte este enlace con tu equipo. Los modelos se ven directo en el celular.")

# Función para listar archivos en la carpeta modelos
def get_archivos_disponibles():
    modelos_dir = "modelos"
    if not os.path.exists(modelos_dir):
        os.makedirs(modelos_dir)
        return []
    # Listar tanto IFC como PDF
    archivos = [f for f in os.listdir(modelos_dir) 
                if f.endswith('.ifc') or f.endswith('.pdf')]
    return sorted(archivos)  # Ordenados alfabéticamente

# Función para obtener info del IFC (solo para archivos IFC)
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
        st.error(f"Error al leer el archivo IFC: {e}")
        return None

# Sidebar
with st.sidebar:
    st.header("📁 Modelos disponibles")
    
    archivos = get_archivos_disponibles()
    
    if not archivos:
        st.warning("No hay archivos en la carpeta 'modelos'")
        st.info("Sube archivos .ifc o .pdf a la carpeta 'modelos' en GitHub")
        archivo_seleccionado = None
        es_pdf = False
        info = None
    else:
        # Selector de archivo
        archivo_seleccionado = st.selectbox(
            "Elige un modelo:",
            archivos,
            index=0
        )
        
        # Detectar si es PDF
        es_pdf = archivo_seleccionado.endswith('.pdf')
        
        if archivo_seleccionado and not es_pdf:
            # Solo mostrar estadísticas si es IFC
            ruta_archivo = os.path.join("modelos", archivo_seleccionado)
            info = get_ifc_info(ruta_archivo)
            
            if info:
                st.markdown("---")
                st.subheader("📊 Estadísticas")
                
                # Mostrar métricas en columnas
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Elementos", info["elementos"])
                    st.metric("Pisos", info["pisos"])
                    st.metric("Puertas", info["puertas"])
                with col2:
                    st.metric("Ventanas", info["ventanas"])
                    st.metric("Muros", info["muros"])
                    st.metric("Losas", info["losas"])
        else:
            info = None

# Área principal
if archivos and archivo_seleccionado:
    st.header(f"📐 {archivo_seleccionado}")
    
    # Generar URL raw del archivo en GitHub
    usuario = "jorgejuarez85"
    repo = "visor-ifc"
    rama = "main"
    url_raw = f"https://raw.githubusercontent.com/{usuario}/{repo}/refs/heads/{rama}/modelos/{archivo_seleccionado}"
    
    if es_pdf:
        # ============================================
        # VISUALIZACIÓN DE PDF 3D (CON U3D)
        # ============================================
        st.success("✅ **PDF 3D detectado** - Ideal para ver en celular")
        
        st.markdown("""
        ### 📱 Cómo ver el modelo 3D en tu celular:
        1. **Haz clic** en el botón "Abrir PDF" (abajo)
        2. El PDF se abrirá en tu navegador
        3. **Toca el modelo** con un dedo para rotarlo
        4. **Pellizca** con dos dedos para acercar/alejar
        
        *No necesitas instalar ninguna app. El visor 3D está dentro del PDF.*
        """)
        
        # Opción 1: Visor de Google (funciona en todos los dispositivos)
        st.markdown("### 🌐 Ver online:")
        st.components.v1.html(f"""
        <div style="text-align: center; margin: 20px 0;">
            <a href="{url_raw}" target="_blank" style="
                background-color: #4CAF50;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 5px;
                font-size: 18px;
                display: inline-block;
                margin: 10px;
            ">📄 Abrir PDF directamente</a>
        </div>
        <iframe 
            src="https://docs.google.com/viewer?url={url_raw}&embedded=true" 
            width="100%" 
            height="700px" 
            style="border: 2px solid #ddd; border-radius: 10px;">
        </iframe>
        """, height=750)
        
        # Opción 2: Descarga directa
        with open(os.path.join("modelos", archivo_seleccionado), "rb") as f:
            pdf_bytes = f.read()
        
        st.markdown("### 📥 Descargar para ver sin internet:")
        st.download_button(
            label="📥 Descargar PDF 3D",
            data=pdf_bytes,
            file_name=archivo_seleccionado,
            mime="application/pdf"
        )
        
        # Instrucciones adicionales
        with st.expander("❓ Ayuda: ¿Cómo se usa el PDF 3D?"):
            st.markdown("""
            **En PC:**
            - Haz clic en el modelo para activarlo
            - Arrastra con el ratón para rotar
            - Usa la rueda del ratón para zoom
            
            **En celular/tablet:**
            - Toca la pantalla y arrastra para rotar
            - Pellizca para acercar/alejar
            - Toca dos veces para centrar
            
            **El PDF 3D funciona en:**
            - ✅ Adobe Acrobat Reader
            - ✅ Navegadores modernos (Chrome, Safari, Edge)
            - ✅ Visores PDF de iPhone/iPad y Android
            """)
    
    else:
        # ============================================
        # VISUALIZACIÓN DE ARCHIVOS IFC
        # ============================================
        if info:
            st.markdown("### 🏗️ Modelo IFC")
            
            # Enlaces a visores web (los que funcionan actualmente)
            st.markdown("#### 🌐 Ver online (visores web):")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                [![IFC.js](https://img.shields.io/badge/Abrir%20en-IFC.js-blue?style=for-the-badge)](https://ifcjs.github.io/ifcjs-crash-course/sample.html?load={url_raw})
                
                *Visor de código abierto*
                """)
                
                st.markdown(f"""
                [![That Open Company](https://img.shields.io/badge/Abrir%20en-That%20Open%20Company-purple?style=for-the-badge)](https://platform.thatopen.com/apps/ifc-viewer?load={url_raw})
                
                *Visor profesional*
                """)
            
            with col2:
                st.markdown(f"""
                [![WebIFCViewer](https://img.shields.io/badge/Abrir%20en-WebIFCViewer-green?style=for-the-badge)](https://webifcviewer.com/?load={url_raw})
                
                *Visor rápido y ligero*
                """)
                
                st.markdown(f"""
                [![Descargar](https://img.shields.io/badge/📥-Descargar%20IFC-red?style=for-the-badge)]({url_raw})
                
                *Para usar en BIMvision u otros programas*
                """)
            
            st.info("⚠️ **Nota**: Los visores web son servicios externos y pueden fallar. Si no funcionan, descarga el archivo y úsalo en BIMvision (PC).")
        
        else:
            st.error("No se pudo leer el archivo IFC")

else:
    # Mensaje de bienvenida
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://via.placeholder.com/600x400?text=Selecciona+un+modelo+en+el+panel+lateral", 
                 use_container_width=True)
    
    st.markdown("""
    ## 🎯 Cómo usar esta aplicación
    
    1. **En el panel izquierdo**, selecciona un modelo
    2. **Si es PDF 3D**: se abrirá directamente en el navegador (puedes rotarlo con los dedos)
    3. **Si es IFC**: elige un visor web o descarga el archivo
    
    ### 📱 Funciona perfecto en:
    - Celulares (Android/iPhone)
    - Tablets
    - PC (Windows/Mac/Linux)
    
    ### 📂 Modelos disponibles:
    Los archivos están en la carpeta `modelos` de GitHub y se actualizan automáticamente.
    """)

# Footer
st.markdown("---")
st.markdown(
    "🔗 **Comparte este enlace con tu equipo**: " + 
    f"`https://visor-ifc-dxojck8pjjvkvf5wcrnk5g.streamlit.app/`"
)
st.caption("Visor BIM - Hecho con ❤️ usando Streamlit y Python")
