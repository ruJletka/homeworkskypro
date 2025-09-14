import re
from collections import Counter
from typing import Dict, List


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество операций по заданным категориям на основе поля description."""
    if not categories or not data:
        return {}

    category_counter = Counter()

    for category in categories:
        category_counter[category] = 0

    patterns = {}
    for category in categories:
        try:
            patterns[category] = re.compile(re.escape(category), re.IGNORECASE)
        except re.error:
            patterns[category] = None

    for operation in data:
        description = operation.get("description", "")
        if not isinstance(description, str) or not description.strip():
            continue

        for category in categories:
            pattern = patterns[category]
            if pattern and pattern.search(description):
                category_counter[category] += 1

    return dict(category_counter)
