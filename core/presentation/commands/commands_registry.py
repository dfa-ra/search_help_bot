from typing import List, Tuple, Callable
from telegram import BotCommand

from core.presentation.handlers import *
from core.presentation.commands.command_lists import get_bot_command, get_list_command

utils_handler_mapping = {
    "start": start_handler,
    "help": help_handler,
}

users_handler_mapping = {
    "register": register_handler,
    "who_am_i": info_handler
}

handler_mapping = users_handler_mapping | utils_handler_mapping


def get_bot_commands_func() -> List[Tuple[BotCommand, Callable]]:
    bot_commands = get_bot_command().commands
    return [(BotCommand(command, description), handler_mapping[command]) for command, description in bot_commands]


def get_bot_commands() -> List[BotCommand]:
    bot_commands = get_bot_command().commands
    return [BotCommand(command, description) for command, description in bot_commands]


def get_list_commands():
    return get_list_command()
