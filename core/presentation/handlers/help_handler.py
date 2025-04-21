from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes

from app.service_container import ServiceContainer
from core.presentation.command_list import commands
from core.services.help_service import HelpService


@inject
async def help_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        help_service: HelpService = Provide[ServiceContainer.help_service]
):
    text = help_service.execute(commands=commands)
    await update.message.reply_text(text)
