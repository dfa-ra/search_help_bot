from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes

from app.service_container import ServiceContainer
from core.presentation.commands.command_lists import get_list_command
from core.services import HelpService


@inject
async def help_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        help_service: HelpService = Provide[ServiceContainer.help_service]
):
    text = help_service.execute(commands=get_list_command())
    await update.message.reply_text(text)
