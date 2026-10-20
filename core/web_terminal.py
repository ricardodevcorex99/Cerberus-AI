import os
import sys
import json
import threading
import io

# Asegurar que la raíz de Cerberus esté en el PATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import redirect_stdout, redirect_stderr
from http.server import HTTPServer, BaseHTTPRequestHandler
from core.ai_engine import load_env_file

load_env_file()
PORT = int(os.getenv("WEB_TERMINAL_PORT", 5055))

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cerberus Terminal Web (Puerto 5055)</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220%22%20%22100%22%20%22100%22><text y=%22.9em%22 font-size=%2290%22>🛡️</text></svg>">
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: #0b0f19;
            color: #10b981;
            font-family: 'JetBrains Mono', monospace;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .term-header {
            background: #111827;
            border-bottom: 1px solid #1f2937;
            padding: 10px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .traffic-lights { display: flex; gap: 8px; }
        .dot { width: 12px; height: 12px; border-radius: 50%; }
        .red { background: #ef4444; }
        .yellow { background: #f59e0b; }
        .green { background: #10b981; }
        .term-title { color: #f3f4f6; font-size: 13px; font-weight: bold; }
        .term-links a {
            color: #38bdf8;
            font-size: 12px;
            text-decoration: none;
            margin-left: 12px;
            padding: 4px 8px;
            background: #1e293b;
            border-radius: 6px;
            border: 1px solid #334155;
        }
        .term-links a:hover { background: #334155; }
        #terminal-body {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-break: break-word;
            font-size: 13px;
            line-height: 1.5;
            color: #d1d5db;
        }
        .ansi-cyan { color: #06b6d4; font-weight: bold; }
        .ansi-yellow { color: #f59e0b; font-weight: bold; }
        .ansi-green { color: #10b981; font-weight: bold; }
        .ansi-red { color: #ef4444; font-weight: bold; }
        .ansi-purple { color: #a855f7; font-weight: bold; }
        .term-input-row {
            display: flex;
            align-items: center;
            padding: 12px 16px;
            background: #090d16;
            border-top: 1px solid #1f2937;
        }
        .prompt-label {
            color: #f59e0b;
            font-weight: bold;
            margin-right: 8px;
            white-space: nowrap;
        }
        #cmd-input {
            flex: 1;
            background: transparent;
            border: none;
            color: #f3f4f6;
            font-family: inherit;
            font-size: 14px;
            outline: none;
        }
        .quick-actions {
            display: flex;
            gap: 8px;
            padding: 8px 16px;
            background: #0d131f;
            border-top: 1px solid #1f2937;
            overflow-x: auto;
        }
        .btn-quick {
            background: #1e293b;
            color: #94a3b8;
            border: 1px solid #334155;
            padding: 4px 10px;
            border-radius: 6px;
            font-family: inherit;
            font-size: 11px;
            cursor: pointer;
            white-space: nowrap;
        }
        .btn-quick:hover { background: #334155; color: #f8fafc; }
    </style>
</head>
<body>
    <div class="term-header">
        <div class="traffic-lights">
            <span class="dot red"></span>
            <span class="dot yellow"></span>
            <span class="dot green"></span>
        </div>
        <div class="term-title">🛡️ CERBERUS SECURITY HACKER AI - TERMINAL EMULATOR (PORT 5055)</div>
        <div class="term-links">
            <a href="http://localhost:5050" target="_blank">📊 SIEM Dashboard (5050)</a>
            <a href="http://localhost:8888" target="_blank">⚡ MiVeci Ops (8888)</a>
        </div>
    </div>

    <div id="terminal-body">
<span class="ansi-cyan">=====================================================================</span>
<span class="ansi-yellow">      🛡️   C E R B E R U S   S E C U R I T Y   H A C K E R   A I   🛡️</span>
<span class="ansi-cyan">=====================================================================</span>
<span class="ansi-green">[+] Sistema de Defensa Cerberus Iniciado...</span>
<span class="ansi-green">[+] Conexión con MongoDB Atlas y Gemini 3.8 Flash: ACTIVA</span>
<span class="ansi-green">[+] Modo Terminal Web Activo (Termux Compatible)</span>

MÓDULOS DISPONIBLES:
  [ 1 ] 🔍 Auditar código fuente (SAST OWASP Top 10)
  [ 2 ] 💾 Escanear Base de Datos MongoDB Atlas (Regla Vendedores vs Compradores)
  [ 3 ] 🧱 Probar Firewall de Inyección de Prompts / Reseñas (Defensa L7)
  [ 4 ] 📊 Ver Registro de Incidentes SIEM (Historial y Severidad)
  [ 5 ] 🧹 Limpiar pantalla
  [ help ] Ver comandos disponibles

Escribe el número del módulo que deseas ejecutar:
    </div>

    <div class="quick-actions">
        <button class="btn-quick" onclick="sendCmd('1')">[1] Auditar Código</button>
        <button class="btn-quick" onclick="sendCmd('2')">[2] Escanear MongoDB</button>
        <button class="btn-quick" onclick="sendCmd('3')">[3] Probar Firewall</button>
        <button class="btn-quick" onclick="sendCmd('4')">[4] Registro SIEM</button>
        <button class="btn-quick" onclick="sendCmd('clear')">Limpiar Pantalla</button>
    </div>

    <div class="term-input-row">
        <span class="prompt-label">root@cerberus-sec:~#</span>
        <input type="text" id="cmd-input" autofocus autocomplete="off" placeholder="Escribe 1, 2, 3, 4 o cualquier comando...">
    </div>

    <script>
        const terminalBody = document.getElementById('terminal-body');
        const cmdInput = document.getElementById('cmd-input');

        function scrollToBottom() {
            terminalBody.scrollTop = terminalBody.scrollHeight;
        }

        async function sendCmd(cmd) {
            cmd = (cmd || cmdInput.value).trim();
            if (!cmd) return;
            cmdInput.value = '';

            terminalBody.innerHTML += `\\n<span class="ansi-yellow">root@cerberus-sec:~#</span> \${escapeHtml(cmd)}\\n`;
            scrollToBottom();

            if (cmd.toLowerCase() === 'clear' || cmd === '5') {
                terminalBody.innerHTML = '';
                return;
            }

            terminalBody.innerHTML += `<span class="ansi-cyan">[*] Ejecutando módulo en segundo plano...</span>\\n`;
            scrollToBottom();

            try {
                const res = await fetch('/api/run', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ command: cmd })
                });
                const data = await res.json();
                terminalBody.innerHTML += formatOutput(data.output || 'Sin respuesta.') + '\\n';
            } catch (err) {
                terminalBody.innerHTML += `<span class="ansi-red">Error al comunicar con Cerberus: \${err.message}</span>\\n`;
            }
            scrollToBottom();
        }

        cmdInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                sendCmd();
            }
        });

        function formatOutput(text) {
            return text
                .replace(/\[\+\]/g, '<span class="ansi-green">[+]</span>')
                .replace(/\[\!\]/g, '<span class="ansi-yellow">[!]</span>')
                .replace(/\[\*\]/g, '<span class="ansi-cyan">[*]</span>')
                .replace(/\[AMENAZA[^\]]*\]/g, '<span class="ansi-red">$&</span>')
                .replace(/\[SEGURO[^\]]*\]/g, '<span class="ansi-green">$&</span>')
                .replace(/CRÍTICO/g, '<span class="ansi-red">CRÍTICO</span>')
                .replace(/ALTO/g, '<span class="ansi-yellow">ALTO</span>');
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }
    </script>
</body>
</html>
"""

class TerminalHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "online", "terminal": "active", "port": PORT}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/run':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            try:
                data = json.loads(body)
                cmd = str(data.get('command', '')).strip()
            except Exception:
                cmd = ''

            output = self.execute_command(cmd)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"output": output}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def execute_command(self, cmd):
        buf = io.StringIO()
        try:
            with redirect_stdout(buf), redirect_stderr(buf):
                if cmd == '1':
                    print("--- INICIANDO AUDITORÍA SAST LOCAL ---")
                    from modules.modulo1_auditor import auditar_codigo
                    # Simular opción 1 automática para web
                    import builtins
                    orig_input = builtins.input
                    builtins.input = lambda _: "1"
                    try:
                        auditar_codigo()
                    finally:
                        builtins.input = orig_input
                elif cmd == '2':
                    print("--- ESCANEANDO MONGODB ATLAS (VENDEDORES VS COMPRADORES) ---")
                    from modules.modulo2_spam import escanear_reservas
                    import builtins
                    orig_input = builtins.input
                    builtins.input = lambda _: ""
                    try:
                        escanear_reservas()
                    finally:
                        builtins.input = orig_input
                elif cmd == '3':
                    print("--- BATERÍA DE PRUEBAS FIREWALL SEMÁNTICO L7 ---")
                    from modules.modulo3_firewall import probar_firewall
                    import builtins
                    orig_input = builtins.input
                    builtins.input = lambda _: "2"
                    try:
                        probar_firewall()
                    finally:
                        builtins.input = orig_input
                elif cmd == '4':
                    print("--- REGISTRO CENTRAL DE INCIDENTES SIEM ---")
                    from core.dashboard import ver_dashboard
                    import builtins
                    orig_input = builtins.input
                    builtins.input = lambda _: ""
                    try:
                        ver_dashboard()
                    finally:
                        builtins.input = orig_input
                elif cmd.startswith("test "):
                    # Probar un payload libre contra el firewall
                    payload = cmd[5:].strip()
                    from modules.modulo3_firewall import evaluar_payload_firewall
                    res = evaluar_payload_firewall(payload, "Web Terminal")
                    status_lbl = "BLOQUEADO" if res["bloqueado"] else "PERMITIDO"
                    print(f"Payload: '{payload}'")
                    print(f"Veredicto: {status_lbl} ({res['severidad']})")
                    print(f"Filtro: {res['filtro']}")
                    print(f"Detalle: {res['justificacion']}")
                else:
                    print(f"Comando '{cmd}' no reconocido.")
                    print("Comandos válidos: 1 (Auditor), 2 (Escanear MongoDB), 3 (Firewall), 4 (SIEM), test <frase>, clear")
        except Exception as e:
            print(f"Error durante ejecución: {e}")

        return buf.getvalue()

    def log_message(self, format, *args):
        pass # Silenciar logs en consola

def start_terminal_server():
    server = HTTPServer(('0.0.0.0', PORT), TerminalHandler)
    server.serve_forever()

def lanzar_terminal_background():
    t = threading.Thread(target=start_terminal_server, daemon=True)
    t.start()
    return t

if __name__ == '__main__':
    print(f"Iniciando Cerberus Terminal Web en http://localhost:{PORT}")
    start_terminal_server()
