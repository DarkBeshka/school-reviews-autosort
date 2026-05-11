import os
import logging
from config.settings import LOG_FILE

def setup_logging():
    """Настройка логирования: создание папки и файла логов."""
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def ensure_dirs(dirs):
    """Создать указанные директории, если их нет."""
    for d in dirs:
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)