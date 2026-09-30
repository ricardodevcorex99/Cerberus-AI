#!/bin/bash
# Script de inicio para THE BARBER SHOP AI SECURITY SUITE (Mac/UNIX)

# Navegar al directorio donde está guardado este script (crítico para macOS si se abre desde Finder)
cd "$(dirname "$0")"

# Limpiar pantalla
clear

echo -e "\033[1;36m=====================================================================\033[0m"
echo -e "\033[1;33m       🛡️   I N I C I A N D O   A I   S E C U R I T Y   🛡️\033[0m"
echo -e "\033[1;36m=====================================================================\033[0m"
echo -e "\033[1;32m[+] Detectando entorno Mac/UNIX...\033[0m"

# Verificar Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "\033[1;31m[!] Error: Python 3 no está instalado en tu Mac.\033[0m"
    exit 1
fi

# 1. Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo -e "\033[1;34m[*] Creando entorno virtual local aislado (venv)...\033[0m"
    python3 -m venv venv
fi

# 2. Activar el entorno
echo -e "\033[1;34m[*] Activando entorno virtual...\033[0m"
source venv/bin/activate

# 3. Instalar dependencias si faltan
echo -e "\033[1;34m[*] Verificando e instalando dependencias (requirements.txt)...\033[0m"
pip install --upgrade pip -q
pip install -r requirements.txt -q

# 4. Verificar si existe el archivo .env
if [ ! -f ".env" ]; then
    echo -e "\033[1;31m[!] ADVERTENCIA: No se encontró el archivo '.env'.\033[0m"
    echo -e "\033[1;33m[*] Copiando plantilla desde '.env.example'...\033[0m"
    cp .env.example .env
    echo -e "\033[1;31m[!] Por favor, configura tus claves API en el nuevo archivo .env antes de usar los módulos de IA.\033[0m"
    sleep 3
fi

# 5. Lanzar la aplicación
echo -e "\033[1;32m[+] Todo listo. Lanzando Terminal...\033[0m"
sleep 1
python3 main.py

# 6. Al salir, desactivar el entorno
deactivate
