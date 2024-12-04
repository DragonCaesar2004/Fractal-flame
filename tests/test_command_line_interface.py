import pytest
from src.command_line_interface import (
    CommandLineInterface,
)  # Предполагаемое имя модуля и класса
from src.custom_exception import CustomException
from src.config import max_iteration_num
from src.project_types import UserData


@pytest.fixture()
def cli_fixture():
    return CommandLineInterface()


def test_get_size_valid_input(monkeypatch, cli_fixture):
    monkeypatch.setattr("builtins.input", lambda input: "10")
    side_message = "ширину"
    min_size = 5
    max_size = 2000
    result = cli_fixture._get_size(side_message, min_size, max_size)
    assert result == 10


def test_get_size_multiple_args(monkeypatch, cli_fixture):
    monkeypatch.setattr("builtins.input", lambda input: "10 20")
    side_message = "высоту"
    min_size = 5
    max_size = 2000
    with pytest.raises(CustomException) as exc_info:
        cli_fixture._get_size(side_message, min_size, max_size)
    assert str(exc_info.value) == cli_fixture._get_only_one_arg_message()


def test_get_size_non_int_input(monkeypatch, cli_fixture):
    monkeypatch.setattr("builtins.input", lambda input: "десять")
    side = "высоту"
    min_size = 5
    max_size = 2000
    with pytest.raises(CustomException) as exc_info:
        cli_fixture._get_size(side, min_size, max_size)
    assert str(exc_info.value) == cli_fixture._get_not_int_message()


def test_get_size_less_than_min(monkeypatch, cli_fixture):

    monkeypatch.setattr("builtins.input", lambda input: "3")
    side = "высоту"
    min_size = 5
    max_size = 2000
    with pytest.raises(CustomException) as exc_info:
        cli_fixture._get_size(side, min_size, max_size)
    assert str(exc_info.value) == "Размер должен быть больше или равен " + str(min_size)


def test_get_size_more_than_max(monkeypatch, cli_fixture):

    monkeypatch.setattr("builtins.input", lambda input: "3000")
    side = "высоту"
    min_size = 5
    max_size = 2000
    with pytest.raises(CustomException) as exc_info:
        cli_fixture._get_size(side, min_size, max_size)
    assert str(exc_info.value) == "Размер должен быть меньше или равен " + str(max_size)


def test_get_size_message(cli_fixture):
    assert cli_fixture._get_size_message("ширину") == "Введите ширину изображения: "


def test_get_only_one_arg_message(cli_fixture):
    assert (
        cli_fixture._get_only_one_arg_message()
        == "Пожалуйста, введите только один аргумент."
    )


def test_get_not_int_message(cli_fixture):
    assert cli_fixture._get_not_int_message() == "Ввод должен быть целым числом."


def test_get_less_than_min_message(cli_fixture):
    assert (
        cli_fixture._get_less_than_min_message()
        == "Размер должен быть больше или равен "
    )


def test_get_more_than_max_message(cli_fixture):
    assert (
        cli_fixture._get_more_than_max_message()
        == "Размер должен быть меньше или равен "
    )


def test_get_width_input_message(cli_fixture):
    assert cli_fixture._get_width_input_message() == "Введите ширину изображения."


def test_get_height_input_message(cli_fixture):
    assert cli_fixture._get_height_input_message() == "Введите высоту изображения."


def test_valid_iterations_input(monkeypatch, cli_fixture):

    monkeypatch.setattr("builtins.input", lambda input: "5000")
    result = cli_fixture._get_iterations_number()
    assert result == 5000


def test_negative_iterations_input(monkeypatch, cli_fixture):

    monkeypatch.setattr("builtins.input", lambda input: "-5000")
    with pytest.raises(CustomException) as exc_info:
        cli_fixture._get_iterations_number()
    assert str(exc_info.value) == "Ввод должен быть положительным числом."


def test_exceeding_iterations_input(monkeypatch, cli_fixture):

    monkeypatch.setattr("builtins.input", lambda input: str(max_iteration_num + 1))
    with pytest.raises(CustomException) as exc_info:
        cli_fixture._get_iterations_number()
    assert (
        str(exc_info.value)
        == "Введеное число итераций превышает максимальное значение, программа будет слишком долго работать."
    )


def test_non_integer_input(monkeypatch, cli_fixture):
    monkeypatch.setattr("builtins.input", lambda input: "три")
    with pytest.raises(CustomException) as exc_info:
        cli_fixture._get_iterations_number()
    assert str(exc_info.value) == "Ввод должен быть целым числом."


def test_float_input(monkeypatch, cli_fixture):
    monkeypatch.setattr("builtins.input", lambda input: "123.45")
    with pytest.raises(CustomException) as exc_info:
        cli_fixture._get_iterations_number()
    assert str(exc_info.value) == "Ввод должен быть целым числом."


def test_get_transformer_function_set_valid(monkeypatch, cli_fixture):
    monkeypatch.setattr("builtins.input", lambda input: "1 2")
    assert cli_fixture._get_transformer_function_set() == {1, 2}


def test_get_transformer_function_set_empty_input(monkeypatch, cli_fixture):
    monkeypatch.setattr("builtins.input", lambda input: "")
    with pytest.raises(CustomException) as exc:
        cli_fixture._get_transformer_function_set()
    assert str(exc.value) == "Введите не пустую строку."


def test_get_transformer_function_set_invalid_range(monkeypatch, cli_fixture):
    monkeypatch.setattr("builtins.input", lambda input: "1000")
    with pytest.raises(CustomException) as exc:
        cli_fixture._get_transformer_function_set()
    assert str(exc.value) == "Вы ввели число не из заданного диапазона."


def test_get_transformer_function_set_duplicate(monkeypatch, cli_fixture):
    monkeypatch.setattr("builtins.input", lambda input: "1 2 2")
    with pytest.raises(CustomException) as exc:
        cli_fixture._get_transformer_function_set()
    assert str(exc.value) == "Вы ввели повторяющееся значение."


def test_int_validate_valid(cli_fixture):
    assert cli_fixture._int_validate("1") == 1


def test_int_validate_invalid(cli_fixture):
    with pytest.raises(CustomException) as exc:
        cli_fixture._int_validate("abc")
    assert str(exc.value) == "Ввод должен быть целым числом."


def test_get_empty_input_message(cli_fixture):
    assert cli_fixture._get_empty_input_message() == "Введите не пустую строку."


def test_get_not_in_range_message(cli_fixture):
    assert (
        cli_fixture._get_not_in_range_message()
        == "Вы ввели число не из заданного диапазона."
    )


def test_get_duplicate_input_message(cli_fixture):
    assert cli_fixture._get_duplicate_input() == "Вы ввели повторяющееся значение."


@pytest.fixture
def mock_cli(mocker):
    """Создаем экземпляр класса с использованием mocker для моков."""
    cli = CommandLineInterface()
    mocker.patch.object(cli, "_get_width_input_message", return_value=500)
    mocker.patch.object(cli, "_get_height_input_message", return_value=300)
    mocker.patch.object(cli, "_get_iterations_number", return_value=10)
    mocker.patch.object(cli, "_get_transformer_function_set", return_value={1, 2, 3})
    mocker.patch.object(
        cli,
        "_get_size",
        side_effect=lambda val, min_val, max_val: max(min_val, min(val, max_val)),
    )
    return cli


def test_get_user_data(mocker):
    cli = CommandLineInterface()

    # Мокаем методы с помощью pytest-mock
    mocker.patch.object(cli, "_get_size", side_effect=[500, 500])
    mocker.patch.object(
        cli, "_get_width_input_message", return_value="Введите ширину изображения."
    )
    mocker.patch.object(
        cli, "_get_height_input_message", return_value="Введите высоту изображения."
    )
    mocker.patch.object(cli, "_get_iterations_number", return_value=5)
    mocker.patch.object(cli, "_get_transformer_function_set", return_value={1, 2, 3})

    expected_user_data = UserData(
        img_width_in_pixels=500,
        img_height_in_pixels=500,
        iterations_number=5,
        transformer_function_set={1, 2, 3},
    )

    assert cli.get_user_data() == expected_user_data
