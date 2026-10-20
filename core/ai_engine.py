import os
import time
import json
import urllib.request
import urllib.error

def load_env_file():
    """Carga variables desde el archivo .env sin dependencias externas."""
    # Buscar en la carpeta raíz de Cerberus
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, '.env')
    
    # También buscar en el proyecto padre si existe
    parent_env = os.path.join(os.path.dirname(base_dir), '.env')
    
    target_path = env_path if os.path.exists(env_path) else (parent_env if os.path.exists(parent_env) else None)
    
    if target_path and os.path.exists(target_path):
        try:
            with open(target_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        k = k.strip()
                        v = v.strip().strip('"\'')
                        if k and k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass

def analizar_con_ia(prompt, datos):
    """
    Envía un prompt y datos a la API de Google Gemini con reintentos y enfriamiento automático.
    Funciona tanto en Termux, macOS, Linux y Windows sin necesidad de librerías externas.
    """
    try:
        load_env_file()
        api_key = os.getenv("STITCH_API_KEY")
        if not api_key:
            return "Error: No se encontró STITCH_API_KEY en el archivo .env"
            
        model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        mensaje_completo = f"{prompt}\n\nDatos a analizar:\n{datos}"
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = json.dumps({
            "contents": [{
                "parts": [{"text": mensaje_completo}]
            }]
        }).encode('utf-8')
        
        headers = {'Content-Type': 'application/json'}
        
        # Bucle de reintentos para manejar picos de saturación (Error 429 o 503)
        for intento in range(3):
            req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
            try:
                with urllib.request.urlopen(req, timeout=25) as response:
                    res_json = json.loads(response.read().decode('utf-8'))
                    try:
                        return res_json['candidates'][0]['content']['parts'][0]['text'].strip()
                    except (KeyError, IndexError):
                        return str(res_json)
            except urllib.error.HTTPError as e:
                code = e.code
                error_body = e.read().decode('utf-8', errors='ignore')
                
                if code == 429:
                    if intento < 1:
                        print("⚠️ [Cerberus IA] Límite de cuota alcanzado. Reintentando...")
                        time.sleep(2)
                        continue
                    return "Error API (Código 429): Límite de cuota alcanzado."
                elif code in [500, 502, 503]:
                    if intento < 1:
                        print(f"⚠️ [Cerberus IA] Servidor temporalmente ocupado (Código {code}). Reintentando...")
                        time.sleep(1)
                        continue
                    return f"Error API (Código {code}): Servidores temporalmente ocupados."
                else:
                    return f"Error API (Código {code}): {error_body}"
            except Exception as conn_err:
                if intento < 2:
                    time.sleep(2)
                    continue
                return f"Error de conexión con Cerberus IA: {conn_err}"
                
    except Exception as e:
        return f"Error general en Cerberus IA: {e}"
