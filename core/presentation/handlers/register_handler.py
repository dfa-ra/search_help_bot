from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes

from app.service_container import ServiceContainer
from core.models import User
from core.services.user_services import RegisterService


@inject
async def register_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        register_service: RegisterService = Provide[ServiceContainer.register_service]
):
    user = User(telegram_id=update.effective_user.id, name_tag=update.effective_user.name, name=update.effective_user.first_name)
    result = await register_service.execute(user)

    if result.is_failure():
        await update.message.reply_text("Данный пользователь уже зарегестрирован")
