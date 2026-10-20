import os
import sys
import json
import threading
import time

# Asegurar que la raíz de Cerberus esté en el PATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify
from core.ai_engine import load_env_file

load_env_file()
PORT = int(os.getenv("SIEM_PORT", 5050))

app = Flask(__name__, template_folder='../templates')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    inc_count = 0
    inc_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/incidentes.json')
    if os.path.exists(inc_file):
        try:
            with open(inc_file, 'r', encoding='utf-8') as f:
                inc_count = len(json.load(f))
        except Exception:
            pass
            
    return jsonify({
        "status": "online",
        "service": "Cerberus Security Hacker AI",
        "port": PORT,
        "total_incidents": inc_count,
        "model": os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    })

@app.route('/api/incidentes')
def api_incidentes():
    inc_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/incidentes.json')
    try:
        with open(inc_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return jsonify(data)
    except Exception:
        # Fallback a respaldo si no existe
        backup = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/incidentes_backup.json')
        if os.path.exists(backup):
            try:
                with open(backup, 'r', encoding='utf-8') as f:
                    return jsonify(json.load(f))
            except Exception:
                pass
        return jsonify([])

def start_flask():
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

def lanzar_servidor():
    print(f"\n🌐 \033[1;36mIniciando Servidor Web Cerberus SIEM Dashboard (Puerto {PORT})...\033[0m")
    t = threading.Thread(target=start_flask, daemon=True)
    t.start()
    time.sleep(1) 
    print(f"✅ \033[1;32mServidor corriendo en http://localhost:{PORT}\033[0m")
    print("\n" + "="*60)
    print("Dashboard Web activo. Puedes abrir en tu navegador:")
    print(f"👉 http://localhost:{PORT}")
    print("="*60 + "\n")
    input("🛑 Presiona ENTER aquí ÚNICAMENTE cuando quieras apagar el servidor...")

if __name__ == '__main__':
    start_flask()
