from widget import get_date


def filter_by_state(list_dict: list, state='EXECUTED') -> list:
    '''Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state соответствует указанному значению.'''
    filter_list = []
    for dict_item in list_dict:
        if dict_item.get('state') == state:
            filter_list.append(dict_item)

    return filter_list
