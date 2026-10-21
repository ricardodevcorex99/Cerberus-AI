import os
import sys
import json
import datetime

DATA_FILE = "data/incidentes.json"

def guardar_incidente(modulo, severidad, detalle):
    if not os.path.exists("data"):
        os.makedirs("data")
        
    incidentes = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                incidentes = json.load(f)
            except:
                incidentes = []
    
    nuevo_id = f"INC-{len(incidentes) + 1:03d}"
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    incidente = {
        "id": nuevo_id,
        "fecha": fecha,
        "modulo": modulo,
        "severidad": severidad,
        "detalle": detalle
    }
    incidentes.append(incidente)
    
    with open(DATA_FILE, "w") as f:
        json.dump(incidentes, f, indent=4)
    
    return nuevo_id

def ver_dashboard(inc_id=None):
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        os.system('cls' if os.name == 'nt' else 'clear')

    incidentes = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                incidentes = json.load(f)
            except:
                incidentes = []

    # Si se pide el detalle de un incidente específico
    if inc_id:
        target = str(inc_id).strip().upper()
        if not target.startswith("INC-") and target.isdigit():
            target = f"INC-{int(target):03d}"
            
        encontrado = next((i for i in incidentes if i['id'].upper() == target), None)
        if encontrado:
            print("=====================================================================")
            print("       🛡️   C E R B E R U S   S I E M   D E T A I L   🛡️")
            print("=====================================================================")
            print(f"📄 REPORTE DETALLADO DE INCIDENTE: \033[1;36m{encontrado['id']}\033[0m")
            print(f"⏰ Fecha y Hora  : {encontrado['fecha']}")
            print(f"🛡️  Módulo Origen : {encontrado['modulo']}")
            
            sev = str(encontrado.get('severidad', 'MEDIO')).upper()
            color = "\033[91m" if "CRÍT" in sev else ("\033[93m" if "ALT" in sev else "\033[95m")
            print(f"🚨 Severidad     : {color}{encontrado['severidad']}\033[0m")
            print("-" * 65)
            print("📝 DETALLE FORENSE DEL INCIDENTE:")
            print(f"\033[96m{encontrado['detalle']}\033[0m")
            print("=" * 65)
        else:
            print(f"❌ Incidente '{inc_id}' no encontrado en la base de datos de Cerberus.")
            print("💡 Usa el comando '4' para ver la lista completa de incidentes disponibles.")
        return

    # Si se pide la lista completa de incidentes
    print("=====================================================================")
    print("   🛡️  C E R B E R U S   S E C U R I T Y   H A C K E R   A I  🛡️")
    print("=====================================================================")
    print("[Módulo 4] Registro Central de Vulnerabilidades (Dashboard SIEM)\n")

    if not incidentes:
        print("ℹ️ El registro SIEM se encuentra limpio (0 incidentes registrados).")
        print("🛡️ El centinela de Cerberus se encuentra vigilante en tiempo real.")
        print("=" * 65)
        return

    print(f"{'ID':<10} | {'FECHA':<20} | {'MÓDULO':<25} | {'SEVERIDAD':<12}")
    print("-" * 75)
    for inc in incidentes:
        sev = str(inc.get('severidad', 'MEDIO')).upper()
        if 'CRÍT' in sev:
            color = "\033[91m" # Rojo
        elif 'ALT' in sev:
            color = "\033[93m" # Amarillo
        elif 'MED' in sev:
            color = "\033[95m" # Morado
        elif 'BAJ' in sev:
            color = "\033[96m" # Cyan
        elif 'EXCEL' in sev or 'SEG' in sev:
            color = "\033[92m" # Verde
        else:
            color = "\033[0m"

        print(f"{inc['id']:<10} | {inc['fecha']:<20} | {inc['modulo']:<25} | {color}{inc['severidad']}\033[0m")

    print("-" * 75)
    print("💡 Para inspeccionar el detalle forense de un incidente:")
    print("   • Escribe su código directamente (ej. INC-041) o haz clic sobre su enlace.")
    print("=" * 75)

    if hasattr(sys.stdin, 'isatty') and sys.stdin.isatty():
        seleccion = input("\nEscribe el ID del incidente para ver detalles (o ENTER para volver): ").strip().upper()
        if seleccion:
            ver_dashboard(inc_id=seleccion)
            input("\nPresiona ENTER para volver al menú...")
