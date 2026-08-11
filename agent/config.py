import json
from pathlib import Path

# Kullanıcının ev dizinindeki konfigürasyon dosyası (~/.agentrc)
CONFIG_FILE = Path.home() / ".agentrc"

def load_config() -> dict:
    """
    ~/.agentrc dosyasını okur ve bir sözlük (dict) olarak döndürür.
    Dosya yoksa veya bozuksa boş sözlük döner.
    """
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_config(data: dict) -> None:
    """
    Verilen konfigürasyon sözlüğünü ~/.agentrc dosyasına yazar.
    """
    existing_config = load_config()
    existing_config.update(data)
    
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_config, f, indent=4, ensure_ascii=False)