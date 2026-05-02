import json
import os

SETTINGS_FILE = 'settings.json'

DEFAULT_SETTINGS = {
    "snake_color": [0, 255, 0],
    "grid_overlay": False,
    "sound": True
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return {"snake_color": (0, 255, 0), "grid_overlay": False, "sound": True}

    with open(SETTINGS_FILE, 'r') as f:
        try:
            data = json.load(f)
        except Exception:
            save_settings(DEFAULT_SETTINGS)
            return {"snake_color": (0, 255, 0), "grid_overlay": False, "sound": True}

    for key, val in DEFAULT_SETTINGS.items():
        if key not in data:
            data[key] = val

    data['snake_color'] = tuple(data['snake_color'])
    return data

def save_settings(settings):
    to_save = {}
    for key, val in settings.items():
        to_save[key] = list(val) if isinstance(val, tuple) else val
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(to_save, f, indent=4)

CS = 20
W, H = 30, 20
WIDTH, HEIGHT = W * CS, H * CS  # 600 x 400