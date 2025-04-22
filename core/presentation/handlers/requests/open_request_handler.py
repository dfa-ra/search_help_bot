from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes

from app.service_container import ServiceContainer
from core.services import OpenRequestService


@inject
async def open_request_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        open_my_request_service: OpenRequestService = Provide[ServiceContainer.open_my_request_service]
):
    if len(context.args) != 1:
        await update.message.reply_text("Ввдите номер заявки которую вы хотите открыть")
        return

    result = await open_my_request_service.execute(int(context.args[0]), update.effective_user.id)

    await update.message.reply_text(result.message)
