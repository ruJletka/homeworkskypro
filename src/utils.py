import json
import logging
import os
from pathlib import Path


def setup_logger():
    current_file_path = Path(__file__).resolve()
    project_root = current_file_path.parent.parent

    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / f"app_{__name__}.log"

    logger = logging.getLogger(__name__)
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


def load_transaction_data() -> list[dict[str, any]]:
    """Функция загружает данные о финансовых операциях из файла operations.json в директории /data."""
    try:
        logger.info("Начало загрузки данных о транзакциях")

        file_path = os.path.join('data', 'operations.json')
        logger.debug(f"Путь к файлу: {file_path}")

        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        if os.path.getsize(file_path) == 0:
            logger.warning(f"Файл пуст: {file_path}")
            return []

        logger.info("Чтение файла с данными транзакций")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            logger.warning("Данные в файле не являются списком")
            return []

        logger.info(f"Успешно загружено {len(data)} транзакций")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON: {str(e)}")
        return []

    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {str(e)}")
        return []

    except PermissionError as e:
        logger.error(f"Ошибка доступа к файлу: {str(e)}")
        return []

    except Exception as e:
        logger.exception(f"Непредвиденная ошибка при загрузке данных: {str(e)}")
        return []
