from dataclasses import dataclass
from typing import Tuple, List

# файл создания команд и добавления текстового описания к ним

@dataclass
class UtilsCommandsList:
    commands_name = "\n\n # Команды взаибодействия с ботом\n\n"
    commands = [
        ("start", "Запуск бота (информация о боте)"),
        ("help", "Помощь"),
        ("info", "Информация о том что к чему вообще")
    ]


@dataclass
class UserCommandsList:
    commands_name = "\n\n # Команды взаимодействия с полезователем\n\n"
    commands = [
        ("add_information", "Добавить информацию о себе"),
        ("who_am_i", "Узнать информацию о себе"),
    ]

@dataclass
class RequestsCommandsList:
    commands_name = "\n\n # Команды взаимодействия с заявками\n\n"
    commands = [
        ("create_request", "Создать заявку"),
        ("close_request", "Закрыть свою заявку по id"),
        ("open_request", "Открыть свою заявку по id"),
        ("show_requests", "Показать все открытые заявки"),
        ("show_my_requests", "Показать мои заявки"),
        ("show_my_selected_requests", "Показать заявки которые я выполняю"),
        ("requests_brainrot", "Показывать заявки в виде ленты"),
        ("delete_request", "Удалить заявку"),
        ("select_request", "Выбрать заявку для выполнения"),
        ("request_completed", "Выбрать сдлеанную заявку и закрыть её")
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
