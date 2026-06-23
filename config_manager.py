import json
import os
from pathlib import Path

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'data', 'config.json')
WELCOME_DIR = os.path.join(os.path.dirname(__file__), 'data')
WELCOME_PATH = os.path.join(WELCOME_DIR, 'welcome_custom.png')

DEFAULT_CONFIG = {
    'channel_username': '',
    'admin_username': '',
    'welcome_image_path': '',
}


def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
    except Exception as e:
        print(f"Config load error: {e}")
    return dict(DEFAULT_CONFIG)


def save_config(config):
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Config save error: {e}")


def set_channel(username):
    cfg = load_config()
    cfg['channel_username'] = username.strip()
    save_config(cfg)


def set_admin(username):
    cfg = load_config()
    cfg['admin_username'] = username.strip()
    save_config(cfg)


def set_welcome_image(file_path):
    cfg = load_config()
    cfg['welcome_image_path'] = file_path
    save_config(cfg)


def get_channel():
    cfg = load_config()
    return cfg.get('channel_username') or ''


def get_admin():
    cfg = load_config()
    return cfg.get('admin_username') or ''


def get_welcome_image():
    cfg = load_config()
    path = cfg.get('welcome_image_path') or ''
    if path and os.path.exists(path):
        return path
    default = WELCOME_PATH
    if os.path.exists(default):
        return default
    return ''
