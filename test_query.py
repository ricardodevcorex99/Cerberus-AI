import urllib.request
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("FIREBASE_API_KEY")

auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
payload = json.dumps({"email": "bot_python@barbershop.com", "password": "bot123456", "returnSecureToken": True}).encode('utf-8')
req = urllib.request.Request(auth_url, data=payload, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as response:
    token = json.loads(response.read().decode()).get('idToken')

url = "https://firestore.googleapis.com/v1/projects/the-barber-shop-c623b/databases/(default)/documents:runQuery"
payload = json.dumps({
  "structuredQuery": {
    "from": [{"collectionId": "firewall_logs"}],
    "where": {
      "fieldFilter": {
        "field": {"fieldPath": "estado"},
        "op": "EQUAL",
        "value": {"stringValue": "PENDIENTE"}
      }
    }
  }
}).encode('utf-8')
req = urllib.request.Request(url, data=payload, method="POST", headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req) as response:
    print(response.read().decode())
