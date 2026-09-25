# 🎭 Chatbot con Personalidad - Actividad 6

Chatbot interactivo desarrollado en **Python + Streamlit** que adopta la personalidad de 5 compañeros de clase, permitiendo conversar por **chat escrito** y por **chat de voz** (entrada por micrófono y salida por altavoz).

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Descripción

Este proyecto implementa un chatbot didáctico donde el usuario puede **seleccionar a uno de 5 compañeros** y conversar con él. Cada compañero tiene:

- ✅ Personalidad propia (tono, muletillas, forma de hablar)
- ✅ Datos reales (canción, película, deporte, materia, comida favorita)
- ✅ Cualidades que lo describen

El bot responde **adoptando la personalidad** del compañero seleccionado, no como un asistente genérico.

---

## ✨ Características

| Función | Descripción |
|---------|-------------|
| 🎭 **5 personalidades** | Cada compañero tiene su propio tono, muletillas y carácter |
| ✍️ **Chat escrito** | Barra de entrada tipo chat moderna |
| 🎤 **Chat de voz (entrada)** | Botón para hablar por micrófono y transcribir a texto |
| 🔊 **Chat de voz (salida)** | Opción para que el bot lea sus respuestas en voz alta |
| 🎨 **Diseño de alto contraste** | Interfaz oscura con acentos amarillos y cyan |
| 🔄 **Cambio dinámico** | Al cambiar de compañero, el chat se reinicia con su saludo típico |
| 🗑️ **Limpiar chat** | Botón para reiniciar la conversación |

---

## 👥 Los 5 Compañeros

| Compañero | Canción | Película | Deporte | Materia | Comida | Cualidades |
|-----------|---------|----------|---------|---------|--------|------------|
| **Ochoa Alejandro** | Sweet Child O' Mine | Avengers: Endgame | Voleibol | Física | Espinaca con huevo | Amable, presta atención |
| **Luis Tapia** | Azabache | Spider-Man: No Way Home | Gym | Inglés | Salchipapa costeña | Musculoso, romántico |
| **Iktan Godoy** | Enamorado tuyo | Batman: El caballero de la noche | Basketball | Matemáticas | Pizza | Resiliente, obstinado |
| **Miguel Muete** | Talismán | La tumba de las luciérnagas | Fútbol de salón | Pensamiento científico | Mazorcada | Inteligente, imprudente |
| **Karen Canchon** | La Cherry | El viaje de Chihiro | Ninguno | Matemáticas | Fresas con crema | Inteligente, apática |

### 🎭 Estilo de cada personalidad

- **Ochoa** → Amable, tranquilo, atento. Muletillas: *"con gusto", "claro que sí", "tranquilo"*.
- **Luis** → Motivador, gym-lover, romántico. Muletillas: *"bro", "let's go", "puro músculo"*.
- **Iktan** → Resiliente, serio, obstinado. Muletillas: *"no me rindo", "la caída enseña"*.
- **Miguel** → Analítico, científico, directo. Muletillas: *"según la ciencia", "analicemos"*.
- **Karen** → Seca, directa, apática con sarcasmo leve. Muletillas: *"ok", "supongo", "meh"*.

---

## 🛠️ Requisitos

- **Python 3.10** o superior
- **Windows / macOS / Linux**
- Micrófono (opcional, para chat de voz de entrada)
- Parlantes (opcional, para chat de voz de salida)
- Conexión a internet (para el reconocimiento de voz de Google)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/chatbot-personalidad.git
cd chatbot-personalidad
```

### 2. Crear entorno virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

> ⚠️ Si en Windows PowerShell te da error de "ejecución de scripts deshabilitada", ejecuta:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar PyAudio (para el micrófono)

**Windows (recomendado):**
```bash
pip install pipwin
pipwin install pyaudio
```

**Alternativa si `pipwin` falla:**
```bash
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

---

## ▶️ Uso

Con el entorno virtual activado, ejecuta:

```bash
streamlit run main.py
```

Se abrirá automáticamente en tu navegador en `http://localhost:8501`.

### 🎮 Cómo interactuar

1. **Elige un compañero** en la barra lateral izquierda (radio buttons).
2. **Escribe** tu mensaje en la barra inferior, o presiona **🎤 Hablar por micrófono**.
3. Activa **🔊 Respuestas por voz** para que el bot te conteste hablando.
4. Presiona **🗑️ Limpiar chat** para reiniciar la conversación.

### 💬 Ejemplos de preguntas

- "Hola"
- "¿Cuál es tu canción favorita?"
- "¿Qué película te gusta?"
- "¿Qué deporte practicas?"
- "¿Cuál es tu comida favorita?"
- "Háblame de ti"
- "¿Cómo eres?"

---

## 📁 Estructura del proyecto

```
chatbot-personalidad/
├── .venv/                  # Entorno virtual (no subir a Git)
├── main.py                 # Código principal del chatbot
├── requirements.txt        # Dependencias del proyecto
├── README.md               # Este archivo
└── .gitignore              # Archivos ignorados por Git
```

### `.gitignore` recomendado

```
.venv/
__pycache__/
*.pyc
.streamlit/
.env
```

### `requirements.txt`

```txt
streamlit
pyttsx3
pywin32
SpeechRecognition
pyaudio
```

---

## 🧠 Cómo funciona la personalidad

Cada compañero tiene un diccionario con:

```python
"Luis Tapia": {
    "cancion": "Azabache",
    "pelicula": "Spider-Man: No Way Home",
    "personalidad": "Eres Luis Tapia. Gym-lover, motivador, romántico.",
    "saludo": "¡Hey bro! 💪 ¿Listo para entrenar?",
    "muletillas": ["bro", "let's go", "puro músculo"]
}
```

La función `generar_respuesta()` detecta la intención del usuario (saludo, canción, película, etc.) y devuelve la respuesta **usando las muletillas y el tono** del compañero seleccionado.

---

## 🔍 Análisis: ¿Existen chatbots con personalidades similares?

### Sí, existen varios proyectos comparables

Durante la investigación encontramos que este tipo de chatbot tiene precedentes tanto en código abierto como en productos comerciales.

### Proyectos de código abierto

| Proyecto | Descripción | Parecido con el nuestro |
|----------|-------------|-------------------------|
| **Mushu** (GitHub) | El desarrollador asignó personalidades únicas a sus amigos reales (ej: "gato perezoso y sarcástico", "amigo caótico y honesto"). Soporta memoria de conversación. | ⭐ **Muy similar**: misma idea de personificar amigos reales, con tono y muletillas propias |
| **openpdb** | Usa tipos MBTI para generar agentes IA con personalidad | Similar en concepto, distinto en fuente de personalidad |

### Productos comerciales

| Producto | Personalidades | Parecido |
|----------|---------------|----------|
| **Geppetto** | Batman, Spider-Man, Einstein, etc. | Selección de personaje con personalidad precargada |
| **ChaChat** | Personajes IA en español con voz | Soporta texto + voz, misma mecánica de interacción |
| **Novia IA (Amoura)** | 6 personalidades: romántica, juguetona, intelectual... | Selección de personalidad predefinida |
| **Personality Bot** | Robot, superhéroe, pirata, hippie, Yoda | Mismo mecanismo: system prompt define tono y vocabulario |

### 🔑 Diferencias clave

**Mecanismo técnico:** Todos usan la misma técnica que nuestro proyecto — **instrucciones de personalidad predefinidas** que determinan el tono, vocabulario y lógica de respuesta.

**Fuente de personalidad:**
- **Comerciales:** estereotipos prefabricados (héroes, arquetipos, roles)
- **Nuestro proyecto:** personas reales que conocemos (compañeros de clase)

**Valor diferencial:** La mayoría de productos ofrecen "personalidades genéricas". El nuestro ofrece **retratos personalizados** con datos reales (canciones, comidas, deportes) y recuerdos auténticos. Esto es justo lo que el proyecto **Mushu** demuestra: llevar la personalidad de amigos reales a la IA produce resultados "divertidos y sorprendentemente precisos".

### 📌 Conclusión del análisis

El chatbot desarrollado **no es único en su categoría**, pero sí **distintivo en su enfoque**: mientras los productos comerciales venden personalidades genéricas, este proyecto construye personalidades basadas en **personas reales observables**. La singularidad está en la autenticidad de los datos, no en la tecnología.

---

## 🐛 Problemas conocidos y soluciones

### El micrófono no funciona

1. **Instala PyAudio correctamente:**
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

2. **Verifica permisos de Windows:**
   - Configuración → Privacidad → Micrófono
   - Activa "Permitir que las apps accedan al micrófono"
   - Activa "Permitir que las apps de escritorio accedan al micrófono"

3. **Verifica el dispositivo predeterminado:**
   - Clic derecho en 🔊 → Configuración de sonido → Entrada

4. **Verifica que PyAudio esté instalado:**
   ```bash
   python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
   ```

### Error `ModuleNotFoundError`

Asegúrate de tener el entorno virtual activado (debe aparecer `(.venv)` al inicio del terminal) antes de instalar o ejecutar.

### PowerShell bloquea la activación

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### pyttsx3 no habla

En Windows instala `pywin32`:
```bash
pip install pywin32
```

---

## 🛠️ Tecnologías usadas

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — Framework de UI
- [pyttsx3](https://pypi.org/project/pyttsx3/) — Texto a voz (offline)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) — Reconocimiento de voz
- [PyAudio](https://pypi.org/project/PyAudio/) — Acceso al micrófono
- [pywin32](https://pypi.org/project/pywin32/) — Soporte Windows para TTS

---

## 📚 Aprendizajes

- Creación de entornos virtuales en VS Code
- Uso de `st.session_state` para mantener estado entre recargas
- Manejo de audio en Python (entrada y salida)
- Diseño de personalidades mediante "system prompts"
- Comparación crítica con soluciones comerciales y de código abierto

---

## 👨‍💻 Autor

**[Tu Nombre]**
Actividad 6 — [Nombre del curso]
[Fecha]

---

## 📄 Licencia

Este proyecto es de uso educativo. Puedes usarlo, modificarlo y compartirlo libremente.

---

## 🙏 Agradecimientos

- A mis compañeros por prestar sus datos y personalidades
- A la comunidad de Streamlit por la documentación
- A los proyectos **Mushu** y **openpdb** por inspirar este análisis comparativo
