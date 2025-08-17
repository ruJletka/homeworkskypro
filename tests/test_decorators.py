import pytest

from src.decorators import log


def test_log_success(capsys):
    @log()
    def add(a, b):
        return a + b

    result = add(2, 3)
    captured = capsys.readouterr()
    assert result == 5
    assert ("add ок. Результат: 5" in captured.out)


def test_log_error(capsys):
    @log()
    def divide(a, b):
        return a / b

    result = divide(10, 0)
    captured = capsys.readouterr()
    assert result is None
    assert "divide error: division by zero. Inputs: (10, 0)" in captured.out


def test_log_file(tmp_path):
    log_file = tmp_path / "test_log.txt"

    @log(filename=("test_log.txt"))
    def sum_numbers(a, b):
        return a + b

    assert sum_numbers(2, 3) == 5

    with open("test_log.txt", "r", encoding="utf-8") as file:
        assert "Функция sum_numbers ок. Результат: 5" in file.read()
