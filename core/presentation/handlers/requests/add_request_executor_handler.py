from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes

from app.service_container import ServiceContainer
from core.services import SelectRequestService


# хендлер команды /select_request
# позволяет добавлять на заявки их исполнителя
@inject
async def add_request_executor_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        select_request_service: SelectRequestService = Provide[ServiceContainer.select_request_service],
):
    if len(context.args) != 1:
        await update.message.reply_text(" # Ввдите номер заявки которую вы хотите выполнить")
        return

    result = await select_request_service.execute(int(context.args[0]), update.effective_user.id)

    await update.message.reply_text(result.message)
