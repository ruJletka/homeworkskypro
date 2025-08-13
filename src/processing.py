def filter_by_state(list_dict: list, state: str = 'EXECUTED') -> list:
    """Функция возвращает новый список словарей, содержащий только те словари,
     у которых ключ state соответствует указанному значению."""
    filter_list = []
    for dict_item in list_dict:
        if dict_item.get('state') == state:
            filter_list.append(dict_item)

    return filter_list


def sort_by_date(list_dict: list, descending: bool = True) -> list:
    """Функция, которая принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание). Функция должна возвращать
    новый список, отсортированный по дате (date)."""
    return sorted(list_dict, key=lambda x: x["date"], reverse=descending)
