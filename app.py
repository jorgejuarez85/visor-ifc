import streamlit as st
import ifcopenshell
import os

st.set_page_config(page_title="Visor IFC", layout="wide")
st.title("🏗️ Visor IFC - Modo Sencillo")

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
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Elementos", info["elementos"])
                    st.metric("Puertas", info["puertas"])
                with col2:
                    st.metric("Pisos", info["pisos"])
                    st.metric("Ventanas", info["ventanas"])

# Área principal
if modelos and modelo_seleccionado:
    st.subheader(f"📐 Visualizando: {modelo_seleccionado}")
    
    # Generar URL raw del archivo en GitHub
    usuario = "jorgejuarez85"
    repo = "visor-ifc"
    rama = "main"
    url_raw = f"https://raw.githubusercontent.com/{usuario}/{repo}/{rama}/modelos/{modelo_seleccionado}"
    
    # Mostrar URL (opcional)
    with st.expander("🔗 URL del archivo"):
        st.code(url_raw, language="text")
    
     # VISOR xCave (recomendado para móvil)
    st.markdown("### 🕶️ Visor 3D")
    st.caption("Haz clic en el modelo para interactuar (zoom, rotar, etc.) - Optimizado para móvil")
    
    # HTML con iframe a xCave
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <style>
            body {{ 
                margin: 0; 
                overflow: hidden; 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background-color: #f5f5f5;
            }}
            #info {{ 
                position: absolute; 
                top: 10px; 
                left: 10px; 
                right: 10px;
                background: rgba(0,0,0,0.8); 
                color: white; 
                padding: 8px 16px; 
                border-radius: 30px;
                font-size: 14px;
                z-index: 1000;
                text-align: center;
                backdrop-filter: blur(5px);
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }}
            .loading {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: #333;
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <div id="info">🔄 Cargando modelo en xCave... (pocos segundos)</div>
        <iframe 
            src="https://xcave.app/embed?url={url_raw}&autoload=true"
            width="100%" 
            height="700px" 
            style="border: none; background: white;"
            allowfullscreen
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture">
        </iframe>
        <script>
            // Actualizar mensaje cuando cargue
            setTimeout(function() {{
                document.getElementById('info').innerHTML = '✅ Modelo listo - Usa gestos táctiles o ratón';
            }}, 4000);
            
            // Detectar si es móvil
            if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {{
                document.getElementById('info').innerHTML = '👆 Toca para rotar | Pellizca para zoom';
            }}
        </script>
    </body>
    </html>
    """
    
    # Mostrar el visor
    st.components.v1.html(html_code, height=720)
    
    # Instrucciones de uso
    with st.expander("📖 Cómo usar el visor"):
        st.markdown("""
        - **Ratón / touch**: Rotar la vista
        - **Rueda / pellizco**: Zoom
        - **Botón derecho + arrastrar**: Panorámica
        - **Haz clic en elementos**: Seleccionar (si el visor lo soporta)
        
        El visor puede tardar unos segundos en cargar dependiendo del tamaño del archivo.
        """)
    
    # Opciones adicionales
    st.markdown("---")
    st.subheader("🔗 Compartir o descargar")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"[![IFC.js](https://img.shields.io/badge/🕶️-Abrir%20en%20IFC.js-blue)](https://ifcjs.github.io/ifcjs-crash-course/sample.html?load={url_raw})")
    with col2:
        st.markdown(f"[![xCave](https://img.shields.io/badge/🌐-Abrir%20en%20xCave-green)](https://xcave.app/?load={url_raw})")
    with col3:
        st.markdown(f"[![Descargar](https://img.shields.io/badge/📥-Descargar%20IFC-orange)]({url_raw})")

else:
    st.info("👈 Selecciona un modelo del panel lateral para comenzar")
    st.image("https://via.placeholder.com/800x400?text=Selecciona+un+modelo+IFC", use_container_width=True)

# Footer
st.markdown("---")
st.caption("Visor IFC simplificado - Modelos almacenados en GitHub")
