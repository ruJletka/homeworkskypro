import json
import os


def load_transaction_data(file_path: str) -> list[dict[str, any]]:
    """Функция загружает данные о финансовых операциях из JSON-файла."""
    try:
        if not os.path.exists(file_path):
            return []
        if os.path.getsize(file_path) == 0:
            return []

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, FileNotFoundError, PermissionError):
        return []

    except Exception:
        return []
