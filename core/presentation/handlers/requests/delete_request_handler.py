from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes

from app.service_container import ServiceContainer
from core.services import DeleteRequestService


@inject
async def delete_request_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        delete_request_service: DeleteRequestService = Provide[ServiceContainer.delete_request_service],
):
    if len(context.args) != 1:
        await update.message.reply_text("Ввдите номер заявки которую вы хотите удалить")
        return

    result = await delete_request_service.execute(int(context.args[0]), update.effective_user.id)

    await update.message.reply_text(result.message)

