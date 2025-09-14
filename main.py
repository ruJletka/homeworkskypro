import logging
from pathlib import Path
from typing import Any, Dict, List

from src.bank_analytics import process_bank_operations
from src.bank_operations import process_bank_search
from src.file_reader import read_transaction_csv, read_transaction_excel
from src.generators import filter_by_currency, transaction_descriptions
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transaction_data
from src.widget import get_date, mask_account_card


def setup_logger():
    """Настройка логгера"""
    current_file_path = Path(__file__).resolve()
    project_root = current_file_path.parent.parent

    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / "app_main.log"

    logger = logging.getLogger("main")
    logger.setLevel(logging.DEBUG)

    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)

    return logger


logger = setup_logger()


def display_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода в консоль"""
    try:
        date_str = get_date(transaction.get("date", ""))

        description = transaction.get("description", "Нет описания")

        from_info = transaction.get("from", "")
        to_info = transaction.get("to", "")

        from_str = mask_account_card(from_info) if from_info else "Не указано"
        to_str = mask_account_card(to_info) if to_info else "Не указано"

        amount = transaction.get("operationAmount", {}).get("amount", "0")
        currency = transaction.get("operationAmount", {}).get("currency", {}).get("name", "руб.")

        return f"""
{date_str} {description}
{from_str} -> {to_str}
Сумма: {amount} {currency}
"""
    except Exception as e:
        logger.error(f"Ошибка при форматировании транзакции: {e}")
        return f"Ошибка отображения транзакции: {transaction.get('id', 'unknown')}"


def get_user_input(prompt: str, valid_options: List[str] = None) -> str:
    """Получает ввод от пользователя с валидацией"""
    while True:
        user_input = input(prompt).strip().lower()

        if valid_options:
            if user_input in [opt.lower() for opt in valid_options]:
                return user_input
            print(f"Пожалуйста, введите один из вариантов: {', '.join(valid_options)}")
        else:
            return user_input


def main():
    """Основная функция программы"""
    logger.info("Запуск программы")

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = get_user_input("Ваш выбор (1-3): ", ["1", "2", "3"])

    transactions = []
    file_type = ""

    if file_choice == "1":
        file_type = "JSON"
        print("Для обработки выбран JSON-файл.")
        transactions = load_transaction_data()
    elif file_choice == "2":
        file_type = "CSV"
        print("Для обработки выбран CSV-файл.")
        transactions = read_transaction_csv()
    elif file_choice == "3":
        file_type = "XLSX"
        print("Для обработки выбран XLSX-файл.")
        transactions = read_transaction_excel()

    logger.info(f"Загружено {len(transactions)} транзакций из {file_type}-файла")

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}")

        status_input = input("Статус: ").strip().upper()

        if status_input in valid_statuses:
            filtered_transactions = filter_by_state(transactions, status_input)
            print(f'Операции отфильтрованы по статусу "{status_input}"')
            logger.info(f"Фильтрация по статусу: {status_input}, найдено: {len(filtered_transactions)}")
            break
        else:
            print(f'Статус операции "{status_input}" недоступен.')
            logger.warning(f"Пользователь ввел неверный статус: {status_input}")

    sort_choice = get_user_input("\nОтсортировать операции по дате? Да/Нет: ", ["да", "нет"])

    if sort_choice == "да":
        order_choice = get_user_input(
            "Отсортировать по возрастанию или по убыванию? ", ["по возрастанию", "по убыванию"]
        )

        descending = order_choice == "по убыванию"
        filtered_transactions = sort_by_date(filtered_transactions, descending)
        logger.info(f"Сортировка по дате: {'убывание' if descending else 'возрастание'}")

    currency_choice = get_user_input("\nВыводить только рублевые транзакции? Да/Нет: ", ["да", "нет"])

    if currency_choice == "да":
        rub_transactions = []
        for transaction in filtered_transactions:
            currency_code = transaction.get("operationAmount", {}).get("currency", {}).get("code", "")
            if currency_code == "RUB":
                rub_transactions.append(transaction)
        filtered_transactions = rub_transactions
        logger.info(f"Фильтрация по рублевым транзакциям, осталось: {len(filtered_transactions)}")

    search_choice = get_user_input(
        "\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет: ", ["да", "нет"]
    )

    if search_choice == "да":
        search_word = input("Введите слово для поиска в описании: ").strip()
        if search_word:
            filtered_transactions = process_bank_search(filtered_transactions, search_word)
            logger.info(f"Поиск по слову '{search_word}', найдено: {len(filtered_transactions)}")

    print("\nРаспечатываю итоговый список транзакций...")

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        logger.warning("Не найдено транзакций после всех фильтров")
        return

    print(f"\nВсего банковских операций в выборке: {len(filtered_transactions)}")

    for transaction in filtered_transactions:
        print(display_transaction(transaction))
        print("-" * 50)

    logger.info(f"Успешно отображено {len(filtered_transactions)} транзакций")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(f"Критическая ошибка в main: {e}")
        print("Произошла непредвиденная ошибка. Программа завершена.")
