import os
import sys
import time

from modules.modulo1_auditor import auditar_codigo
from modules.modulo2_spam import escanear_reservas
from modules.modulo3_firewall import probar_firewall
from core.dashboard import ver_dashboard

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("\033[1;36m" + "=====================================================================" + "\033[0m")
    print("\033[1;33m" + "      🛡️   C E R B E R U S   S E C U R I T Y   H A C K E R   A I   🛡️" + "\033[0m")
    print("\033[1;36m" + "=====================================================================" + "\033[0m")
    print("\033[1;32m[+] Sistema de Defensa Cerberus Iniciado...\033[0m")
    print("\033[1;32m[+] Enlace MongoDB Atlas & Google Gemini: ESTABLECIDO\033[0m")
    print("\033[1;32m[+] Plataformas: macOS / Linux / Termux Android\033[0m\n")

def main():
    while True:
        print_header()
        print("\033[1;37mMÓDULOS DE OPERACIÓN:\033[0m\n")
        print("  \033[1;34m[ 1 ]\033[0m 🔍 Auditar código fuente (MiVeci App / GitHub) \033[90m- SAST OWASP Top 10\033[0m")
        print("  \033[1;34m[ 2 ]\033[0m 💾 Escanear MongoDB Atlas (Vendedores vs Compradores) \033[90m- Defensa Activa\033[0m")
        print("  \033[1;34m[ 3 ]\033[0m 🧱 Probar Firewall de Entradas y Formularios \033[90m- Nombres, Búsquedas y APIs\033[0m")
        print("  \033[1;34m[ 4 ]\033[0m 📊 Ver Registro SIEM Central en Terminal \033[90m- Incidentes & Severidad\033[0m")
        print("  \033[1;34m[ 5 ]\033[0m 🌐 Lanzar Servidor Web SIEM Dashboard \033[90m(Puerto 5050 - Gráficos)\033[0m")
        print("  \033[1;34m[ 6 ]\033[0m 🖥️  Lanzar Terminal Web Embebida \033[90m(Puerto 5055 - Terminal Web Emulator)\033[0m")
        print("  \033[1;31m[ 7 ]\033[0m 🚪 Salir de la Suite\n")
        print("\033[1;36m" + "---------------------------------------------------------------------" + "\033[0m")
        
        opcion = input("\033[1;33mroot@cerberus-sec:~# \033[0m").strip()
        
        if opcion == '1':
            auditar_codigo()
        elif opcion == '2':
            escanear_reservas()
        elif opcion == '3':
            probar_firewall()
        elif opcion == '4':
            ver_dashboard()
        elif opcion == '5':
            from core.web_dashboard import lanzar_servidor
            lanzar_servidor()
        elif opcion == '6':
            import subprocess
            print("\n🌐 Iniciando Cerberus Terminal Web en http://localhost:5055 ...")
            subprocess.Popen([sys.executable, "core/web_terminal.py"])
            time.sleep(1)
            print("✅ Terminal Web activa. Abriendo en navegador...")
            os.system("open http://localhost:5055 2>/dev/null")
            input("\nPresiona ENTER para volver al menú...")
        elif opcion == '7':
            print("\n\033[1;31m[!] Saliendo de Cerberus Security Hacker AI...\033[0m\n")
            sys.exit(0)
        else:
            print("\n\033[1;31m❌ Opción no válida. Intenta de nuevo.\033[0m")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[1;31m[!] Abortando ejecución y saliendo de la Suite...\033[0m\n")
        sys.exit(0)
