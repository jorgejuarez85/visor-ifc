import streamlit as st

st.set_page_config(page_title="Visor 3D Campo", layout="wide")
st.title("📱 Modelos para Campo - Versión Visual")
st.markdown("Selecciona un proyecto y ve el modelo 3D directamente en tu celular.")

# Diccionario de proyectos: Nombre -> URL del OBJ en Dropbox (con raw=1)
proyectos = {
    "Proyecto Alpha": "https://www.dropbox.com/scl/fi/xtp7rqhezg60jpyynm9fk/p3.obj?rlkey=1f1simujje3t33h7sr3yv18sx&st=gqzeb9nk&raw=1",
    "Proyecto Beta": "https://www.dropbox.com/scl/fi/abcd/otro.obj?rlkey=...&raw=1",
    # Agrega aquí todos tus proyectos
}

# Selector en el lateral
with st.sidebar:
    st.header("🗂️ Proyectos")
    proyecto_seleccionado = st.selectbox("Elige un proyecto:", list(proyectos.keys()))

# Área principal: visor 3D
if proyecto_seleccionado:
    url_obj = proyectos[proyecto_seleccionado]
    
    st.subheader(f"🏗️ {proyecto_seleccionado}")
    st.caption("Usa los dedos para rotar y hacer zoom.")
    
    # Usamos un enlace directo (evita problemas CORS)
    st.markdown(f"""
    <div style="text-align: center; margin: 30px 0;">
        <a href="https://3dviewer.net/#model={url_obj}" target="_blank" style="
            background-color: #4CAF50;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 50px;
            font-size: 20px;
            font-weight: bold;
            display: inline-block;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        ">🔍 ABRIR MODELO 3D EN VISOR</a>
    </div>
    <p style="text-align: center; color: #666;">
        El visor se abre en una nueva pestaña.<br>
        Funciona perfecto en celular y tablet.
    </p>
    """, unsafe_allow_html=True)
    
    # Opción de compartir enlace directo
    with st.expander("🔗 Compartir este modelo"):
        st.markdown(f"**URL del visor:**")
        st.code(f"https://3dviewer.net/#model={url_obj}")
    
    # Descarga directa
    with st.expander("📥 Descargar archivo OBJ"):
        st.markdown(f"[Haz clic aquí para descargar el modelo]({url_obj})")

else:
    st.info("👈 Selecciona un proyecto del panel lateral")
    st.image("https://via.placeholder.com/800x400?text=Selecciona+un+proyecto+para+ver+el+modelo+3D")

st.markdown("---")
st.caption("App de Campo - Visualización 3D simple para el equipo")
