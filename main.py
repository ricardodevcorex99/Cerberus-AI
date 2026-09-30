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
    print("\033[1;32m[+] Sistema de Defensa Iniciado...\033[0m")
    print("\033[1;32m[+] Enlace Termux/Mac Neo: ESTABLECIDO\033[0m\n")

def main():
    while True:
        print_header()
        print("\033[1;37mMÓDULOS DE OPERACIÓN:\033[0m\n")
        print("  \033[1;34m[ 1 ]\033[0m 🔍 Auditar código fuente (Vercel/GitHub) \033[90m- Buscador de Vulnerabilidades\033[0m")
        print("  \033[1;34m[ 2 ]\033[0m 💾 Escanear Base de Datos (Firebase)   \033[90m- Detector de Spam/Fraude\033[0m")
        print("  \033[1;34m[ 3 ]\033[0m 🧱 Probar Firewall del Chatbot         \033[90m- Protección en tiempo real\033[0m")
        print("  \033[1;34m[ 4 ]\033[0m 📊 Ver Registro SIEM Central           \033[90m- Dashboard de Vulnerabilidades\033[0m")
        print("  \033[1;34m[ 5 ]\033[0m 🌐 Lanzar Servidor Web (Dashboard)     \033[90m- Gráficos en Tiempo Real\033[0m")
        print("  \033[1;31m[ 6 ]\033[0m 🚪 Salir de la Terminal\n")
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
