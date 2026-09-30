<<<<<<< HEAD
# 🏦 Coink Analytics + 🎭 Chatbot con Personalidad - Actividad 6

Proyecto doble desarrollado en **Python + Streamlit** que incluye:

1. **🏦 Análisis de datos Coink** — Dashboard interactivo sobre depósitos en máquinas OINK con una métrica propia llamada **Coink Score**.
2. **🎭 Chatbot con Personalidad** — Chatbot que adopta la personalidad de 5 compañeros de clase, con soporte para chat escrito y chat de voz.
=======
# 🎭 Chatbot con Personalidad - Actividad 6

Chatbot interactivo desarrollado en **Python + Streamlit** que adopta la personalidad de 5 compañeros de clase, permitiendo conversar por **chat escrito** y por **chat de voz** (entrada por micrófono y salida por altavoz).
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

<<<<<<< HEAD
## 📋 Tabla de contenido

- [🏦 Parte 1: Coink Analytics](#-parte-1-coink-analytics)
  - [¿Qué es Coink y qué es un OINK?](#qué-es-coink-y-qué-es-un-oink)
  - [Cómo funciona un OINK](#cómo-funciona-un-oink)
  - [Métrica: Coink Score](#métrica-coink-score)
  - [Bases de datos: relacional vs no relacional](#bases-de-datos-relacional-vs-no-relacional)
- [🎭 Parte 2: Chatbot con Personalidad](#-parte-2-chatbot-con-personalidad)
  - [Los 5 compañeros](#los-5-compañeros)
  - [Análisis comparativo](#análisis-comparativo)
- [🚀 Instalación](#-instalación)
- [▶️ Uso](#️-uso)
- [📁 Estructura del proyecto](#-estructura-del-proyecto)
- [🐛 Problemas conocidos](#-problemas-conocidos)
- [👨‍💻 Autor](#️-autor)

---

# 🏦 Parte 1: Coink Analytics

Dashboard interactivo que analiza los depósitos realizados en las máquinas **OINK** de la fintech colombiana **Coink**, y clasifica a los usuarios según su comportamiento de ahorro.

## ¿Qué es Coink y qué es un OINK?

**Coink** es una fintech colombiana que fomenta el ahorro mediante una billetera digital y máquinas físicas de depósito llamadas **OINK**.

Un **OINK** es una máquina física de depósito de ahorros. Funciona como un "cajero al revés": el usuario **deposita monedas y billetes en efectivo** y estos se reflejan automáticamente en su **billetera digital** dentro de la app móvil de Coink.

Los OINKs están ubicados en puntos estratégicos de alto tráfico:

- Centros comerciales (Plaza de las Américas, Los Molinos)
- Universidades (Universidad de los Andes)
- Zonas empresariales

## Cómo funciona un OINK

Flujo completo desde que el usuario inserta una moneda hasta que ve el saldo en su app:

```
┌─────────────────────────────────────────────┐
│ ( INICIO ) Usuario inserta moneda en OINK   │
└─────────────────────────────────────────────┘
                    │
                    ▼
        ◇ ¿Sensor valida la moneda? ◇
         │No                    │Sí
         ▼                      ▼
   [Devolver moneda]    [Clasificador cuenta]
   [ + registrar  ]     [ denominación     ]
   [   intento    ]            │
         │                     ▼
         │            [Usuario se autentica]
         │            [  QR / Huella / Cédula]
         │                     │
         │                     ▼
         │          ◇ ¿API Coink valida? ◇
         │           │No           │Sí
         │           ▼             ▼
         │      [Rechazar]   [Backend crea]
         │      [notificar]  [registro depósito]
         │           │             │
         │           │             ▼
         │           │     [( PostgreSQL ACID )]
         │           │             │
         │           │             ▼
         │           │     [Actualizar saldo]
         │           │     [billetera digital]
         │           │             │
         │           │             ▼
         │           │     [Publicar Kafka]
         │           │             │
         │           │             ▼
         │           │     [App recibe push]
         │           │             │
         │           │             ▼
         │           │     [Usuario ve saldo]
         │           │             │
         │           │             ▼
         │           │   ◇ ¿Desea retirar? ◇
         │           │    │No         │Sí
         │           │    │           ▼
         │           │    │   [Selecciona monto]
         │           │    │   [ y método      ]
         │           │    │           │
         │           │    │           ▼
         │           │    │  ◇ ¿Saldo suficiente? ◇
         │           │    │   │No        │Sí
         │           │    │   ▼          ▼
         │           │    │ [Error]  [Validar]
         │           │    │ [saldo]  [antifraude]
         │           │    │   │          │
         │           │    │   │          ▼
         │           │    │   │   [Pasarela pagos]
         │           │    │   │   [  PSE / ACH  ]
         │           │    │   │          │
         │           │    │   │          ▼
         │           │    │   │   [Debitar billetera]
         │           │    │   │          │
         │           │    │   │          ▼
         │           │    │   │   [Confirmar usuario]
         │           │    │   │          │
         ▼           ▼    ▼   ▼          ▼
        ┌─────────────────────────────────────┐
        │           ( FIN )                   │
        └─────────────────────────────────────┘
```

**Etapas:**

1. **Inserción de la moneda** — Sensores ópticos y de peso validan autenticidad.
2. **Conteo y clasificación** — Se separa por denominación ($50, $100, $200, $500, $1000).
3. **Autenticación** — QR, cédula, huella o app.
4. **Registro transaccional** — PostgreSQL con ACID + eventos en Kafka.
5. **Actualización de billetera** — Saldo actualizado + push al móvil.
6. **Visualización** — App muestra el saldo en tiempo real.
7. **Retiro** — Pasarela PSE/ACH + validación antifraude.

## Métrica: Coink Score

Un "buen usuario" se define como aquel que es **constante, ahorra montos significativos, es leal y mantiene un ticket promedio saludable**.

```
Coink_Score = 0.30 * Frecuencia_norm
            + 0.30 * Monto_Total_norm
            + 0.20 * Ticket_Promedio_norm
            + 0.20 * Antigüedad_norm
```

Cada componente se normaliza con Min-Max (0 a 1) y se multiplica por 100.

**Clasificación final:**

| Categoría | Rango | Significado |
|-----------|-------|-------------|
| 🥇 **Oro** | Score ≥ 70 | Usuario estrella: frecuente, leal y con buen ticket |
| 🥈 **Plata** | 40 ≤ Score < 70 | Usuario intermedio |
| 🥉 **Bronce** | Score < 40 | Usuario esporádico o con depósitos mínimos |

## Bases de datos: relacional vs no relacional

### Base de datos relacional

Modelo donde los datos se organizan en **tablas** con filas y columnas, con **esquema fijo**, relacionadas mediante **claves primarias y foráneas**. Se consulta con **SQL** (MySQL, PostgreSQL, Oracle). Garantizan **ACID**.

### Base de datos no relacional (NoSQL)

No usa tablas rígidas. Se divide en documentales (MongoDB), clave-valor (Redis), columnares (Cassandra) y de grafos (Neo4j). Priorizan **escalabilidad horizontal** y esquemas flexibles (BASE en vez de ACID).

### Recomendación para Coink: modelo híbrido

| Requisito Coink | Relacional | No Relacional |
|---|---|---|
| Integridad transaccional (dinero) | ✅ ACID obligatorio | ⚠️ Riesgo |
| Relación usuario ↔ depósito ↔ billetera ↔ retiro | ✅ Claves foráneas | ❌ Redundancia |
| Reportes analíticos | ✅ SQL + joins | ⚠️ Requiere agregaciones |
| Alto volumen de eventos IoT | ⚠️ Costoso escalar | ✅ MongoDB/Cassandra |
| Geolocalización y logs | ❌ | ✅ |

**Conclusión:** Usar **PostgreSQL** como base principal (usuarios, cuentas, transacciones, retiros) y **MongoDB/Cassandra** para telemetría IoT de los OINKs.

---

# 🎭 Parte 2: Chatbot con Personalidad

Chatbot interactivo que adopta la personalidad de 5 compañeros de clase, permitiendo conversar por **chat escrito** y por **chat de voz** (entrada por micrófono y salida por altavoz).

## Los 5 compañeros
=======
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
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e

| Compañero | Canción | Película | Deporte | Materia | Comida | Cualidades |
|-----------|---------|----------|---------|---------|--------|------------|
| **Ochoa Alejandro** | Sweet Child O' Mine | Avengers: Endgame | Voleibol | Física | Espinaca con huevo | Amable, presta atención |
| **Luis Tapia** | Azabache | Spider-Man: No Way Home | Gym | Inglés | Salchipapa costeña | Musculoso, romántico |
| **Iktan Godoy** | Enamorado tuyo | Batman: El caballero de la noche | Basketball | Matemáticas | Pizza | Resiliente, obstinado |
| **Miguel Muete** | Talismán | La tumba de las luciérnagas | Fútbol de salón | Pensamiento científico | Mazorcada | Inteligente, imprudente |
| **Karen Canchon** | La Cherry | El viaje de Chihiro | Ninguno | Matemáticas | Fresas con crema | Inteligente, apática |

<<<<<<< HEAD
### Estilo de cada personalidad
=======
### 🎭 Estilo de cada personalidad
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e

- **Ochoa** → Amable, tranquilo, atento. Muletillas: *"con gusto", "claro que sí", "tranquilo"*.
- **Luis** → Motivador, gym-lover, romántico. Muletillas: *"bro", "let's go", "puro músculo"*.
- **Iktan** → Resiliente, serio, obstinado. Muletillas: *"no me rindo", "la caída enseña"*.
- **Miguel** → Analítico, científico, directo. Muletillas: *"según la ciencia", "analicemos"*.
- **Karen** → Seca, directa, apática con sarcasmo leve. Muletillas: *"ok", "supongo", "meh"*.

<<<<<<< HEAD
## Análisis comparativo

### Proyectos de código abierto

| Proyecto | Descripción | Parecido |
|----------|-------------|----------|
| **Mushu** (GitHub) | Personalidades únicas para amigos reales. Soporta memoria de conversación. | ⭐ Muy similar |
| **openpdb** | Usa tipos MBTI para generar agentes IA con personalidad | Similar en concepto |

### Productos comerciales

| Producto | Personalidades | Parecido |
|----------|---------------|----------|
| **Geppetto** | Batman, Spider-Man, Einstein | Selección de personaje |
| **ChaChat** | Personajes IA en español con voz | Texto + voz |
| **Novia IA (Amoura)** | Romántica, juguetona, intelectual | Personalidad predefinida |
| **Personality Bot** | Robot, superhéroe, pirata, Yoda | System prompt define tono |

### Diferencias clave

**Mecanismo técnico:** Todos usan instrucciones de personalidad predefinidas (*system prompts*) que determinan tono, vocabulario y lógica de respuesta.

**Fuente de personalidad:**

- **Comerciales:** estereotipos prefabricados
- **Nuestro proyecto:** personas reales que conocemos

**Valor diferencial:** Retratos personalizados con datos reales, no personalidades genéricas.

### Conclusión del análisis

El chatbot **no es único en su categoría**, pero sí **distintivo en su enfoque**: mientras los productos comerciales venden personalidades genéricas, este proyecto construye personalidades basadas en **personas reales observables**. La singularidad está en la autenticidad de los datos, no en la tecnología.

=======
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e
---

## 🛠️ Requisitos

- **Python 3.10** o superior
- **Windows / macOS / Linux**
- Micrófono (opcional, para chat de voz de entrada)
- Parlantes (opcional, para chat de voz de salida)
<<<<<<< HEAD
- Conexión a internet (para reconocimiento de voz de Google)
=======
- Conexión a internet (para el reconocimiento de voz de Google)
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
<<<<<<< HEAD
git clone https://github.com/tu-usuario/actividad6-coink-chatbot.git
cd actividad6-coink-chatbot
=======
git clone https://github.com/tu-usuario/chatbot-personalidad.git
cd chatbot-personalidad
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e
```

### 2. Crear entorno virtual

**Windows:**
<<<<<<< HEAD

=======
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
<<<<<<< HEAD

=======
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e
```bash
python3 -m venv .venv
source .venv/bin/activate
```

<<<<<<< HEAD
> ⚠️ Si en Windows PowerShell da error de "ejecución de scripts deshabilitada":
>
=======
> ⚠️ Si en Windows PowerShell te da error de "ejecución de scripts deshabilitada", ejecuta:
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

<<<<<<< HEAD
### 4. Instalar PyAudio (solo para el chatbot de voz)

**Windows:**

=======
### 4. Instalar PyAudio (para el micrófono)

**Windows (recomendado):**
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e
```bash
pip install pipwin
pipwin install pyaudio
```

<<<<<<< HEAD
**macOS:**

=======
**Alternativa si `pipwin` falla:**
```bash
pip install pyaudio
```

**macOS:**
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
<<<<<<< HEAD

=======
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

---

## ▶️ Uso

<<<<<<< HEAD
### 🏦 Dashboard de Coink

```bash
streamlit run app.py
```

Abre en `http://localhost:8501`. Verás:

- Métricas globales (usuarios, monto total, score promedio)
- Gráficas de distribución por categoría
- Top 10 usuarios por Coink Score
- Explorador de usuario individual

### 🎭 Chatbot con Personalidad
=======
Con el entorno virtual activado, ejecuta:
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e

```bash
streamlit run main.py
```

<<<<<<< HEAD
1. Elige un compañero en la barra lateral.
2. Escribe o presiona 🎤 **Hablar por micrófono**.
3. Activa 🔊 **Respuestas por voz** para que el bot te conteste hablando.
4. Presiona 🗑️ **Limpiar chat** para reiniciar.

### 📊 Script de análisis batch (opcional)

```bash
python analisis_coink.py
```

Genera `usuarios_calificados.csv` y `coink_analisis.png` con las 4 gráficas.
=======
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
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e

---

## 📁 Estructura del proyecto

```
<<<<<<< HEAD
actividad6-coink-chatbot/
├── .venv/                      # Entorno virtual (no subir a Git)
├── app.py                      # Dashboard Streamlit de Coink
├── main.py                     # Chatbot con Personalidad
├── analisis_coink.py           # Script batch de análisis
├── depositos_oinks.csv         # Dataset de depósitos
├── usuarios_calificados.csv    # Generado por analisis_coink.py
├── coink_analisis.png          # Generado por analisis_coink.py
├── requirements.txt            # Dependencias
├── README.md                   # Este archivo
└── .gitignore                  # Archivos ignorados por Git
=======
chatbot-personalidad/
├── .venv/                  # Entorno virtual (no subir a Git)
├── main.py                 # Código principal del chatbot
├── requirements.txt        # Dependencias del proyecto
├── README.md               # Este archivo
└── .gitignore              # Archivos ignorados por Git
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e
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
<<<<<<< HEAD
pandas
numpy
matplotlib
seaborn
=======
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e
pyttsx3
pywin32
SpeechRecognition
pyaudio
```

---

<<<<<<< HEAD
## 🐛 Problemas conocidos

### `FileNotFoundError: depositos_oinks.csv`

Asegúrate de que el CSV esté en la **misma carpeta** que los scripts. El código usa:

```python
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "depositos_oinks.csv"
```

Ejecuta los comandos **desde la raíz del proyecto**, no desde `.venv\Scripts\`.

### El script `analisis_coink.py` se ve en blanco en Streamlit

Ese archivo es un **script batch de consola**, no una app de Streamlit. Ejecútalo con:

```bash
python analisis_coink.py
```

No con `streamlit run`.

### El micrófono no funciona

1. Instala PyAudio:
=======
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
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```
<<<<<<< HEAD
2. Configuración → Privacidad → Micrófono → permitir apps.
3. Verifica el dispositivo predeterminado en Configuración de sonido.

### Error `ModuleNotFoundError`

Verifica que el entorno virtual esté activado (debe aparecer `(.venv)` al inicio del terminal).

### `pyttsx3` no habla

En Windows instala:

=======

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
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e
```bash
pip install pywin32
```

---

## 🛠️ Tecnologías usadas

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — Framework de UI
<<<<<<< HEAD
- [Pandas](https://pandas.pydata.org/) — Análisis de datos
- [Matplotlib](https://matplotlib.org/) + [Seaborn](https://seaborn.pydata.org/) — Visualización
=======
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e
- [pyttsx3](https://pypi.org/project/pyttsx3/) — Texto a voz (offline)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) — Reconocimiento de voz
- [PyAudio](https://pypi.org/project/PyAudio/) — Acceso al micrófono
- [pywin32](https://pypi.org/project/pywin32/) — Soporte Windows para TTS

---

## 📚 Aprendizajes

- Creación de entornos virtuales en VS Code
- Uso de `st.session_state` para mantener estado entre recargas
- Manejo de audio en Python (entrada y salida)
<<<<<<< HEAD
- Diseño de personalidades mediante *system prompts*
- Comprensión del ecosistema Coink (OINKs, billeteras digitales, bases de datos híbridas)
- Construcción de métricas de negocio (Coink Score)
=======
- Diseño de personalidades mediante "system prompts"
>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e
- Comparación crítica con soluciones comerciales y de código abierto

---

## 👨‍💻 Autor

**[Thomas Arismendi]**
<<<<<<< HEAD
Actividad 6 — [Programación de Software SENA]

---
=======
Actividad 6 — [programacion de software SENA]

>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e

## 📄 Licencia

Este proyecto es de uso educativo. Puedes usarlo, modificarlo y compartirlo libremente.

---

## 🙏 Agradecimientos

- A mis compañeros por prestar sus datos y personalidades
- A la comunidad de Streamlit por la documentación
<<<<<<< HEAD
- A los proyectos **Mushu** y **openpdb** por inspirar el análisis comparativo
- A **Coink** por el contexto sobre los OINKs y su arquitectura de datos
=======
- A los proyectos **Mushu** y **openpdb** por inspirar este análisis comparativo

>>>>>>> a5cc6c46ad8937ec6b95dcd580be8feb1081108e
