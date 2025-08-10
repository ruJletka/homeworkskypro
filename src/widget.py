from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """Функция, которая умеет обрабатывать информацию как о картах, так и о счетах,
    а затем маскировать их"""

    parts_number = account_card.split()
    account_type = parts_number[0]
    number = parts_number[-1]


    if account_type == "Счет":
        masked = get_mask_account(number)
        return masked if masked == "Неверный номер аккаунта" else f"{account_type} {masked}"


    masked = get_mask_card_number(number)
    if masked == "Несуществующий номер карты":
        return masked

    return f"{' '.join(parts_number[:-1])} {masked}"


def get_date(date_info: str) -> str:
    """Функция, которая принимает на вход строку с датой в формате
    2024-03-11T02:26:18.671407 и возвращает строку с датой в формате
    ДД.ММ.ГГГГ (11.03.2024)."""
    return f"{date_info[8:10]}.{date_info[5:7]}.{date_info[:4]}"
