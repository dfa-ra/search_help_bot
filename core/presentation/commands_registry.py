from typing import List, Tuple, Callable
from telegram import BotCommand, Update
from telegram.ext import ContextTypes

from core.presentation.handlers import *
from core.presentation.command_list import commands

handler_mapping = {
    "start": start_handler,
    "help": help_handler,
    "register": register_handler,
}


def get_bot_commands_func() -> List[Tuple[BotCommand, Callable]]:
    return [(BotCommand(command, description), handler_mapping[command]) for command, description in commands]


def get_bot_commands() -> List[BotCommand]:
    return [BotCommand(command, description) for command, description in commands]


def get_list_commands() -> List[Tuple[str, str]]:
    return commands
