from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes

from app.service_container import ServiceContainer
from core.common.completable import CompletableResult
from core.services import UserInfoService


# хендлер команды /who_am_i
# показывает информацию о пользователе
@inject
async def user_info_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        info_user_service: UserInfoService = Provide[ServiceContainer.user_info_service]
):
    result: CompletableResult = await info_user_service.execute(update.effective_user.id)
    await update.message.reply_text(result.message)
