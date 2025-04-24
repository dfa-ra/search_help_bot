from typing import List, Tuple, Callable
from telegram import BotCommand
from telegram.ext import CommandHandler, filters, MessageHandler, CallbackQueryHandler

from core.presentation.handlers import *
from core.presentation.commands.command_lists import get_bot_command, get_list_command

utils_handler_mapping = {
    "start": register_handler,
    "help": help_handler,
}

users_handler_mapping = {
    "who_am_i": info_handler
}

requests_handler_mapping = {
    "close_request": close_request_handler,
    "open_request": open_request_handler,
    "show_requests": show_all_open_requests_handler,
    "show_my_requests": show_user_requests_handler,
    "show_my_selected_requests": show_user_selected_requests_handler,
    "requests_brainrot": requests_brainrot_handler,
    "delete_request": delete_request_handler,
    "select_request": add_request_executor_handler
}

handler_mapping = users_handler_mapping | utils_handler_mapping | requests_handler_mapping

message_handler_mapping = [
    ConversationHandler(
        entry_points=[CommandHandler('create_request', create_requests_handler)],
        states={
            TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, topic_handler)],
            MAIN_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_text_handler)],
            DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, deadline_handler)],
            MONEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, money_handler)],
        },
        fallbacks=[],
    ),
    ConversationHandler(
        entry_points=[CommandHandler('add_information', add_information_handler)],
        states={
            UNIVERSITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_university_handler)],
            COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_course_handler)],
            DIRECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_direction_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel_handler)],
    ),
    MessageHandler(filters.TEXT & ~filters.COMMAND, request_brainrot_button_handle)

]




def get_list_message_handler():
    return message_handler_mapping


def get_bot_commands_func() -> List[Tuple[BotCommand, Callable]]:
    bot_commands = get_bot_command().commands
    result = []
    for command, description in bot_commands:
        handler = handler_mapping.get(command)
        if handler is not None:
            result.append((BotCommand(command, description), handler))
    return result

def get_bot_commands() -> List[BotCommand]:
    bot_commands = get_bot_command().commands
    return [BotCommand(command, description) for command, description in bot_commands]


def get_list_commands():
    return get_list_command()
