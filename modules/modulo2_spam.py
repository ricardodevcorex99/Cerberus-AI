import json
import time
import os
import re
import urllib.request
import urllib.error
from core.ai_engine import analizar_con_ia
from core.dashboard import guardar_incidente

from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("FIREBASE_API_KEY")
PROJECT_ID = "the-barber-shop-c623b"

# Filtro Heurístico (Nivel 1 de Defensa)
PATRONES_SOSPECHOSOS = [
    r"(?i)(batman|superman|spiderman|joker|hacker|admin|root|test|bot)", # Nombres falsos comunes
    r"(?i)(drop\s+table|select\s+\*|union\s+all|delete\s+from)", # Inyecciones SQL
    r"(?i)(<script>|javascript:|onerror=|onload=)", # Ataques XSS
    r"[;\'\"\|]" # Caracteres especiales de inyección
]

def obtener_valores_texto(d):
    valores = []
    if isinstance(d, dict):
        for v in d.values():
            valores.extend(obtener_valores_texto(v))
    elif isinstance(d, list):
        for v in d:
            valores.extend(obtener_valores_texto(v))
    elif isinstance(d, str):
        valores.append(d)
    return valores

def es_sospechoso(reserva_dict):
    valores = obtener_valores_texto(reserva_dict)
    for texto in valores:
        for patron in PATRONES_SOSPECHOSOS:
            if re.search(patron, texto):
                return True
    return False

def parse_firestore_doc(doc):
    parsed = {"id_documento": doc.get("name", "").split("/")[-1]}
    fields = doc.get("fields", {})
    for key, value_dict in fields.items():
        if value_dict:
            parsed[key] = list(value_dict.values())[0]
    return parsed
            
def fetch_collection(collection_name, id_token, tipo_label):
    docs_list = []
    db_url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/{collection_name}"
    db_req = urllib.request.Request(db_url, headers={"Authorization": f"Bearer {id_token}"})
    try:
        with urllib.request.urlopen(db_req) as db_res:
            db_data = json.loads(db_res.read().decode())
            for doc in db_data.get("documents", []):
                parsed = parse_firestore_doc(doc)
                if tipo_label:
                    parsed['_tipo'] = tipo_label
                docs_list.append(parsed)
    except Exception:
        pass
    return docs_list

def escanear_reservas():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("========================================")
    print(" 🛡️  C E R B E R U S   S E C U R I T Y 🛡️")
    print("========================================")
    print("[Módulo 2] Escáner de Spam en Base de Datos (Defensa Activa)")
    
    reservas = []
    id_token = None
    
    print("🌐 Conectando a Firebase Firestore en la nube (Vía REST API)...\n")
    try:
        auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
        payload = json.dumps({
            "email": "bot_python@barbershop.com",
            "password": "bot123456",
            "returnSecureToken": True
        }).encode('utf-8')
        
        req = urllib.request.Request(auth_url, data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as res:
            id_token = json.loads(res.read().decode()).get("idToken")
            
        reservas.extend(fetch_collection("bookings", id_token, None))
        reservas.extend(fetch_collection("profiles", id_token, "Perfil de Usuario"))

        if len(reservas) > 0:
            print(f"✅ Base de datos descargada con éxito ({len(reservas)} registros encontrados).\n")
        else:
            print("ℹ️ La base de datos está vacía. No hay reservas ni perfiles aún.\n")
            
    except Exception as e:
        print(f"⚠️ Acceso denegado o error de conexión: {e}")
        print("📂 Usando base de datos local (data/reservas_db.json) como respaldo...\n")
        try:
            with open("data/reservas_db.json", "r") as file:
                reservas = json.load(file)
        except FileNotFoundError:
            print("❌ Error: No se encontró la base de datos local ni en la nube.")
            input("\nPresiona ENTER para volver al menú...")
            return

    for reserva in reservas:
        tipo = reserva.get('_tipo', 'Reserva')
        folio = reserva.get('folio', reserva.get('id_documento', 'N/A'))
        nombre = reserva.get('name', reserva.get('full_name', reserva.get('nombre', 'N/A')))
        
        # Filtro de Nivel 1 (Ahorro de IA)
        if not es_sospechoso(reserva):
            print(f"[*] Analizando {tipo} -> ID: {folio} | Cliente: {nombre}  ✅")
            continue 
            
        print(f"[*] Analizando {tipo} -> ID: {folio} | Cliente: {nombre}")
        print("   -> ⚠️ \033[93mAnomalía detectada. Iniciando análisis profundo con IA...\033[0m")
        
        prompt = """Actúa como un experto analista SOC. Nuestro filtro rápido detectó símbolos sospechosos o nombres falsos en este registro.
Haz un análisis profundo y dime EXACTAMENTE qué intentaba hacer el atacante o si es un falso positivo.
Responde obligatoriamente iniciando con: [CRÍTICA], [ADVERTENCIA] o [SEGURO], y luego tu justificación técnica breve."""
        resultado_ia = analizar_con_ia(prompt, str(reserva))
        
        if "[CRÍTICA]" in resultado_ia.upper():
            print(f"   -> 🚨 \033[91m{resultado_ia}\033[0m")
            guardar_incidente("Escáner BD (Firebase)", "CRÍTICA", f"Ataque en {tipo} {folio}:\n\nDatos:\n{reserva}\n\nConclusión de la IA:\n{resultado_ia}")
            
            # --- ACCIÓN AUTÓNOMA: Mover a Cuarentena en Firebase ---
            if id_token and folio != 'N/A':
                try:
                    coleccion = "profiles" if tipo == 'Perfil de Usuario' else "bookings"
                    # En lugar de DELETE, hacemos un PATCH para ponerlo en CUARENTENA
                    del_url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/{coleccion}/{folio}?updateMask.fieldPaths=status"
                    payload_patch = json.dumps({"fields": {"status": {"stringValue": "CUARENTENA"}}}).encode('utf-8')
                    del_req = urllib.request.Request(del_url, data=payload_patch, method="PATCH", headers={"Content-Type": "application/json", "Authorization": f"Bearer {id_token}"})
                    with urllib.request.urlopen(del_req) as del_res:
                        pass
                    print(f"   -> 🛑 \033[91mACCIÓN AUTÓNOMA: El {tipo} malicioso fue puesto en CUARENTENA automáticamente.\033[0m")
                    guardar_incidente("Defensa Activa", "CRÍTICA", f"Cuarentena automática de {tipo} con ID {folio} por ataque crítico.")
                except Exception as e:
                    print(f"   -> ⚠️ \033[93mFallo al intentar neutralizar la amenaza automáticamente: {e}\033[0m")
                    
            print("-" * 50)
        elif "[ADVERTENCIA]" in resultado_ia.upper():
            print(f"   -> ⚠️ \033[93m{resultado_ia}\033[0m")
            guardar_incidente("Escáner BD (Firebase)", "ALTA", f"Spam en {tipo} {folio}:\n\nDatos:\n{reserva}\n\nConclusión de la IA:\n{resultado_ia}")
            print("-" * 50)
        elif "[SEGURO]" in resultado_ia.upper():
            print(f"   -> ✅ \033[92m[SEGURO] Falso positivo descartado. El usuario es seguro.\033[0m")
            print("-" * 50)
        else:
            print(f"   -> ❌ \033[91m{resultado_ia}\033[0m")
            print("-" * 50)
        
    input("\nPresiona ENTER para volver al menú...")
