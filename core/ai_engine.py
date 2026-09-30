import os
try:
    from dotenv import load_dotenv
    import requests
except ImportError:
    pass

def analizar_con_ia(prompt, datos):
    try:
        load_dotenv()
        api_key = os.getenv("STITCH_API_KEY")
        if not api_key:
            return "Error: No se encontró STITCH_API_KEY en el archivo .env"
            
        mensaje_completo = f"{prompt}\n\nDatos a analizar: {datos}"
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts":[{"text": mensaje_completo}]}]}
        # Bucle de reintentos para manejar picos de saturación de la API (Error 503)
        import time
        for intento in range(3):
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            elif response.status_code == 429:
                if intento < 2:
                    print("⚠️ Límite de cuota gratuita alcanzado. Esperando 30 segundos de enfriamiento...")
                    time.sleep(30)
                    continue
                return f"Error API (Código 429): Límite de peticiones de tu plan gratuito excedido. Intenta en 1 minuto."
            elif response.status_code in [500, 503]:
                if intento < 2:
                    time.sleep(4) # Esperar 4 segundos antes de reintentar
                    continue
                return f"Error API (Código {response.status_code}): Los servidores de IA están temporalmente saturados. Por favor, intenta de nuevo."
            else:
                return f"Error API (Código {response.status_code}): {response.text}"
            
    except Exception as e:
        return f"Error de conexión: {e}"
