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
    assert "divide error: ZeroDivisionError. Inputs: (10, 0)" in captured.out


def test_log_file(tmp_path):
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def sum_numbers(a, b):
        return a + b

    assert sum_numbers(2, 3) == 5

    with open(log_file, "r", encoding="utf-8") as file:
        assert "Функция sum_numbers ок. Результат: 5" in file.read()


def test_error_log_file(tmp_path):
    log_file = tmp_path / "error_log.txt"

    @log(filename=str(log_file))
    def faulty_func():
        raise ValueError("Test error")

    faulty_func()

    with open(log_file) as f:
        content = f.read()

    assert "faulty_func error: ValueError" in content
    assert "Inputs: (), {}" in content
