import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "calendar.json"

DEFAULT_CONFIG = {
    "settings": {
        "check_interval_seconds": 5,
        "font_size": 72,
        "font_color": "#00d9ff",
        "bg_color": "#0a0a0f",
        "subtitle_font_size": 28,
    },
    "events": [],
}


def load_config():
    """Load config from JSON file."""
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    """Save config to JSON file."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def get_config_path():
    """Return the config file path."""
    return CONFIG_FILE
