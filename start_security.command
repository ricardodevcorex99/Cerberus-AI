#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Iniciar servicios de fondo de Cerberus (Dashboard 5050 y Terminal Web 5055)
python3 core/web_dashboard.py >/dev/null 2>&1 &
python3 core/web_terminal.py >/dev/null 2>&1 &

# Ejecutar consola interactiva en la terminal nativa
python3 main.py
