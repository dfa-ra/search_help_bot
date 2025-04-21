from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class UtilsCommandsList:
    commands_name = "\n\n # Команды взаибодействия с ботом\n\n"
    commands = [
        ("start", "Запуск бота"),
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
class BotCommands:
    commands: List[Tuple[str, str]]


def get_bot_command():
    return BotCommands(UtilsCommandsList.commands + UserCommandsList.commands)


def get_list_command():
    return [
        UtilsCommandsList.commands_name, UtilsCommandsList.commands,
        UserCommandsList.commands_name, UserCommandsList.commands]
