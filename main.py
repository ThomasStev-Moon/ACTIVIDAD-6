import streamlit as st
import pyttsx3
import speech_recognition as sr

# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Chatbot con Personalidad",
    page_icon="🎭",
    layout="wide"
)

# ============================================================
# ESTILOS CSS - Alto contraste
# ============================================================
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    h1 { color: #FFD700 !important; text-align: center; text-shadow: 2px 2px 4px #000; }
    h2, h3 { color: #00E5FF !important; }
    p, li, label, span, div { color: #FFFFFF; }
    .perfil {
        background: linear-gradient(135deg, #1f2937, #374151);
        padding: 18px;
        border-radius: 14px;
        border-left: 6px solid #FFD700;
        margin-bottom: 12px;
    }
    .perfil b { color: #FFD700; font-size: 1.1rem; }
    .stButton>button {
        background-color: #FFD700;
        color: #000000;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 10px 18px;
        width: 100%;
    }
    .stButton>button:hover { background-color: #FFC300; }
    section[data-testid="stSidebar"] { background-color: #111827; }
    section[data-testid="stSidebar"] * { color: #FFFFFF !important; }
    .burbuja-user {
        background-color: #1E88E5;
        padding: 12px 16px;
        border-radius: 14px 14px 0 14px;
        margin: 8px 0 8px auto;
        max-width: 75%;
        color: white !important;
        text-align: right;
    }
    .burbuja-bot {
        background-color: #374151;
        padding: 12px 16px;
        border-radius: 14px 14px 14px 0;
        margin: 8px auto 8px 0;
        max-width: 75%;
        color: white !important;
        border-left: 4px solid #FFD700;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# DATOS DE LOS COMPAÑEROS CON PERSONALIDAD
# ============================================================
companeros = {
    "Ochoa Alejandro": {
        "cancion": "Sweet Child O' Mine",
        "pelicula": "Avengers: Endgame",
        "deporte": "Voleibol",
        "materia": "Física",
        "comida": "Espinaca con huevo",
        "cualidades": ["Amable", "Presta atención"],
        "personalidad": "Eres Ochoa Alejandro. Hablas de forma muy amable, atenta y tranquila.",
        "saludo": "¡Hola parcero! 😊 Qué bueno que hablemos, cuéntame ¿en qué te ayudo?",
        "muletillas": ["con gusto", "claro que sí", "tranquilo", "con toda"]
    },
    "Luis Tapia": {
        "cancion": "Azabache",
        "pelicula": "Spider-Man: No Way Home",
        "deporte": "Gym",
        "materia": "Inglés",
        "comida": "Salchipapa costeña",
        "cualidades": ["Musculoso", "Romántico"],
        "personalidad": "Eres Luis Tapia. Gym-lover, motivador, romántico.",
        "saludo": "¡Hey bro! 💪 ¿Listo para entrenar? Cuéntame qué necesitas, ¡vamos con toda!",
        "muletillas": ["bro", "let's go", "puro músculo", "la clave es la constancia"]
    },
    "Iktan Godoy": {
        "cancion": "Enamorado tuyo",
        "pelicula": "Batman: El caballero de la noche",
        "deporte": "Basketball",
        "materia": "Matemáticas",
        "comida": "Pizza",
        "cualidades": ["Resiliente", "Obstinado"],
        "personalidad": "Eres Iktan Godoy. Resiliente, obstinado, nunca te rindes.",
        "saludo": "Hey. Soy Iktan. 🦇 Si vas a preguntar algo, pregúntalo con ganas. Aquí no nos rendimos.",
        "muletillas": ["no me rindo", "la caída enseña", "vamos con todo", "soy obstinado"]
    },
    "Miguel Muete": {
        "cancion": "Talismán",
        "pelicula": "La tumba de las luciérnagas",
        "deporte": "Fútbol de salón",
        "materia": "Pensamiento científico",
        "comida": "Mazorcada",
        "cualidades": ["Inteligente", "Imprudente"],
        "personalidad": "Eres Miguel Muete. Inteligente, analítico, directo sin filtro.",
        "saludo": "Hola. 🧠 Soy Miguel. Dime, ¿qué quieres analizar hoy? Aunque te advierto, soy directo.",
        "muletillas": ["según la ciencia", "es interesante", "analicemos", "siendo honesto"]
    },
    "Karen Canchon": {
        "cancion": "La Cherry",
        "pelicula": "El viaje de Chihiro",
        "deporte": "Ninguno",
        "materia": "Matemáticas",
        "comida": "Fresas con crema",
        "cualidades": ["Inteligente", "Apática"],
        "personalidad": "Eres Karen Canchon. Inteligente, apática, directa con sarcasmo leve.",
        "saludo": "Hola. Soy Karen. 🙂 ¿Qué quieres? Te escucho.",
        "muletillas": ["ok", "supongo", "meh", "es lo que hay"]
    }
}

# ============================================================
# FUNCIONES DE VOZ
# ============================================================
def hablar(texto):
    """Convierte texto a voz con pyttsx3."""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 165)
        engine.setProperty('volume', 1.0)
        voces = engine.getProperty('voices')
        for v in voces:
            nombre = v.name.lower()
            if 'spanish' in nombre or 'español' in nombre or 'helena' in nombre or 'sabina' in nombre:
                engine.setProperty('voice', v.id)
                break
        limpio = texto
        for ch in ["*", "•", "#", "_", "`"]:
            limpio = limpio.replace(ch, "")
        engine.say(limpio)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        st.warning(f"⚠️ No se pudo reproducir el audio: {e}")


def escuchar():
    """Escucha el micrófono y devuelve texto."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            with st.spinner("🎤 Escuchando... habla ahora"):
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=10)
        texto = recognizer.recognize_google(audio, language="es-CO")
        return texto.lower()
    except sr.WaitTimeoutError:
        st.warning("⏱️ No detecté voz. Intenta de nuevo.")
        return ""
    except sr.UnknownValueError:
        st.warning("🤔 No entendí lo que dijiste.")
        return ""
    except Exception as e:
        st.error(f"❌ Error con el micrófono: {e}")
        return ""

# ============================================================
# LÓGICA DEL CHATBOT
# ============================================================
def generar_respuesta(pregunta, nombre_comp):
    p = pregunta.lower().strip()
    datos = companeros[nombre_comp]
    nombre_corto = nombre_comp.split()[0]
    muletilla = datos["muletillas"][0]

    if any(s in p for s in ["hola", "buenas", "hey", "saludos", "qué más", "que mas"]):
        return datos["saludo"]

    if any(s in p for s in ["quién eres", "quien eres", "cómo te llamas", "como te llamas", "tu nombre"]):
        return f"Soy {nombre_comp}. {datos['personalidad']}"

    if any(s in p for s in ["cómo eres", "como eres", "personalidad", "cualidades", "carácter"]):
        return f"Mis cualidades son: {', '.join(datos['cualidades'])}. {muletilla.capitalize()}."

    if any(s in p for s in ["canción", "cancion", "música", "musica", "cantas"]):
        return f"🎵 Mi canción favorita es «{datos['cancion']}». ¡Buenísima, {muletilla}!"

    if any(s in p for s in ["película", "pelicula", "film", "cine", "pelis"]):
        return f"🎬 Mi película favorita es «{datos['pelicula']}». Me encanta, {muletilla}."

    if any(s in p for s in ["deporte", "juegas", "entrenas", "futbol", "baloncesto", "gym"]):
        return f"🏅 Mi deporte es {datos['deporte']}. ¡Me apasiona, {muletilla}!"

    if any(s in p for s in ["materia", "asignatura", "estudias", "clase"]):
        return f"📚 Mi materia favorita es {datos['materia']}. {muletilla.capitalize()}."

    if any(s in p for s in ["comida", "comes", "plato", "comer"]):
        return f"🍽️ Mi comida favorita es {datos['comida']}. ¡Uy, qué rico, {muletilla}!"

    if any(s in p for s in ["cuéntame", "cuentame", "sobre ti", "háblame de ti", "tus datos"]):
        return (f"Claro, {muletilla}. Soy {nombre_comp}. 🎵 {datos['cancion']} | "
                f"🎬 {datos['pelicula']} | 🏅 {datos['deporte']} | "
                f"📚 {datos['materia']} | 🍽️ {datos['comida']}. "
                f"Me describen como: {', '.join(datos['cualidades'])}.")

    if any(s in p for s in ["cómo estás", "como estas", "qué tal", "que tal"]):
        return f"Bien, aquí {muletilla}, ¿y tú qué tal? Cuéntame."

    if any(s in p for s in ["gracias", "thanks"]):
        return f"Con gusto, {muletilla}. Cuando quieras hablamos otra vez. 😊"

    if any(s in p for s in ["adiós", "adios", "chao", "bye", "nos vemos"]):
        return f"¡Nos vemos! Cuídate, {muletilla}."

    return (f"Mmm, no estoy seguro de eso, {muletilla}. "
            f"Pregúntame por mi canción, película, deporte, comida, materia favorita "
            f"o por mi personalidad. Soy {nombre_corto} 😉.")

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.header("🎭 Elige un compañero")
    st.markdown("---")
    seleccion = st.radio("¿Con quién quieres hablar?", list(companeros.keys()), index=0)

    st.markdown("---")
    st.subheader(f"📋 Perfil de {seleccion}")
    d = companeros[seleccion]
    st.markdown(f"""
    <div class="perfil">
        <b>{seleccion}</b><br><br>
        🎵 {d['cancion']}<br>
        🎬 {d['pelicula']}<br>
        🏅 {d['deporte']}<br>
        📚 {d['materia']}<br>
        🍽️ {d['comida']}<br>
        💫 {', '.join(d['cualidades'])}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    voz_salida = st.checkbox("🔊 Respuestas por voz", value=False)
    if st.button("🗑️ Limpiar chat"):
        st.session_state.mensajes = []
        st.session_state.comp_actual = None
        st.rerun()

# ============================================================
# ENCABEZADO
# ============================================================
st.title("🎭 Chatbot con Personalidad")
st.markdown(f"### 💬 Hablando con **{seleccion}**")
st.markdown("Puedes **escribir** o usar el **micrófono** 🎤")

# ============================================================
# ESTADO
# ============================================================
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
if "comp_actual" not in st.session_state:
    st.session_state.comp_actual = None
if "entrada_voz" not in st.session_state:
    st.session_state.entrada_voz = ""

# Si cambia el compañero, reinicia con su saludo
if st.session_state.comp_actual != seleccion:
    st.session_state.comp_actual = seleccion
    st.session_state.mensajes = [
        {"role": "assistant", "content": companeros[seleccion]["saludo"]}
    ]

# ============================================================
# HISTORIAL DE MENSAJES
# ============================================================
for msg in st.session_state.mensajes:
    if msg["role"] == "user":
        st.markdown(f'<div class="burbuja-user">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="burbuja-bot">🎭 <b>{seleccion}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

# ============================================================
# BOTÓN DE VOZ
# ============================================================
col1, col2 = st.columns([1, 3])
with col1:
    if st.button("🎤 Hablar por micrófono"):
        texto = escuchar()
        if texto:
            st.session_state.entrada_voz = texto
            st.rerun()

# ============================================================
# ENTRADA DE TEXTO (chat escrito)
# ============================================================
entrada = st.chat_input("✍️ Escribe tu mensaje aquí...")

pregunta_final = None
if st.session_state.entrada_voz:
    pregunta_final = st.session_state.entrada_voz
    st.session_state.entrada_voz = ""
elif entrada:
    pregunta_final = entrada

if pregunta_final:
    st.session_state.mensajes.append({"role": "user", "content": pregunta_final})
    respuesta = generar_respuesta(pregunta_final, seleccion)
    st.session_state.mensajes.append({"role": "assistant", "content": respuesta})

    if voz_salida:
        hablar(respuesta)

    st.rerun()