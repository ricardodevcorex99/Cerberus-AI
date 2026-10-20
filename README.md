# 🐕 Cerberus AI - Security Suite

<p align="center">
  <img src="https://img.shields.io/badge/Security-OWASP-blue.svg" alt="OWASP">
  <img src="https://img.shields.io/badge/Python-3.10+-yellow.svg" alt="Python">
  <img src="https://img.shields.io/badge/AI-Gemini%203.8%20Flash-orange.svg" alt="Gemini">
  <img src="https://img.shields.io/badge/Database-MongoDB%20Atlas-green.svg" alt="MongoDB">
  <img src="https://img.shields.io/badge/Platform-Termux%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

Cerberus AI es una **Suite de Ciberseguridad Defensiva y Mini-SIEM** de próxima generación. Actúa como el legendario perro de tres cabezas, protegiendo tus aplicaciones web y móviles mediante el uso de Inteligencia Artificial (**Google Gemini 3.8 Flash**) para auditorías de código semántico, protección de bases de datos y escudos contra Prompt Injection en tiempo real.

---

## 🏛️ Las 3 Cabezas de Cerberus (Arquitectura)

Cerberus AI está dividido en 3 módulos principales, cada uno diseñado para interceptar y neutralizar vectores de ataque modernos.

| Módulo | Nombre | Función Principal | Descripción Técnica |
| :---: | :--- | :--- | :--- |
| **1** | 👁️ **Auditor SAST OWASP** | Detección de Vulnerabilidades | Escanea archivos locales o repositorios remotos de GitHub. Detecta exposición de credenciales (Credential Leaks: MongoDB URI, S3/R2 Keys) y fallos de lógica de negocio asignando un riesgo **OWASP (0-10)**. |
| **2** | 🛡️ **Escáner de Base de Datos** | Prevención de Spam & Inyecciones | Conexión en vivo con **MongoDB Atlas**. Reglas de defensa activa:<br>• **Compradores:** Zero-Tolerance a nombres de personajes (Batman, Superman), trolls, bots o apodos absurdos.<br>• **Vendedores:** Tolerancia a nombres creativos de locales, pero bloqueo estricto a palabras soeces/vulgares.<br>• **NoSQL Injections:** Detección de operadores `$ne`, `$gt`, `$where` y traslado a **Cuarentena**. |
| **3** | 🔥 **Firewall Semántico (WAF)** | Anti Prompt-Injection & L7 Shield | Actúa como un middleware inteligente. Intercepta entradas de texto, reseñas y prompts en tiempo real, evaluando la intención con Gemini para neutralizar inyecciones de comandos maliciosos y jailbreaks. |

---

## 🖥️ Modos de Acceso (Terminal & Web)

1. **Terminal Nativa de macOS / Linux / Termux:**
   ```bash
   python3 main.py
   ```
2. **Terminal Web Embebida en Navegador (Puerto 5055):**
   - Interfaz web interactiva idéntica a Termux para ejecutar módulos desde cualquier navegador.
3. **SIEM Web Dashboard (Puerto 5050):**
   - Panel de control gráfico con métricas, gráficos de **Chart.js** y distribución de severidad de incidentes.

---

## 🚀 Instalación y Despliegue Rápido

Cerberus AI está diseñado para correr nativamente en **macOS**, **Termux (Android)** y **Linux**.

### Requisitos Previos
- Python 3.10 o superior.
- Una API Key de Google Gemini (`gemini-3.8-flash`).

### Pasos de Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/ricardodevcorex99/Cerberus-AI.git
   cd Cerberus-AI
   ```
2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configurar Credenciales:**
   Renombra el archivo `.env.example` a `.env` y coloca tu API Key de Gemini y tu URI de MongoDB:
   ```bash
   cp .env.example .env
   nano .env
   ```
4. **Ejecutar Cerberus:**
   ```bash
   bash start.sh
   # O en macOS con doble clic a: start_security.command
   ```

---

## 📊 Sistema SIEM Integrado (Dashboard)

Cerberus AI incluye un **Dashboard de Gestión de Incidentes** (Módulo 4). Todo ataque interceptado por cualquiera de las 3 cabezas se registra localmente en `data/incidentes.json` con una escala dinámica de severidad:

- 🟢 **EXCELENTE / NULO** (0 - 2)
- 🔵 **BAJO** (3 - 4)
- 🟣 **MEDIO** (5 - 6)
- 🟡 **ALTO** (7 - 8)
- 🔴 **CRÍTICO** (9 - 10)

---

## 💡 Recomendaciones y Casos Específicos

### 1. Usuarios de Termux (Android)
- **Manejo de Sesiones:** Asegúrate de otorgar permisos de almacenamiento a Termux (`termux-setup-storage`) si deseas que Cerberus lea volcados o configuraciones fuera de su carpeta principal.
- **Rendimiento:** Termux puede cerrar procesos en segundo plano para ahorrar batería. Al ejecutar el Módulo 1 (Auditor), mantén la pantalla encendida para evitar desconexiones por timeout.

### 2. Cuotas de la API de Google Gemini (Error 429 / 503)
- Cerberus tiene un sistema de **enfriamiento automático (Retry Loop)**. Si los servidores de Google se saturan, el programa pausará su ejecución durante 15-30 segundos y lo intentará de nuevo automáticamente.

---

## 🤝 Contribución
¡Cerberus AI es de código abierto! Siéntete libre de hacer un *Fork*, mejorar los módulos y enviar un *Pull Request*.
