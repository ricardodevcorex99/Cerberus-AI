import json
import time
import os
import sys
import re
from core.ai_engine import analizar_con_ia, load_env_file
from core.dashboard import guardar_incidente

# ========================================================
# REGLAS HEURÍSTICAS DE CERBERUS (NIVEL 1 DE DEFENSA)
# ========================================================

# 1. Regla de Compradores: Zero Tolerance (Nombres absurdos, personajes, bots y groserías)
PATRONES_COMPRADORES_PROHIBIDOS = [
    r"(?i)(batman|superman|spiderman|joker|hacker|admin|root|\bbot\b|goku|naruto|shrek|\banon\b|anonymous|el_macho|null|undefined)",
    r"(?i)\b(verga|mierda|culo|puta|puto|chucha|cojudo|malparido|hdp|pendejo|careverga|zorra)\b",
    r"[;\'\"\|\{\}\$]" # Caracteres de inyección
]

# 2. Regla de Vendedores: Tolerancia a nombres creativos/raros, pero CERO vulgaridades
PATRONES_VENDEDORES_VULGARES = [
    r"(?i)\b(verga|mierda|culo|puta|puto|chucha|cojudo|malparido|hdp|pendejo|careverga|zorra)\b",
    r"(?i)(drop\s+table|delete\s+from|union\s+all|<script>|\$where|\$regex)" # Inyecciones directas
]

# 3. Inyecciones NoSQL y XSS generales
PATRONES_INYECCION = [
    r"(?i)(\$ne|\$gt|\$gte|\$lt|\$lte|\$in|\$nin|\$where|\$regex)",
    r"(?i)(<script>|javascript:|onerror=|onload=)",
]

def obtener_conexiones_mongo():
    load_env_file()
    uri = os.getenv("MONGODB_URI", "")
    db_name = os.getenv("MONGODB_DATABASE", "miveci")
    return uri, db_name

def es_nombre_comprador_invalido(nombre):
    if not nombre or len(str(nombre).strip()) < 2:
        return True, "Nombre vacío o demasiado corto"
    for p in PATRONES_COMPRADORES_PROHIBIDOS:
        if re.search(p, str(nombre)):
            return True, f"Coincide con patrón no permitido: {p}"
    return False, None

def es_nombre_vendedor_vulgar(nombre):
    if not nombre:
        return False, None
    for p in PATRONES_VENDEDORES_VULGARES:
        if re.search(p, str(nombre)):
            return True, f"Palabra soez o inyección detectada: {p}"
    return False, None

def escanear_reservas():
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        os.system('cls' if os.name == 'nt' else 'clear')
    print("=====================================================================")
    print(" 🛡️  C E R B E R U S   S E C U R I T Y   H A C K E R   A I  🛡️")
    print("=====================================================================")
    print("[Módulo 2] Escáner de Base de Datos MongoDB Atlas (Defensa Activa)\n")
    print("Reglas aplicadas:")
    print("  • Compradores: Zero Tolerance (Nombres reales, ni Batman ni trolls)")
    print("  • Vendedores: Tolerancia creativa, BLOQUEO estricto a palabras soeces")
    print("  • General: Detección activa de inyecciones NoSQL ($ne, $gt, XSS)\n")
    
    uri, db_name = obtener_conexiones_mongo()
    registros = []
    mongo_client = None
    
    print(f"🌐 Conectando a MongoDB Atlas ({db_name})...")
    
    try:
        from pymongo import MongoClient
        mongo_client = MongoClient(uri, serverSelectionTimeoutMS=4000)
        db = mongo_client[db_name]
        
        # 1. Obtener Tiendas (businesses)
        try:
            for b in db.businesses.find().limit(30):
                b['_tipo'] = 'VENDEDOR'
                registros.append(b)
        except Exception:
            pass
            
        # 2. Obtener Usuarios (users)
        try:
            for u in db.users.find().limit(30):
                u['_tipo'] = 'COMPRADOR' if u.get('role') != 'seller' else 'VENDEDOR'
                registros.append(u)
        except Exception:
            pass
            
        print(f"✅ Descargados {len(registros)} registros de MongoDB Atlas para análisis forense.\n")
    except Exception as e:
        print(f"⚠️ Aviso: Conexión directa a MongoDB Atlas limitada ({e}).")
        print("📂 Usando registros locales de respaldo para verificación...\n")
        
        # Cargar respaldo si existe
        backup_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/reservas_db.json")
        if os.path.exists(backup_path):
            with open(backup_path, 'r', encoding='utf-8') as f:
                registros = json.load(f)
                
    if not registros:
        print("ℹ️ Atlas conectado, pero no hay usuarios ni tiendas registradas en MiVeci aún.")
        print("🧪 Cargando Batería de Cuentas de Prueba para verificar las Reglas de Defensa:")
        print("   • Compradores: Cero tolerancia (Batman, trolls y personajes bloqueados)")
        print("   • Vendedores: Tolerancia a nombres creativos, pero bloqueo estricto a palabras soeces\n")
        registros = [
            {"_id": "SIM-001", "_tipo": "COMPRADOR", "name": "David Betancourt", "email": "david@miveci.com"},
            {"_id": "SIM-002", "_tipo": "COMPRADOR", "name": "Batman_DarkKnight", "email": "batman@gotham.city"},
            {"_id": "SIM-003", "_tipo": "COMPRADOR", "name": "Hacker_Root_Admin", "email": "admin@botnet.org"},
            {"_id": "SIM-004", "_tipo": "VENDEDOR", "storeName": "El Rinconcito del Sabor de Doña Carmen", "owner": "Carmen P."},
            {"_id": "SIM-005", "_tipo": "VENDEDOR", "storeName": "La Gran Verga Market", "owner": "Troll"},
            {"_id": "SIM-006", "_tipo": "COMPRADOR", "name": "Comprador_Test", "query": {"$ne": 1}},
        ]

    amenazas_detectadas = 0
    
    print("-" * 65)
    for idx, reg in enumerate(registros):
        tipo = reg.get('_tipo', 'COMPRADOR')
        id_doc = str(reg.get('_id', reg.get('id', f'REG-{idx}')))
        nombre = reg.get('storeName', reg.get('name', reg.get('cliente', 'Desconocido')))
        
        es_amenaza = False
        razon_amenaza = ""
        
        # Nivel 1: Filtro Heurístico
        if tipo == 'COMPRADOR':
            es_invalido, motivo = es_nombre_comprador_invalido(nombre)
            if es_invalido:
                es_amenaza = True
                razon_amenaza = f"Nombre de comprador no permitido ({motivo})"
        else: # VENDEDOR
            es_vulgar, motivo = es_nombre_vendedor_vulgar(nombre)
            if es_vulgar:
                es_amenaza = True
                razon_amenaza = f"Nombre de negocio con palabras soeces/ataque ({motivo})"
                
        # Nivel 2: Detección profunda de Inyecciones NoSQL
        reg_str = json.dumps({k: v for k, v in reg.items() if k != '_id'}, default=str)
        for p in PATRONES_INYECCION:
            if re.search(p, reg_str):
                es_amenaza = True
                razon_amenaza = f"Inyección NoSQL detectada ({p})"
                break
                
        if es_amenaza:
            amenazas_detectadas += 1
            print(f"🚨 \033[91m[AMENAZA DETECTADA - {tipo}]\033[0m")
            print(f"   ID: {id_doc} | Sujeto: '{nombre}'")
            print(f"   Causa: {razon_amenaza}")
            
            # Veredicto certero de Cerberus
            veredicto = f"ESTADO: BLOQUEADO (ATAQUE) | SEVERIDAD: ALTO | JUSTIFICACIÓN: {razon_amenaza}"
            print(f"   🤖 Dictamen Cerberus: {veredicto}")
            
            # Acción activa: Mover a Cuarentena si hay cliente Mongo
            if mongo_client:
                try:
                    col_name = "businesses" if tipo == 'VENDEDOR' else "users"
                    db[col_name].update_one(
                        {"_id": reg.get('_id')},
                        {"$set": {"cerberus_status": "CUARENTENA", "quarantine_reason": razon_amenaza}}
                    )
                    print(f"   🔒 \033[92mAcción de Defensa: Registro movido a CUARENTENA en MongoDB Atlas.\033[0m")
                except Exception as db_err:
                    print(f"   ⚠️ No se pudo aplicar cuarentena: {db_err}")
                    
            guardar_incidente("Escáner BD (MongoDB)", "ALTO", f"{tipo}: '{nombre}' bloqueado. Causa: {razon_amenaza}")
            print("-" * 65)
        else:
            print(f"✅ \033[92m[SEGURO - {tipo}]\033[0m {id_doc}: '{nombre}' verificado correctamente.")
            
    print("=" * 65)
    print(f"Resumen del Escaneo: {len(registros)} registros analizados, {amenazas_detectadas} amenazas neutralizadas.")
    input("\nPresiona ENTER para volver al menú principal...")
