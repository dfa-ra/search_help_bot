from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class UtilsCommandsList:
    commands_name = "\n\n # Команды взаибодействия с ботом\n\n"
    commands = [
        ("start", "Запуск бота (информация о боте)"),
        ("help", "Помощь"),
    ]


@dataclass
class UserCommandsList:
    commands_name = "\n\n # Команды взаимодействия с полезователем\n\n"
    commands = [
        ("register", "Зарегистрироваться в систему"),
        ("who_am_i", "Узнать информацию о себе"),
    ]

@dataclass
class RequestsCommandsList:
    commands_name = "\n\n # Команды взаимодействия с заявками\n\n"
    commands = [
        ("create_request", "Создать заявку по id"),
        ("close_request", "Закрыть заявку по id"),
        ("open_request", "Открыть заявку по id"),
        ("show_requests", "Показать все открытые заявки"),
        ("show_my_requests", "Показать мои заявки"),
        ("show_my_selected_requests", "Показать заявки которые я выполняю"),
        ("delete_request", "Удалить заявку"),
        ("select_request", "Выбрать заявку для выполнения"),
    ]

@dataclass
class BotCommands:
    commands: List[Tuple[str, str]]


def get_bot_command():
    return BotCommands(UtilsCommandsList.commands + UserCommandsList.commands + RequestsCommandsList.commands)


def get_list_command():
    return [
        UtilsCommandsList.commands_name, UtilsCommandsList.commands,
        UserCommandsList.commands_name, UserCommandsList.commands,
        RequestsCommandsList.commands_name, RequestsCommandsList.commands
    ]
