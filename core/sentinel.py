import os
import time
import json
import re
import threading
from core.ai_engine import load_env_file
from core.dashboard import guardar_incidente
from modules.modulo2_spam import (
    obtener_conexiones_mongo,
    es_nombre_comprador_invalido,
    es_nombre_vendedor_vulgar,
    PATRONES_INYECCION
)

_sentinel_thread = None
_inspected_ids = set()
_running = False

def start_sentinel(interval_sec=8):
    """
    Inicia el centinela de Cerberus en segundo plano.
    Monitorea de forma continua MongoDB Atlas (businesses y users de MiVeci).
    """
    global _sentinel_thread, _running
    if _running:
        return
    _running = True
    _sentinel_thread = threading.Thread(target=_sentinel_loop, args=(interval_sec,), daemon=True)
    _sentinel_thread.start()

def _sentinel_loop(interval):
    global _running
    try:
        from pymongo import MongoClient
    except ImportError:
        return

    uri, db_name = obtener_conexiones_mongo()
    if not uri:
        return

    client = None
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        db = client[db_name]
    except Exception:
        return

    while _running:
        try:
            # 1. Monitoreo continuo de Negocios en Atlas
            for b in db.businesses.find().limit(50):
                doc_id = str(b.get('_id', b.get('id', '')))
                if doc_id and doc_id not in _inspected_ids:
                    _inspected_ids.add(doc_id)
                    store_name = b.get('storeName', b.get('name', ''))
                    
                    # Chequeo léxico
                    es_vulgar, motivo = es_nombre_vendedor_vulgar(store_name)
                    if es_vulgar:
                        guardar_incidente(
                            "Sentinel (Tiendas Atlas)",
                            "ALTO",
                            f"Negocio con contenido no permitido detectado en MongoDB Atlas: '{store_name}' (ID: {doc_id})"
                        )

                    # Chequeo NoSQL Injection
                    b_str = json.dumps({k: v for k, v in b.items() if k != '_id'}, default=str)
                    for p in PATRONES_INYECCION:
                        if re.search(p, b_str):
                            guardar_incidente(
                                "Sentinel (Inyección Atlas)",
                                "CRÍTICO",
                                f"Inyección NoSQL detectada en documento de negocio: '{store_name}' (ID: {doc_id})"
                            )
                            break

            # 2. Monitoreo continuo de Usuarios en Atlas
            for u in db.users.find().limit(50):
                u_id = str(u.get('_id', u.get('id', '')))
                if u_id and u_id not in _inspected_ids:
                    _inspected_ids.add(u_id)
                    role = u.get('role', 'buyer')
                    name = u.get('name', '')
                    
                    if role == 'buyer':
                        invalido, motivo = es_nombre_comprador_invalido(name)
                        if invalido:
                            guardar_incidente(
                                "Sentinel (Comprador Atlas)",
                                "MEDIO",
                                f"Comprador no permitido detectado en MongoDB Atlas: '{name}' ({motivo})"
                            )
                    else:
                        es_vulgar, motivo = es_nombre_vendedor_vulgar(name)
                        if es_vulgar:
                            guardar_incidente(
                                "Sentinel (Vendedor Atlas)",
                                "ALTO",
                                f"Vendedor con contenido no permitido detectado en MongoDB Atlas: '{name}' ({motivo})"
                            )

        except Exception:
            pass

        time.sleep(interval)
