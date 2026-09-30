# 🐕 Cerberus AI - Security Suite

<p align="center">
  <img src="https://img.shields.io/badge/Security-OWASP-blue.svg" alt="OWASP">
  <img src="https://img.shields.io/badge/Python-3.10+-yellow.svg" alt="Python">
  <img src="https://img.shields.io/badge/AI-Gemini%20Flash-orange.svg" alt="Gemini">
  <img src="https://img.shields.io/badge/Platform-Termux%20%7C%20Mac%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

Cerberus AI es una **Suite de Ciberseguridad Open Source** de próxima generación. Actúa como el legendario perro de tres cabezas, protegiendo tus aplicaciones web y repositorios mediante el uso de Inteligencia Artificial (Google Gemini) para auditorías de código semántico en tiempo real.

---

## 🏛️ Las 3 Cabezas de Cerberus (Arquitectura)

Cerberus AI está dividido en 3 módulos principales, cada uno diseñado para interceptar y neutralizar vectores de ataque modernos.

| Módulo | Nombre | Función Principal | Descripción Técnica |
| :---: | :--- | :--- | :--- |
| **1** | 👁️ **Auditor Semántico** | Detección de Vulnerabilidades | Escanea repositorios GitHub o archivos locales. Detecta exposición de credenciales (Credential Leaks) y fallos de lógica de negocio asignando un riesgo **OWASP (0-10)**. |
| **2** | 🛡️ **Escáner de Bases de Datos** | Prevención de Spam & XSS | Analiza volcados JSON de bases de datos (ej. Firebase). Busca inyecciones XSS (Cross-Site Scripting) y patrones de spam antes de que afecten el frontend. |
| **3** | 🔥 **Firewall Semántico (WAF)** | Anti Prompt-Injection | Actúa como un middleware entre el usuario y tu LLM. Intercepta instrucciones (Prompts) en tiempo real, evaluando la intención del usuario para bloquear inyecciones de comandos maliciosos. |

---

## 🚀 Instalación Rápida

Cerberus AI está diseñado para correr nativamente en **Termux (Android)**, **macOS** y **Linux**.

### Requisitos Previos
- Python 3.10 o superior.
- Una API Key de Google Gemini.

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
   Renombra el archivo `.env.example` a `.env` y coloca tu API Key de Gemini:
   ```bash
   cp .env.example .env
   nano .env
   ```
4. **Ejecutar Cerberus:**
   ```bash
   python main.py
   ```

---

## 📊 Sistema SIEM Integrado (Dashboard)

Cerberus AI incluye un **Dashboard de Gestión de Incidentes** (Módulo 4). Todo ataque interceptado por cualquiera de las 3 cabezas se registra localmente en `data/incidentes.json` con una escala dinámica de severidad:

- 🟢 **EXCELENTE / NULO** (0 - 2)
- 🔵 **BAJO** (3 - 4)
- 🟣 **MEDIO** (5 - 6)
- 🟡 **ALTO** (7 - 8)
- 🔴 **CRÍTICO** (9 - 10)

## 🤝 Contribución
¡Cerberus AI es de código abierto! Siéntete libre de hacer un *Fork*, mejorar los módulos y enviar un *Pull Request*. 
