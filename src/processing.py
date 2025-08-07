def filter_by_state(list_dict: list, state: str = 'EXECUTED') -> list:
    """Функция возвращает новый список словарей, содержащий только те словари,
     у которых ключ state соответствует указанному значению."""
    filter_list = []
    for dict_item in list_dict:
        if dict_item.get('state') == state:
            filter_list.append(dict_item)

    return filter_list


if __name__ == "__main__":
    result = filter_by_state([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                              {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                              {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                              {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}])
    print(result)


def sort_by_date(date_list: list, descending: bool = True) -> list:
    """Функция, которая принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание). Функция должна возвращать
    новый список, отсортированный по дате (date)."""
    return sorted(date_list, key=lambda x: x["date"], reverse=descending)
