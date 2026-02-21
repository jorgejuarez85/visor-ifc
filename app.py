import streamlit as st

st.set_page_config(page_title="Visor IFC - Estructuras", layout="wide")

# ============================================
# CONFIGURACIÓN DE USUARIOS Y PROYECTOS
# ============================================

# Diccionario de usuarios válidos (usuario: contraseña)
USUARIOS_VALIDOS = {
    "ffarfan": "opcid1",
    "hrodriguez": "opcid1",
    "habad": "opcid1",
    "fguerrero": "opcid1",
    "jrojas": "opcid1",
    "syauri": "opcid1",
    "jmoreno": "opcid1",
    "lcornejo": "opcid1",
    "hagregu": "opcid1",
    "jescudero": "opcid1",
    "wrivas": "opcid1"
}

# Base de datos de proyectos (todos visibles para cualquier usuario logueado)
proyectos = {
    "5504-dist1-FF": {
        "url": "https://www.dropbox.com/scl/fi/eppqcl9su92q54p7trww1/Dist-Gast-Sector-1.obj?rlkey=fipri74scohl760hubcsn7v4c&st=5ejnkyov&raw=1",
        "descripcion": "Modelo de referencia - Sector 1"
    },
    "5504-dist2-FF": {
        "url": "https://www.dropbox.com/scl/fi/l12rxa96e2k85e8l01pfk/Dist-Gast-Sector-2.obj?rlkey=px7071peo3bdo6bbjwixvqedg&st=bbtj8u15&raw=1",
        "descripcion": "Modelo de referencia - Sector 2"
    },
    "5504-dist3-LevTop-FF": {
        "url": "https://www.dropbox.com/scl/fi/r54em3tp0c2kgyd4etn0z/5504-dist3-LevTop-FF.obj?rlkey=dl34gmiiln4kmknr5vnqjsesd&st=1adnyt9x&dl=1",
        "descripcion": "Modelo de referencia - Sector 3"
    },
    "5504-dist3-FF": {
        "url": "https://www.dropbox.com/scl/fi/8u1il8qaptbar6ffdijum/Dist-Gast-Sector-3.obj?rlkey=ke81fvhzajglo1yc9er1twks5&st=0i7gaive&raw=1",
        "descripcion": "Modelo de referencia - Sector 3"
    },
    "5550-PUCPPZ-WR": {
        "url": "https://www.dropbox.com/scl/fi/4h0g5mauxruaqflrkdgn0/pucp-pz.obj?rlkey=5r8xzzcpblnn1jqaohoswcp6t&st=aby04p02&raw=1",
        "descripcion": "Modelo de referencia - Pabellón Z"
    }
}

# ============================================
# SISTEMA DE LOGIN
# ============================================

def verificar_login(usuario, password):
    """Verifica si el usuario y contraseña son válidos"""
    return usuario in USUARIOS_VALIDOS and USUARIOS_VALIDOS[usuario] == password

# Estado de la sesión
if "logueado" not in st.session_state:
    st.session_state.logueado = False
    st.session_state.usuario = None

# ============================================
# INTERFAZ PRINCIPAL
# ============================================

st.title("🏗️ Visor IFC - Estructuras de Referencia")
st.markdown("Acceso para supervisores de obra")

# --- PANTALLA DE LOGIN ---
if not st.session_state.logueado:
    
    with st.form("login_form"):
        st.subheader("🔐 Acceso al sistema")
        usuario = st.text_input("Usuario:")
        password = st.text_input("Contraseña:", type="password")
        submit = st.form_submit_button("Ingresar")
        
        if submit:
            if verificar_login(usuario, password):
                st.session_state.logueado = True
                st.session_state.usuario = usuario
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")
    
    st.markdown("---")
    st.caption("Solo para personal autorizado - OPCID")

# --- PANTALLA PRINCIPAL (logueado) ---
else:
    st.sidebar.success(f"👋 Usuario: {st.session_state.usuario}")
    
    # Botón de logout
    if st.sidebar.button("🔒 Cerrar sesión"):
        st.session_state.logueado = False
        st.session_state.usuario = None
        st.rerun()
    
    # Lista de proyectos en el sidebar
    with st.sidebar:
        st.header("🗂️ Proyectos disponibles")
        lista_proyectos = list(proyectos.keys())
        proyecto_seleccionado = st.selectbox("Elige un proyecto:", lista_proyectos)
        
        if proyecto_seleccionado:
            st.caption(proyectos[proyecto_seleccionado]["descripcion"])
    
    # Área principal: visor del proyecto seleccionado
    if proyecto_seleccionado:
        url_obj = proyectos[proyecto_seleccionado]["url"]
        
        st.subheader(f"📐 {proyecto_seleccionado}")
        
        # ADVERTENCIA SOLICITADA
        st.warning("⚠️ **Modelos de referencia** - Si requiere información más detallada, por favor solicítela a oficina técnica.")
        
        # Botón para abrir el visor 3D
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
            ">🔍 VER MODELO EN 3D</a>
        </div>
        <p style="text-align: center; color: #666;">
            El visor se abre en una nueva pestaña.<br>
            Funciona perfecto en celular y tablet.
        </p>
        """, unsafe_allow_html=True)
        
        # Información adicional (opcional)
        with st.expander("📋 Detalles del proyecto"):
            st.write(f"**URL del modelo:** (solo para administradores)")
            st.code(url_obj)

st.markdown("---")
st.caption("Visor IFC - Modelos de referencia para supervisores | Desarrollado por OPCID")
