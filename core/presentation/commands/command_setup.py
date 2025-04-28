from telegram.ext import CommandHandler, MessageHandler, filters

from core.presentation.commands.commands_registry import get_bot_commands, get_bot_commands_func, \
    get_list_message_handler

# подключение команд к боту

def register_commands(app):
    commands = get_bot_commands_func()
    for (bot_command, func) in commands:
        app.add_handler(CommandHandler(bot_command.command, func))

    message_commands = get_list_message_handler()
    for dialog in message_commands:
        app.add_handler(dialog)


async def setup_bot_commands(bot):
    await bot.set_my_commands(get_bot_commands())
