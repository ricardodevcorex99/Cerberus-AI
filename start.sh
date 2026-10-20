#!/usr/bin/env bash

# ========================================================
# Cerberus AI Security Suite - Lanzador de Servicios
# ========================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Liberar puertos si estuvieran ocupados
PID_5050=$(lsof -ti :5050)
[ -n "$PID_5050" ] && kill -9 $PID_5050 2>/dev/null

PID_5055=$(lsof -ti :5055)
[ -n "$PID_5055" ] && kill -9 $PID_5055 2>/dev/null

# Iniciar servidor SIEM Dashboard (Puerto 5050)
nohup python3 core/web_dashboard.py >/dev/null 2>&1 &
echo "[✓] Cerberus SIEM Dashboard iniciado en: http://localhost:5050"

# Iniciar Terminal Web (Puerto 5055)
nohup python3 core/web_terminal.py >/dev/null 2>&1 &
echo "[✓] Cerberus Terminal Web iniciada en:   http://localhost:5055"

echo ""
echo "Iniciando consola interactiva..."
python3 main.py
