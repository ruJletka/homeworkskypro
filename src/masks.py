import logging
from pathlib import Path


def setup_logger():
    current_file_path = Path(__file__).resolve()
    project_root = current_file_path.parent.parent

    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / f"app_{__name__}.log"

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)

    return logger


logger = setup_logger()


def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты в виде
    числа и возвращает маску номера по правилу
    XXXX XX** **** XXXX"""

    logger.info(f"Вызов функции get_mask_card_number с аргументом: {card_number}")

    card_number = str(card_number)

    if not card_number.isdigit() or len(card_number) != 16:
        error_msg = "Несуществующий номер карты"
        logger.error(f"Ошибка в get_mask_card_number: {error_msg}. Входные данные: {card_number}")
        return error_msg

    mask_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"
    logger.info(f"Успешное создание маски карты: {mask_number}")

    return mask_number


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску.
    Номер счета замаскирован и отображается в формате **XXXX"""

    logger.info(f"Вызов функции get_mask_account с аргументом: {account_number}")

    account_number = str(account_number)

    if not account_number.isdigit() or len(account_number) != 20:
        error_msg = "Неверный номер аккаунта"
        logger.error(f"Ошибка в get_mask_account: {error_msg}. Входные данные: {account_number}")
        return error_msg

    mask_account = f"**{account_number[-4:]}"
    logger.info(f"Успешное создание маски аккаунта: {mask_account}")

    return mask_account
