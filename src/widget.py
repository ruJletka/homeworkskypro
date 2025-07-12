from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """Функция, которая умеет обрабатывать информацию как о картах, так и о счетах,
    а затем маскировать их"""
    account_card_split = account_card.split()
    number_card = account_card_split[-1]
    if account_card_split[0] == "Счет":
        result = account_card_split[0] + " " + get_mask_account(number_card)
    else:
        result = " ".join(account_card_split[0:-1]) + " " + get_mask_card_number(number_card)
    return result


def get_date(date_info: str) -> str:
    """Функция, которая принимает на вход строку с датой в формате
    2024-03-11T02:26:18.671407 и возвращает строку с датой в формате
    ДД.ММ.ГГГГ (11.03.2024)."""
    return f"{date_info[8:10]}.{date_info[5:7]}.{date_info[:4]}"
