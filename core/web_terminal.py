import os
import sys
import json
import threading
import io

# Asegurar que la raíz de Cerberus esté en el PATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import redirect_stdout, redirect_stderr
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from core.ai_engine import load_env_file

load_env_file()
PORT = int(os.getenv("WEB_TERMINAL_PORT", 5055))
TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates", "web_terminal.html")

def get_html_content():
    if os.path.exists(TEMPLATE_PATH):
        try:
            with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
                return f.read().encode("utf-8")
        except Exception:
            pass
    return b"<h1>Error cargando templates/web_terminal.html</h1>"

class TerminalHandler(BaseHTTPRequestHandler):
    def _send_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors()
        self.end_headers()

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            content = get_html_content()
            self.send_response(200)
            self._send_cors()
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/api/status':
            resp = json.dumps({
                "status": "online",
                "terminal": "active",
                "port": PORT,
                "model": os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
            }).encode('utf-8')
            self.send_response(200)
            self._send_cors()
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(resp)))
            self.end_headers()
            self.wfile.write(resp)
        else:
            self.send_response(404)
            self._send_cors()
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

            resp = json.dumps({"output": output}).encode('utf-8')
            self.send_response(200)
            self._send_cors()
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(resp)))
            self.end_headers()
            self.wfile.write(resp)
        else:
            self.send_response(404)
            self._send_cors()
            self.end_headers()

    def execute_command(self, cmd):
        buf = io.StringIO()
        try:
            with redirect_stdout(buf), redirect_stderr(buf):
                if cmd == '1':
                    print("--- INICIANDO AUDITORÍA SAST LOCAL ---")
                    from modules.modulo1_auditor import auditar_codigo
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
                    print("--- DIAGNÓSTICO DE FORMULARIOS Y ENTRADAS (FIREWALL MIVECI) ---")
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
                    payload = cmd[5:].strip()
                    from modules.modulo3_firewall import evaluar_payload_firewall
                    res = evaluar_payload_firewall(payload, "Web Terminal")
                    status_lbl = "BLOQUEADO" if res["bloqueado"] else "PERMITIDO"
                    print(f"Payload: '{payload}'")
                    print(f"Veredicto: {status_lbl} ({res['severidad']})")
                    print(f"Filtro: {res['filtro']}")
                    print(f"Detalle: {res['justificacion']}")

                elif cmd.lower() in ['help', 'ayuda', '?']:
                    print("=====================================================================")
                    print(" 🛡️  C E R B E R U S   C O M A N D O S   D I S P O N I B L E S  🛡️")
                    print("=====================================================================")
                    print("  1        : Auditar código fuente local MiVeci (SAST OWASP Top 10)")
                    print("  2        : Escanear MongoDB Atlas (Regla Vendedores vs Compradores)")
                    print("  3        : Firewall de Entradas y Formularios (Tiendas, Compradores y Búsqueda)")
                    print("  4        : Ver registro de incidentes SIEM central")
                    print("  test <x> : Evaluar payload libre en vivo con Cerberus")
                    print("  clear    : Limpiar la pantalla de la terminal")

                elif cmd.lower() in ['clear', '5']:
                    print("Pantalla limpiada.")

                else:
                    print(f"Comando '{cmd}' no reconocido.")
                    print("Comandos disponibles: 1 (SAST), 2 (MongoDB), 3 (Firewall Formularios), 4 (SIEM), test <frase>, help, clear")
        except Exception as e:
            print(f"Error durante ejecución: {e}")

        return buf.getvalue()

    def log_message(self, format, *args):
        pass  # Silenciar logs ruidosos en stdout

def start_terminal_server():
    server = ThreadingHTTPServer(('0.0.0.0', PORT), TerminalHandler)
    server.serve_forever()

def lanzar_terminal_background():
    t = threading.Thread(target=start_terminal_server, daemon=True)
    t.start()
    return t

if __name__ == '__main__':
    print(f"Iniciando Cerberus Terminal Web Emulator en http://localhost:{PORT}")
    start_terminal_server()
