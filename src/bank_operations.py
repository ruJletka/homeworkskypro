import re
from typing import Dict, List


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """Фильтрует список банковских операций по строке поиска в описании."""
    if not search:
        return data

    try:
        pattern = re.compile(re.escape(search), re.IGNORECASE)

        result = [
            operation
            for operation in data
            if operation.get("description") and pattern.search(operation["description"])
        ]

        return result

    except re.error:
        return []
