import logging
import os
from pathlib import Path
from datetime import datetime


def setup_logger():
    """Настройка и конфигурация логера"""
    project_root = Path(__file__).parent

    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)

    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = logs_dir / f"app_{current_date}.log"

    logger = logging.getLogger("card_mask_logger")
    logger.setLevel(logging.INFO)

    logger.handlers.clear()

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)

    return logger


logger = setup_logger()
