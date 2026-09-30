import os
import json
from flask import Flask, render_template, jsonify
import threading
import time

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/incidentes')
def api_incidentes():
    try:
        with open('data/incidentes.json', 'r') as f:
            data = json.load(f)
            return jsonify(data)
    except Exception:
        return jsonify([])

def start_flask():
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=5050, debug=False, use_reloader=False)

def lanzar_servidor():
    print("\n🌐 \033[1;36mIniciando Servidor Web Cerberus SIEM Dashboard...\033[0m")
    threading.Thread(target=start_flask, daemon=True).start()
    time.sleep(1) 
    print("✅ \033[1;32mServidor corriendo exitosamente.\033[0m")
    print("\n" + "="*60)
    print("⚠️ ATENCIÓN (USUARIOS DE TERMUX/MÓVIL) ⚠️")
    print("Termux no puede mostrar gráficos. Para ver el Dashboard:")
    print("1. NO presiones Enter todavía.")
    print("2. Abre tu navegador web (Google Chrome o Safari).")
    print("3. Escribe esta dirección en el buscador: http://127.0.0.1:5050")
    print("="*60 + "\n")
    
    input("🛑 Presiona ENTER aquí ÚNICAMENTE cuando quieras apagar el servidor...")

