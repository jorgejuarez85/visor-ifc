import streamlit as st

st.set_page_config(page_title="Visor 3D Campo", layout="wide")
st.title("📱 Modelos para Campo - Versión Visual")
st.markdown("Selecciona un proyecto y ve el modelo 3D directamente en tu celular.")

# Diccionario de proyectos: Nombre -> URL del OBJ en Dropbox (con raw=1)
proyectos = {
    "Proyecto Alpha": "https://www.dropbox.com/scl/fi/xtp7rqhezg60jpyynm9fk/p3.obj?rlkey=...&raw=1",
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
    
    # Visor incrustado (el mismo que probaste)
    st.components.v1.html(f"""
    <iframe 
        src="https://3dviewer.net/embed.html#model={url_obj}"
        width="100%" 
        height="700px" 
        style="border: none; border-radius: 10px;"
        allowfullscreen>
    </iframe>
    """, height=720)
    
    # Opción de compartir enlace directo
    with st.expander("🔗 Compartir este modelo"):
        st.markdown(f"**URL del visor:**")
        st.code(f"https://3dviewer.net/#model={url_obj}")
else:
    st.info("👈 Selecciona un proyecto del panel lateral")
    st.image("https://via.placeholder.com/800x400?text=Selecciona+un+proyecto+para+ver+el+modelo+3D")

st.markdown("---")
st.caption("App de Campo - Visualización 3D simple para el equipo")
