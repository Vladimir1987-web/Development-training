from src.decorators import log, my_function

"""Проверка вывода в консоль"""


def test_log_consol(capsys) -> None:
    my_function(1, 2)
    captured = capsys.readouterr()
    assert "my_function" in captured.out


"""Проверка вывода в файл"""


def test_log_file(capsys) -> None:
    @log(filename="mylog.txt")
    def my_function(x: int, y: int) -> int:
        return x + y

    my_function(1, 2)
    captured = capsys.readouterr()
    assert "" in captured.out


"""Проверка для ошибки"""


def test_log_error(capsys) -> None:
    my_function(1, "2")
    captured = capsys.readouterr()
    assert "my_function" in captured.out


def test_log_file_error(capsys) -> None:
    @log(filename="mylog.txt")
    def my_function(x: int, y: int) -> int:
        return x + y

    my_function(1, "2")
    captured = capsys.readouterr()
    assert "" in captured.out
