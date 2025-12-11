import os
import sys
from kivy.lang import Builder

def get_resource_path(relative_path):
    """Получает правильный путь для ресурсов в exe и в разработке"""
    try:
        # PyInstaller создает временную папку в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # В режиме разработки используем корневую директорию проекта
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.dirname(script_dir)  # Поднимаемся на уровень выше scripts
        base_path = os.path.dirname(base_path)
    full_path = os.path.join(base_path, relative_path)
    return full_path

def load_kv_file(kv_filename):
    """Загружает KV файл с правильным путем"""
    kv_path = get_resource_path(kv_filename)
    
    if not os.path.exists(kv_path):
        # Пробуем найти файл относительно директории скрипта
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_script_dir)
        alt_path = os.path.join(project_root, kv_filename)
        
        if os.path.exists(alt_path):
            kv_path = alt_path
        else:
            raise FileNotFoundError(f"KV file not found: {kv_path} or {alt_path}")
    
    Builder.load_file(kv_path)
    print(f"KV file loaded: {kv_path}")