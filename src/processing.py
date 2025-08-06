from datetime import datetime


def filter_by_state(list_dict: list, state='EXECUTED') -> list:
    '''Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state соответствует указанному значению.'''
    filter_list = []
    for dict_item in list_dict:
        if dict_item.get('state') == state:
            filter_list.append(dict_item)

    return filter_list


def sort_by_date(date_list: list, date_key='date', descending=True) -> list:
    '''Функция, которая принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание). Функция должна возвращать
    новый список, отсортированный по дате (date).'''
    return sorted(date_list, key=lambda x: datetime.strptime(x[date_key], '%Y-%m-%dT%H:%M:%S.%f'), reverse=descending)
