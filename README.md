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
- [🎭 Parte 2: Chatbot con Personalidad](#-parte-2-chatbot-con-personalidad)
- [4. Vigilancia Tecnológica](#4-vigilancia-tecnológica-soluciones-de-hardware-y-software)
- [5. Servicios de Nube](#5-servicios-de-nube-para-bases-de-datos-aws-google-cloud-azure-oracle-e-ibm)
- [🚀 Instalación](#-instalación)
- [▶️ Uso](#️-uso)
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

# 4. Vigilancia Tecnológica: Soluciones de Hardware y Software

## Introducción

La vigilancia tecnológica permite identificar el estado del arte en un campo específico mediante la consulta de bases de datos de patentes como **Lens Patents, USPTO, Patentscope y SpaceNet**. A continuación se presentan **5 tecnologías** relacionadas con hardware/software financiero, indicando cómo se vinculan con bases de datos y su utilidad práctica.

---

## Tecnología 1: Cajeros Automáticos con Módulo de Depósito Seguro (ATM con Cash Deposit Bin)

**Fuente:** Google Patents / USPTO – Patente US20100247000

**Descripción técnica:**
Un cajero automático equipado con un compartimento de depósito seguro que recibe efectivo. El sistema incluye un contenedor que **sella automáticamente el efectivo** cuando se abre el compartimento, evitando robos por parte de técnicos o transportadores de valores. Incorpora un **dispositivo de bloqueo con sensor de acceso** que registra fecha, hora e identificación del usuario en cada evento de apertura. Opcionalmente incluye **etiqueta RFID** para rastreo y un **sistema de alerta** ante accesos no autorizados.

**Relación con bases de datos:**
- **Datos estructurados:** logs de acceso (fecha, hora, usuario, ID del contenedor).
- **Base de datos relacional:** ideal para garantizar integridad referencial entre transacciones y auditoría.
- **Datos de rastreo RFID:** pueden almacenarse en tablas de eventos con índices por timestamp.

**Utilidad:**
- Prevención de fraude interno en el manejo de efectivo.
- Trazabilidad completa de cada apertura del compartimento.
- Auditoría automatizada para cumplimiento normativo.

---

## Tecnología 2: Máquina Bancaria Automática con Comunicación Inalámbrica NFC

**Fuente:** WO2015082346A1 – Patentscope (WIPO)

**Descripción técnica:**
Un cajero automático con **cassettes de efectivo inteligentes** que se comunican con la unidad de control central mediante **Near Field Communication (NFC)**. Cada cassette incluye un transmisor/receptor y una **unidad de almacenamiento de energía** que se carga de forma inalámbrica por inducción electromagnética. La unidad de control usa un **multiplexor** para gestionar múltiples antenas NFC, reduciendo hardware y consumo energético.

**Relación con bases de datos:**
- **Datos de estado del hardware:** nivel de batería, estado de cada cassette, versión de firmware.
- **Base de datos NoSQL (documental):** ideal para almacenar telemetría variable y esquemas flexibles.
- **Historial de cargas y transacciones:** requiere base relacional para consistencia transaccional.

**Utilidad:**
- Mantenimiento predictivo basado en telemetría de los cassettes.
- Reducción de costos operativos (menos hardware, menos energía).
- Actualizaciones de firmware remotas mediante datos NFC.

---

## Tecnología 3: ATM con API para Aplicaciones de Terceros y Mecanismo de Depósito de Efectivo

**Fuente:** US11494747 – USPTO

**Descripción técnica:**
Un cajero automático que permite la instalación de **aplicaciones de terceros** mediante una **API expuesta**. El ATM incluye periféricos como **mecanismo de depósito de efectivo** y componentes GPS. La aplicación de terceros puede acceder a los periféricos **sin acceder a información financiera del usuario**, manteniendo un aislamiento seguro. El sistema permite operaciones como **pago de servicios** aplicando el depósito de efectivo directamente a la cuenta del tercero.

**Relación con bases de datos:**
- **Base relacional:** cuentas de usuario, transacciones, relaciones con terceros.
- **Base de grafos:** relaciones entre usuarios, servicios de terceros y transacciones.
- **Base de datos de documentos:** logs de sesiones de API y eventos de seguridad.

**Utilidad:**
- Ecosistema abierto de servicios financieros en el ATM.
- Nuevas fuentes de ingreso (comisiones por transacciones de terceros).
- Trazabilidad completa de operaciones API.

---

## Tecnología 4: Sistema de Procesamiento de Transacciones con Identificación Biométrica

**Fuente:** US9697698 – USPTO

**Descripción técnica:**
Un sistema que usa **cámaras y sensores** para capturar imágenes de usuarios y compararlas con **datos almacenados** en una base de datos de usuarios autorizados. Si los datos de la cámara coinciden con datos de usuario no autorizado, el sistema activa **alarmas audibles, mensajes remotos o apagado de la máquina**. Los datos de imagen, audio y otros sensores se almacenan en un **data store** que puede estar local o accesible remotamente mediante red TCP/IP.

**Relación con bases de datos:**
- **Base de datos de imágenes:** almacenamiento de rostros para reconocimiento facial.
- **Base NoSQL:** adecuada para datos no estructurados (imágenes, audio).
- **Base relacional:** usuarios autorizados, permisos, logs de acceso.

**Utilidad:**
- Seguridad física del ATM contra usuarios no autorizados.
- Registro forense de intentos de acceso.
- Integración con sistemas de video-vigilancia.

---

## Tecnología 5: Sistema de Gestión de Efectivo con Integración de Pagos Electrónicos

**Fuente:** WO2017042618A1 – Patentscope (WIPO)

**Descripción técnica:**
Un sistema que integra **pago automático en efectivo** en estaciones de servicio con la **recarga de reservas de efectivo** para cajeros automáticos. El sistema incluye un **programa de computadora** que hace interoperar dos mundos: sistemas de gestión de negocios y sistemas bancarios. El efectivo usado para pagos se recicla para cargar los ATM, optimizando la logística de efectivo.

**Relación con bases de datos:**
- **Base relacional:** transacciones de pago, inventario de efectivo por ubicación.
- **Data warehouse:** análisis de flujos de efectivo entre estaciones y ATMs.
- **Base de datos en tiempo real:** monitoreo de niveles de efectivo en cada punto.

**Utilidad:**
- Optimización logística de efectivo (reducción de costos de transporte).
- Integración de pagos en efectivo y electrónicos en un solo sistema.
- Reducción de la huella de carbono al minimizar transportes de valores.

---

## Resumen de Tecnologías y su Relación con Bases de Datos

| # | Tecnología | Fuente | Tipo de BD Principal | Utilidad Clave |
|---|------------|--------|---------------------|----------------|
| 1 | ATM con depósito seguro | US20100247000 | Relacional (auditoría) | Prevención de fraude interno |
| 2 | Cassettes NFC inalámbricos | WO2015082346A1 | NoSQL (telemetría) | Mantenimiento predictivo |
| 3 | ATM con API terceros | US11494747 | Relacional + Grafos | Ecosistema abierto |
| 4 | Identificación biométrica | US9697698 | NoSQL + Relacional | Seguridad física |
| 5 | Gestión de efectivo integrada | WO2017042618A1 | Relacional + DW | Optimización logística |

---

# 5. Servicios de Nube para Bases de Datos: AWS, Google Cloud, Azure, Oracle e IBM

## Introducción

Las principales plataformas de nube ofrecen servicios gestionados de bases de datos que abarcan desde **relacionales tradicionales (SQL)** hasta **NoSQL**, **series temporales**, **grafos** y **libros mayores**.

---

## 5.1 Amazon Web Services (AWS)

| Tipo | Servicio | Descripción | Ideal para |
|------|----------|-------------|------------|
| **Relacional** | Amazon RDS | SQL Server, Oracle, MySQL, MariaDB, PostgreSQL gestionados | OLTP tradicional |
| **Relacional** | Amazon Aurora | MySQL/PostgreSQL compatible, alto rendimiento | Aplicaciones críticas |
| **Relacional (DW)** | Amazon Redshift | Almacenamiento columnar, análisis masivo | Data warehousing |
| **NoSQL (clave-valor)** | Amazon DynamoDB | Latencia de milisegundos, escala automática | Apps web, e-commerce |
| **NoSQL (documental)** | Amazon DocumentDB | Compatible con MongoDB | Contenido, catálogos, perfiles |
| **NoSQL (grafo)** | Amazon Neptune | Consultas de relaciones complejas | Detección de fraude, redes sociales |
| **NoSQL (columnar)** | Amazon Keyspaces | Compatible con Cassandra | IoT, series temporales |
| **In-memory** | ElastiCache / MemoryDB | Redis / Memcached | Caché, sesiones, leaderboards |
| **Libro mayor** | Amazon QLDB | Registro inmutable y verificable | Transacciones bancarias |
| **Objetos** | Amazon S3 | Almacenamiento de datos no estructurados | Data lakes, backups |

---

## 5.2 Google Cloud Platform (GCP)

| Tipo | Servicio | Descripción | Ideal para |
|------|----------|-------------|------------|
| **Relacional** | Cloud SQL | MySQL, PostgreSQL, SQL Server gestionados | Aplicaciones tradicionales |
| **Relacional (global)** | Cloud Spanner | Escala global, consistencia fuerte, ACID | Sistemas bancarios globales |
| **Relacional (analítico)** | BigQuery | Columnar, serverless, análisis masivo | OLAP, reportes |
| **NoSQL (documental)** | Firestore | MongoDB compatible, sincronización en tiempo real | Apps móviles/web |
| **NoSQL (columnar)** | Cloud Bigtable | Alto throughput, baja latencia | IoT, telemetría, time-series |
| **In-memory** | Memorystore | Redis / Memcached gestionado | Caché, sesiones |

---

## 5.3 Microsoft Azure

| Tipo | Servicio | Descripción | Ideal para |
|------|----------|-------------|------------|
| **Relacional** | Azure SQL Database | PaaS totalmente gestionado, motor SQL Server | OLTP, aplicaciones empresariales |
| **Relacional** | Azure SQL Managed Instance | SQL Server con configuración flexible | Migración lift-and-shift |
| **Relacional** | SQL Server en VM | Control total del sistema operativo | Cargas personalizadas |
| **NoSQL (multi-modelo)** | Azure Cosmos DB | Documentos JSON, clave-valor, grafos, columnar | Apps globales de alto rendimiento |
| **Objetos** | Azure Storage | Archivos, blobs, colas, tablas | Datos no estructurados |
| **Analítica unificada** | Microsoft Fabric | Ingesta, ingeniería, DW, BI en un solo servicio | Análisis end-to-end |

---

## 5.4 Oracle Cloud Infrastructure (OCI)

| Tipo | Servicio | Descripción | Ideal para |
|------|----------|-------------|------------|
| **Relacional (autónomo)** | Oracle Autonomous Database | Auto-parcheo, auto-tuning, auto-scaling | OLTP, DW, JSON |
| **Relacional (autónomo)** | Autonomous Transaction Processing | Optimizado para OLTP | Aplicaciones críticas |
| **Relacional (autónomo)** | Autonomous Data Warehouse | Optimizado para analítica | Data warehousing |
| **NoSQL (JSON)** | Autonomous JSON Database | Documentos JSON con SQL | Apps NoSQL |
| **Relacional** | MySQL HeatWave | MySQL con acelerador in-memory | Análisis en tiempo real |
| **Relacional** | Oracle Database en VM/Bare Metal | Control total | Cargas personalizadas |

---

## 5.5 IBM Cloud

| Tipo | Servicio | Descripción | Ideal para |
|------|----------|-------------|------------|
| **Relacional** | IBM Db2 on Cloud | SQL totalmente gestionado | OLTP, aplicaciones empresariales |
| **Relacional** | IBM Cloud Databases for PostgreSQL | PostgreSQL gestionado | Apps modernas |
| **NoSQL (documental)** | IBM Cloud Databases for MongoDB | MongoDB gestionado | Contenido, catálogos |
| **NoSQL (clave-valor)** | IBM Cloud Databases for Redis | Redis gestionado | Caché, sesiones |
| **NoSQL (columnar)** | IBM Cloud Databases for Cassandra | Cassandra gestionado | IoT, series temporales |
| **NoSQL (grafo)** | IBM Cloud Databases for Elasticsearch | Búsqueda y análisis | Logs, observabilidad |
| **Blockchain** | IBM Blockchain Platform | Libro mayor distribuido | Trazabilidad, contratos inteligentes |

---

## 5.6 Tabla Comparativa de Servicios de Nube para Bases de Datos

| Característica | AWS | Google Cloud | Azure | Oracle | IBM |
|----------------|-----|--------------|-------|--------|-----|
| **Relacional gestionado** | RDS, Aurora | Cloud SQL, Spanner | Azure SQL | Autonomous DB | Db2, PostgreSQL |
| **NoSQL documental** | DocumentDB | Firestore | Cosmos DB | Autonomous JSON | MongoDB |
| **NoSQL clave-valor** | DynamoDB | (Firestore) | Cosmos DB | (NoSQL DB) | Redis |
| **NoSQL grafo** | Neptune | (Spanner) | Cosmos DB (Gremlin) | (Graph) | (Elasticsearch) |
| **NoSQL columnar** | Keyspaces | Bigtable | Cosmos DB (Cassandra) | (NoSQL DB) | Cassandra |
| **In-memory** | ElastiCache, MemoryDB | Memorystore | Azure Cache for Redis | (NoSQL DB) | Redis |
| **Data Warehouse** | Redshift | BigQuery | Synapse/Fabric | Autonomous DW | Db2 Warehouse |
| **Libro mayor** | QLDB | (No) | (No) | (Blockchain) | Blockchain Platform |
| **Datos no estructurados** | S3 | Cloud Storage | Blob Storage | Object Storage | Cloud Object Storage |
| **Base global ACID** | Aurora Global | Spanner | Cosmos DB | Autonomous DB | (No) |

---

## 5.7 Análisis y Recomendación para Coink

| Necesidad Coink | Servicio Recomendado | Justificación |
|-----------------|---------------------|---------------|
| Transacciones financieras (ACID) | AWS Aurora / Azure SQL / Oracle Autonomous TP | Consistencia transaccional obligatoria |
| Telemetría IoT de OINKs | AWS DynamoDB / GCP Bigtable / Azure Cosmos DB | Escritura masiva, esquema flexible |
| Análisis de depósitos y usuarios | AWS Redshift / GCP BigQuery / Azure Fabric | OLAP para reportes y dashboards |
| Datos no estructurados | AWS S3 / GCP Cloud Storage / Azure Blob | Almacenamiento económico y escalable |
| Caché de sesiones de app móvil | AWS ElastiCache / GCP Memorystore / Azure Cache | Baja latencia |

**Recomendación:** Un enfoque **multi-nube** o **híbrido** usando AWS como principal (por su portafolio más completo) y GCP BigQuery para analítica avanzada.

---

## Referencias

1. Lens. (2024). Introducing the New Lens. https://lens.xyz/news/introducing-the-new-lens
2. USPTO. (s.f.). Goods and Services Section.
3. WIPO. (2015). WO2015082346A1 – Geldautomat mit NFC-Kommunikation.
4. INPI. (2024). Brevet EP1889327.
5. WIPO. (2025). CWS/13/21 – Report on Technical Assistance.
6. AWS. (2024). Using Power BI with AWS Cloud.
7. Microsoft Learn. (2026). Descripción de los servicios de datos de Azure.
8. USPTO. Patent 013 – Digital Cash Transactions.
9. WIPO. (2007). WO2007036915A1 – Automatic Banking Machine.
10. Astrome. SpaceNet – Satellite Communication Network.
11. WIPO. (2017). PCT/WG/11/5 – Patent Family Citations.
12. AWS. TNC204 – Purpose-built Databases on AWS.
13. IBM. (2025). IBM Cloud Database Services. https://www.ibm.com/mx-es/products/cloud-databases
14. Google Cloud. (2025). Databases Documentation. https://docs.cloud.google.com/docs/databases
15. Oracle. Oracle Cloud Infrastructure Platform Overview.
16. USPTO. US11494747 – ATM with Third-Party Application API.
17. USPTO. US9384637 – Automated Banking Machine.
18. USPTO. US20100247000 – Secure ATM Deposit Bin.
19. WIPO. (2017). WO2017042618A1 – Cash Management System.
20. Oracle. (2025). Autonomous AI Database Workload Types.

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
git clone https://github.com/ThomasStev-Moon/ACTIVIDAD-6.git
cd ACTIVIDAD-6
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

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## ▶️ Uso

### 🏦 Dashboard de Coink

```bash
streamlit run app.py
```

Abre en `http://localhost:8501`.

### 🎭 Chatbot con Personalidad

```bash
streamlit run main.py
```

### 📊 Script de análisis batch

```bash
python analisis_coink.py
```

Genera `usuarios_calificados.csv` y `coink_analisis.png`.

---

## 📁 Estructura del proyecto

```
ACTIVIDAD-6/
├── .venv/                      # Entorno virtual (no subir a Git)
├── app.py                      # Dashboard Streamlit de Coink
├── main.py                     # Chatbot con Personalidad
├── analisis_coink.py           # Script batch de análisis
├── depositos_oinks.csv         # Dataset de depósitos
├── requirements.txt            # Dependencias
├── README.md                   # Este archivo
└── .gitignore                  # Archivos ignorados por Git
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

Asegúrate de que el CSV esté en la **misma carpeta** que los scripts.

### El script `analisis_coink.py` se ve en blanco en Streamlit

Ese archivo es un **script batch de consola**. Ejecútalo con `python analisis_coink.py`, no con `streamlit run`.

### El micrófono no funciona

Instala PyAudio con `pip install pipwin` y luego `pipwin install pyaudio`.

---

## 🛠️ Tecnologías usadas

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/) + [Seaborn](https://seaborn.pydata.org/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [PyAudio](https://pypi.org/project/PyAudio/)

---

## 📚 Aprendizajes

- Creación de entornos virtuales en VS Code
- Uso de `st.session_state` para mantener estado entre recargas
- Manejo de audio en Python (entrada y salida)
- Diseño de personalidades mediante *system prompts*
- Comprensión del ecosistema Coink (OINKs, billeteras digitales, bases de datos híbridas)
- Construcción de métricas de negocio (Coink Score)
- Vigilancia tecnológica con patentes (USPTO, WIPO, Lens)
- Comparación de servicios de nube (AWS, GCP, Azure, Oracle, IBM)

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