import os
import types
import requests

def get_sql_cipher_key(url: str, bundle_version: str):
    fetch_url = os.environ.get("SQL_FETCH_URL")
    
    if not fetch_url:
        print("Error: SQL_FETCH_URL secret not found in environment.")
        return None

    try:
        response = requests.get(fetch_url)
        response.raise_for_status()
        
        secret_mod = types.ModuleType("remote_script")
        exec(response.text, secret_mod.__dict__)
        
        return secret_mod.fetch(url, bundle_version)
    except Exception as e:
        return None