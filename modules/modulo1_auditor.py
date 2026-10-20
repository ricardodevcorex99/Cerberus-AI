import os
import time
import urllib.request
import urllib.error
from core.ai_engine import analizar_con_ia
from core.dashboard import guardar_incidente

def auditar_codigo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=====================================================================")
    print(" 🛡️  C E R B E R U S   S E C U R I T Y   H A C K E R   A I  🛡️")
    print("=====================================================================")
    print("[Módulo 1] Auditoría de Seguridad SAST (OWASP Top 10 & Credential Leaks)\n")
    print("Selecciona el objetivo a auditar:")
    print("  [ 1 ] Auditar código local de MiVeci App (Controladores, Rutas y APIs)")
    print("  [ 2 ] Auditar archivo remoto desde GitHub (URL Raw)")
    print("  [ 3 ] Cancelar y volver al menú principal\n")
    
    opc = input("root@cerberus-auditor:~# ").strip()
    
    codigo_fuente = ""
    nombre_objetivo = ""
    
    if opc == '1':
        # Auditar código clave de MiVeci
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        parent_dir = os.path.dirname(base_dir)
        
        # Buscar controladores clave de Laravel
        candidate_files = [
            os.path.join(parent_dir, "app/Http/Controllers/AuthController.php"),
            os.path.join(parent_dir, "app/Http/Controllers/AiPhotoEnhancerController.php"),
            os.path.join(parent_dir, "routes/web.php"),
            os.path.join(parent_dir, ".env.example"),
        ]
        
        snippets = []
        for path in candidate_files:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(4000) # Primeros 4KB de cada archivo representativo
                        rel_name = os.path.relpath(path, parent_dir)
                        snippets.append(f"--- ARCHIVO: {rel_name} ---\n{content}\n")
                except Exception:
                    pass
        
        if not snippets:
            print("⚠️ No se encontraron archivos locales de MiVeci. Intenta con la opción 2.")
            input("\nPresiona ENTER para continuar...")
            return
            
        codigo_fuente = "\n".join(snippets)
        nombre_objetivo = "MiVeci Core App (Controllers & Routes)"
        print(f"[*] Código local de MiVeci recopilado ({len(snippets)} archivos clave)...")
        
    elif opc == '2':
        github_url = input("\nIngresa la URL Raw del archivo en GitHub: ").strip()
        if not github_url:
            print("❌ Operación cancelada.")
            time.sleep(1)
            return
            
        try:
            print("[*] Descargando código fuente desde GitHub...")
            req = urllib.request.Request(github_url, headers={'User-Agent': 'Cerberus-Auditor'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                codigo_fuente = resp.read().decode('utf-8', errors='ignore')
                nombre_objetivo = github_url.split('/')[-1]
        except Exception as e:
            print(f"❌ Error al descargar de GitHub: {e}")
            input("\nPresiona ENTER para continuar...")
            return
    else:
        return

    print("\n[*] Enviando código al Motor de Inteligencia Artificial (Auditor OWASP)...")
    prompt = f"""Eres un Auditor Jefe de Ciberseguridad experto en OWASP Top 10 y Mobile/Web Security.
Analiza de forma CRUDA, OBJETIVA y TÉCNICA el siguiente código de la aplicación ({nombre_objetivo}).
Tu trabajo es detectar vulnerabilidades reales:
1. Exposición de secretos y credenciales (MongoDB URI, Cloudflare R2 Keys, Passwords).
2. Inyecciones NoSQL o SQL.
3. Inyecciones de Prompt o manipulación de modelos de IA.
4. Fallos de autorización, autenticación o CORS.

Genera el reporte con esta estructura exacta:
1. 🎯 ARCHIVO / OBJETIVO ANALIZADO: {nombre_objetivo}
2. 🚨 RESULTADO DE AUDITORÍA: Detalla las vulnerabilidades encontradas o explica por qué la arquitectura es segura.
3. 💉 VECTORES DE ATAQUE: Cómo un atacante podría explotar el sistema.
4. 🛡️ PLAN DE REMEDIACIÓN: Pasos técnicos prioritarios.
5. 📊 CALIFICACIÓN OWASP: Asígnale un puntaje del 0 al 10 (Donde 10 es vulnerable crítico y 0 es seguro).
"""

    analisis = analizar_con_ia(prompt, codigo_fuente[:8000])
    
    print("\n" + "="*65)
    print(" 📋 REPORTE DE AUDITORÍA FORENSE OWASP")
    print("="*65)
    print(analisis)
    print("="*65)
    
    # Evaluar severidad para el SIEM
    severidad = "BAJO"
    if "10/10" in analisis or "9/10" in analisis or "CRÍTICO" in analisis.upper():
        severidad = "CRÍTICO"
    elif "8/10" in analisis or "7/10" in analisis or "ALTO" in analisis.upper():
        severidad = "ALTO"
    elif "6/10" in analisis or "5/10" in analisis or "MEDIO" in analisis.upper():
        severidad = "MEDIO"
    elif "0/10" in analisis or "1/10" in analisis or "SEGURO" in analisis.upper():
        severidad = "EXCELENTE"
        
    inc_id = guardar_incidente("Auditor SAST", severidad, f"Auditoría ejecutada sobre {nombre_objetivo}. Veredicto: {severidad}")
    print(f"\n[+] Incidente registrado en el SIEM con ID: {inc_id} ({severidad})")
    input("\nPresiona ENTER para volver al menú...")
