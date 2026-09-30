# 🏦 Coink Analytics + 🎭 Chatbot con Personalidad - Actividad 6

Proyecto doble desarrollado en **Python + Streamlit** que incluye:

1. **🏦 Análisis de datos Coink** — Dashboard interactivo sobre depósitos en máquinas OINK con una métrica propia llamada **Coink Score**.
2. **🎭 Chatbot con Personalidad** — Chatbot que adopta la personalidad de 5 compañeros de clase, con soporte para chat escrito y chat de voz.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

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

| Compañero | Canción | Película | Deporte | Materia | Comida | Cualidades |
|-----------|---------|----------|---------|---------|--------|------------|
| **Ochoa Alejandro** | Sweet Child O' Mine | Avengers: Endgame | Voleibol | Física | Espinaca con huevo | Amable, presta atención |
| **Luis Tapia** | Azabache | Spider-Man: No Way Home | Gym | Inglés | Salchipapa costeña | Musculoso, romántico |
| **Iktan Godoy** | Enamorado tuyo | Batman: El caballero de la noche | Basketball | Matemáticas | Pizza | Resiliente, obstinado |
| **Miguel Muete** | Talismán | La tumba de las luciérnagas | Fútbol de salón | Pensamiento científico | Mazorcada | Inteligente, imprudente |
| **Karen Canchon** | La Cherry | El viaje de Chihiro | Ninguno | Matemáticas | Fresas con crema | Inteligente, apática |

### Estilo de cada personalidad

- **Ochoa** → Amable, tranquilo, atento. Muletillas: *"con gusto", "claro que sí", "tranquilo"*.
- **Luis** → Motivador, gym-lover, romántico. Muletillas: *"bro", "let's go", "puro músculo"*.
- **Iktan** → Resiliente, serio, obstinado. Muletillas: *"no me rindo", "la caída enseña"*.
- **Miguel** → Analítico, científico, directo. Muletillas: *"según la ciencia", "analicemos"*.
- **Karen** → Seca, directa, apática con sarcasmo leve. Muletillas: *"ok", "supongo", "meh"*.

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

---

## 🛠️ Requisitos

- **Python 3.10** o superior
- **Windows / macOS / Linux**
- Micrófono (opcional, para chat de voz de entrada)
- Parlantes (opcional, para chat de voz de salida)
- Conexión a internet (para reconocimiento de voz de Google)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/actividad6-coink-chatbot.git
cd actividad6-coink-chatbot
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

> ⚠️ Si en Windows PowerShell da error de "ejecución de scripts deshabilitada":
>
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar PyAudio (solo para el chatbot de voz)

**Windows:**

```bash
pip install pipwin
pipwin install pyaudio
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

```bash
streamlit run main.py
```

1. Elige un compañero en la barra lateral.
2. Escribe o presiona 🎤 **Hablar por micrófono**.
3. Activa 🔊 **Respuestas por voz** para que el bot te conteste hablando.
4. Presiona 🗑️ **Limpiar chat** para reiniciar.

### 📊 Script de análisis batch (opcional)

```bash
python analisis_coink.py
```

Genera `usuarios_calificados.csv` y `coink_analisis.png` con las 4 gráficas.

---

## 📁 Estructura del proyecto

```
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
pandas
numpy
matplotlib
seaborn
pyttsx3
pywin32
SpeechRecognition
pyaudio
```

---

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
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```
2. Configuración → Privacidad → Micrófono → permitir apps.
3. Verifica el dispositivo predeterminado en Configuración de sonido.

### Error `ModuleNotFoundError`

Verifica que el entorno virtual esté activado (debe aparecer `(.venv)` al inicio del terminal).

### `pyttsx3` no habla

En Windows instala:

```bash
pip install pywin32
```

---

## 🛠️ Tecnologías usadas

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — Framework de UI
- [Pandas](https://pandas.pydata.org/) — Análisis de datos
- [Matplotlib](https://matplotlib.org/) + [Seaborn](https://seaborn.pydata.org/) — Visualización
- [pyttsx3](https://pypi.org/project/pyttsx3/) — Texto a voz (offline)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) — Reconocimiento de voz
- [PyAudio](https://pypi.org/project/PyAudio/) — Acceso al micrófono
- [pywin32](https://pypi.org/project/pywin32/) — Soporte Windows para TTS

---

## 📚 Aprendizajes

- Creación de entornos virtuales en VS Code
- Uso de `st.session_state` para mantener estado entre recargas
- Manejo de audio en Python (entrada y salida)
- Diseño de personalidades mediante *system prompts*
- Comprensión del ecosistema Coink (OINKs, billeteras digitales, bases de datos híbridas)
- Construcción de métricas de negocio (Coink Score)
- Comparación crítica con soluciones comerciales y de código abierto

---

## 👨‍💻 Autor

**[Thomas Arismendi]**
Actividad 6 — [Programación de Software SENA]

---

## 📄 Licencia

Este proyecto es de uso educativo. Puedes usarlo, modificarlo y compartirlo libremente.

---

## 🙏 Agradecimientos

- A mis compañeros por prestar sus datos y personalidades
- A la comunidad de Streamlit por la documentación
- A los proyectos **Mushu** y **openpdb** por inspirar el análisis comparativo
- A **Coink** por el contexto sobre los OINKs y su arquitectura de datos