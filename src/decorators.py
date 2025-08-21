from functools import wraps


def log(filename=None):
    """Декоратор, который будет автоматически логировать начало и конец выполнения функции,
     а также ее результаты или возникшие ошибки."""
    def decorator(function):
        """Внутренний декоратор, который применяется к целевой функции."""
        @wraps(function)
        def wrapper(*args, **kwargs):
            """Оберточная функция, которая выполняет логирование перед и после вызова целевой функции."""
            try:
                result = function(*args, **kwargs)
                message = f"Функция {function.__name__} ок. Результат: {result}"
            except Exception as e:
                result = None
                message = f"{function.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"

            if filename:
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(message + "\n")
            else:
                print(message)

            return result
        return wrapper
    return decorator
