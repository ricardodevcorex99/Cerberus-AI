# 🧠 Transferencia de Memoria: THE BARBER SHOP AI SECURITY SUITE

Hola, Antigravity. Si estás leyendo este archivo, acabas de despertar en el entorno de la Mac Neo de Ricardo para continuar el proyecto del Summer Camp 2026. Este archivo funciona como un volcado de memoria (Memory Dump) para que sepas exactamente qué hemos construido, cómo funciona la arquitectura y cuáles son las preferencias de Ricardo.

## 👤 Perfil del Usuario
*   **Nombre:** Ricardo (Arquitecto de Software y Ciberseguridad).
*   **Proyecto:** "THE BARBER SHOP" - Summer Camp 2026.
*   **Enfoque:** Código estrictamente profesional, reportes de seguridad crudos/objetivos y alta tolerancia a la innovación (ej. SIEM Dashboards).

## 🏗️ Arquitectura del Sistema (Python CLI)
El proyecto principal es una **AI Security Suite** modular. Para ejecutarla se usa `python main.py`.
*   `core/ai_engine.py`: Conexión robusta a Gemini (3.5 Flash) que incluye algoritmos de retry (enfriamiento) para evadir errores 503 y 429 (Límite de cuota).
*   `core/dashboard.py`: Un SIEM ligero que guarda logs en `data/incidentes.json` con escalado dinámico de severidad por colores (CRÍTICO, ALTO, MEDIO, BAJO, NULO, EXCELENTE).
*   `modules/modulo1_auditor.py`: Un auditor de código OWASP que descarga archivos directo de GitHub. El prompt está configurado para ser extremadamente crudo y objetivo. Evalúa del 0 al 10.
*   `modules/modulo2_spam.py`: Escáner defensivo de base de datos (`reservas_db.json`).
*   `modules/modulo3_firewall.py`: Escudo semántico en tiempo real contra Prompt Injection.

## 🛡️ Contexto de Desarrollo Frontend (Vercel)
*   En el frontend original de Vercel, descubrimos vulnerabilidades de exposición de API Key y Prompt Injection.
*   **Solución implementada:** Se migró la comunicación a Vercel Serverless Functions (`/api/chat.js`) utilizando `systemInstruction` para aislar el prompt, asegurando una nota de 0/10 en riesgo.

## ⚙️ Reglas de Comportamiento para ti
1.  **Mantén la modularidad:** Cualquier nueva función debe respetar la división entre `core/` y `modules/`.
2.  **Actúa sin rodeos:** Ricardo valora la eficiencia. Si él pide algo, aplícalo directamente.
3.  **Seguridad por diseño:** Nunca sugieras poner secretos en el lado del cliente (Frontend). Protege siempre el archivo `.env`.

¡Estás listo para asistir a Ricardo en su Mac Neo!
