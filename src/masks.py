def get_mask_card_number(card_number: str) -> str:
    '''Функция принимает на вход номер карты в виде
     числа и возвращает маску номера по правилу
     XXXX XX** **** XXXX'''
    card_number = str(card_number)
    if not card_number.isdigit() or len(card_number) != 16:
        return 'Несуществующий номер карты'
    mask_number = f'{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}'
    return mask_number


def get_mask_account(account_number: str) -> str:
    '''Функция принимает на вход номер счета и возвращает его маску.
    Номер счета замаскирован и отображается в формате **XXXX'''
    account_number = str(account_number)
    if not account_number.isdigit() or len(account_number) < 4:
        return 'Номер аккаунта состоит из не менее чем 4 цифр'
    mask_account = f'**{account_number[-4:]}'
    return mask_account
