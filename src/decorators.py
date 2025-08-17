from functools import wraps


def log(filename = None):
    """Декоратор, который будет автоматически логировать начало и конец выполнения функции,
     а также ее результаты или возникшие ошибки."""
    def decorator(function):
        """Внутренний декоратор, который применяется к целевой функции."""
        @wraps(function)
        def wrapper(*args, **kwargs):
            """Оберточная функция, которая выполняет логирование перед и после вызова целевой функции."""
            try:
                result = function(*args, **kwargs)
                name_function = function.__name__
                if filename:
                    file = open(filename, "a", encoding="utf-8")
                    file.write(f"Функция {name_function} ок. Результат: {result}" + "\n")
                    file.close()
                else:
                    print(f"{name_function} ок. Результат: {function(*args, **kwargs)}")
            except Exception as e:
                result = None
                print(f"{function.__name__} error: {e}. Inputs: {args}, {kwargs}")
            except ZeroDivisionError:
                result = None
                print(f"{function.__name__} error: ZeroDivisionError. Inputs: {args}, {kwargs}")

            return result

        return wrapper

    return decorator
