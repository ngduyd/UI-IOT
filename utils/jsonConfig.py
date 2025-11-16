import json, os
CONFIG_PATH = 'config.json'

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"mode": "Wi-Fi", "ssid": "", "password": "", "mqtt": "", "isConfigured": False, "deviceID": ""}

def save_config(data: dict):
    existing_config = load_config()
    existing_config.update(data)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(existing_config, f, ensure_ascii=False, indent=4)

def is_empty(*fields):
    return any(not f.value.strip() for f in fields)