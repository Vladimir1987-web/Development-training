import time
import timeit


def log(filename=None):
    """
    Декоратор log автоматически логирует начало и конец выполнения функции,
    а также ее результаты или возникшие ошибки
    """

    def my_decorator(function):

        def wrapper(*args, **kwargs):
            named_tuple = time.localtime()  # получить struct_time
            time_string = time.strftime("%d/%m/%Y, %H:%M:%S", named_tuple)
            print(f"Функция {function.__name__} начинает работу: {time_string}")

            try:
                result = function(*args, **kwargs)
                success_message = f"{function.__name__} ok. Результат: {result}"
                print(
                    f"Время выполнения декоратора составило:"
                    f"{timeit.timeit(lambda: function(*args, **kwargs), number=1):.6f} секунд."
                )
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(success_message + "\n")
                else:
                    print(success_message)

            except TypeError as e:
                error_message = f"{function.__name__} error:{type(e).__name__}. Inputs: args :{args}, kwargs{kwargs}"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message + "\n")
                else:
                    print(error_message)

        return wrapper

    return my_decorator


@log()
def my_function(x: int, y: int) -> int:
    """Складывает два числа"""
    return x + y


if __name__ == "__main__":
    my_function(1, "2")
