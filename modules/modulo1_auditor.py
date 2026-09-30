import time
import requests
import os
from core.ai_engine import analizar_con_ia
from core.dashboard import guardar_incidente

def auditar_codigo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("========================================")
    print("   🛡️  C E R B E R U S   S E C U R I T Y   H A C K E R   A I 🛡️")
    print("========================================")
    print("[Módulo 1] Auditoría de Despliegue (Vercel/GitHub/Firebase)")
    print("Conectando en tiempo real con:")
    print(" 🌐 Vercel: the-barber-shop.vercel.app")
    print(" 📂 GitHub: ricardodevcorex99/the-barber-shop")
    print(" 🔥 Firebase: the-barber-shop-c623b\n")
    
    github_url = "https://raw.githubusercontent.com/ricardodevcorex99/the-barber-shop/refs/heads/main/chatbot.js"
    
    try:
        print("[*] Descargando código frontend (chatbot.js) desde GitHub (Vinculado a Vercel)...")
        respuesta_git = requests.get(github_url)
        
        if respuesta_git.status_code == 200:
            codigo_fuente = respuesta_git.text
            print("[+] Código descargado con éxito. (Mostrando las primeras líneas)")
            print(codigo_fuente[:150] + "...\n")
            
            print("[*] Pasando el código por la Inteligencia Artificial (Auditor OWASP)...")
            time.sleep(1) 
            
            prompt = """Eres un Auditor Jefe de Ciberseguridad experto en OWASP.
Analiza de forma CRUDA, OBJETIVA y TÉCNICA el siguiente código fuente del frontend (`chatbot.js`).
Tu trabajo es detectar vulnerabilidades reales (Ej. Exposición de secretos, Inyección de código, Inyección de Prompt, fallos de configuración, etc.).
No asumas vulnerabilidades que no existen, pero si encuentras una, detállala con máxima severidad.

Genera el reporte con esta estructura exacta:
1. 🎯 ARCHIVO ANALIZADO: the-barber-shop/chatbot.js
2. 🚨 RESULTADO DE AUDITORÍA: Detalla las vulnerabilidades encontradas (si las hay) o explica por qué la arquitectura actual es segura.
3. 💉 ANÁLISIS DE VECTORES DE ATAQUE: Explica cómo un atacante podría explotar el código actual (o por qué no podría hacerlo).
4. 🛡️ PLAN DE REMEDIACIÓN: Pasos técnicos para solucionar los fallos encontrados (si aplica).
5. 📊 CALIFICACIÓN OWASP: Del 0 al 10 (donde 0 es seguridad total y 10 es riesgo crítico). Sé estricto y objetivo."""
            resultado_ia = analizar_con_ia(prompt, codigo_fuente[:3000])
            
            print("\n================ REPORTE DE AUDITORÍA ================")
            print(f"\033[96m{resultado_ia}\033[0m")
            print("======================================================")
            
            import re
            # Buscar el puntaje en formato X/10 o X / 10
            match = re.search(r'(\d+)\s*/\s*10', resultado_ia)
            if match:
                score = int(match.group(1))
                if score >= 9:
                    severidad = "CRÍTICO"
                elif score >= 7:
                    severidad = "ALTO"
                elif score >= 5:
                    severidad = "MEDIO"
                elif score >= 3:
                    severidad = "BAJO"
                elif score >= 1:
                    severidad = "NULO"
                else:
                    severidad = "EXCELENTE"
            else:
                severidad = "INDEFINIDO"
                
            id_incidente = guardar_incidente("Auditoría de Código", severidad, resultado_ia)
            print(f"\n💾 \033[92m[INFO] El reporte se ha guardado en tu Dashboard con el ID: {id_incidente} (Severidad: {severidad})\033[0m")
            
        else:
            print(f"❌ Error al conectar con GitHub. HTTP: {respuesta_git.status_code}")
            
    except Exception as e:
        print(f"❌ Error de red: {e}")
        
    input("\nPresiona ENTER para volver al menú...")
