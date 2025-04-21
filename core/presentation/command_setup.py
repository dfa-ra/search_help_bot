from telegram.ext import CommandHandler

from core.presentation.commands_registry import get_bot_commands, get_bot_commands_func

def register_commands(app):
    commands = get_bot_commands_func()
    for (bot_command, func) in commands:
        app.add_handler(CommandHandler(bot_command.command, func))

async def setup_bot_commands(bot):
    await bot.set_my_commands(get_bot_commands())
