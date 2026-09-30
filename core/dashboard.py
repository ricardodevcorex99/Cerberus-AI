import os
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
                pass
    
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

def ver_dashboard():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("========================================")
    print("   🛡️  C E R B E R U S   S E C U R I T Y   H A C K E R   A I  🛡️")
    print("========================================")
    print("[Módulo 4] Registro Central de Vulnerabilidades (Dashboard SIEM)")
    
    if not os.path.exists(DATA_FILE):
        print("No hay incidentes registrados en el sistema todavía.")
        input("\nPresiona ENTER para volver al menú...")
        return
        
    with open(DATA_FILE, "r") as f:
        try:
            incidentes = json.load(f)
        except:
            incidentes = []
            
    if not incidentes:
        print("El registro está vacío.")
    else:
        print(f"{'ID':<10} | {'FECHA':<20} | {'MÓDULO':<25} | {'SEVERIDAD':<12}")
        print("-" * 75)
        for inc in incidentes:
            if inc['severidad'] in ['CRÍTICA', 'CRÍTICO']:
                color = "\033[91m" # Rojo
            elif inc['severidad'] in ['ADVERTENCIA', 'ALTO', 'ALTA']:
                color = "\033[93m" # Amarillo
            elif inc['severidad'] == 'MEDIO':
                color = "\033[95m" # Morado
            elif inc['severidad'] == 'BAJO':
                color = "\033[96m" # Cyan
            elif inc['severidad'] == 'NULO':
                color = "\033[94m" # Azul
            elif inc['severidad'] == 'EXCELENTE':
                color = "\033[92m" # Verde
            else:
                color = "\033[0m"
                
            print(f"{inc['id']:<10} | {inc['fecha']:<20} | {inc['modulo']:<25} | {color}{inc['severidad']}\033[0m")
            
        print("-" * 75)
        seleccion = input("\nEscribe el ID del incidente para ver detalles (ej. INC-001) o presiona ENTER para salir: ").strip().upper()
        
        if seleccion:
            encontrado = next((i for i in incidentes if i['id'] == seleccion), None)
            if encontrado:
                print("\n" + "="*60)
                print(f"📄 REPORTE DETALLADO: {encontrado['id']} ({encontrado['fecha']})")
                print(f"Módulo Origen: {encontrado['modulo']}")
                print("="*60)
                print(f"\033[96m{encontrado['detalle']}\033[0m")
                print("="*60)
            else:
                print("❌ ID no encontrado en la base de datos.")
                
    input("\nPresiona ENTER para volver al menú...")
