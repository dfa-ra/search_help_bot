from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.service_container import ServiceContainer
from core.models import Request
from core.services import CreateRequestService, IsIntegerService

TOPIC, MAIN_TEXT, DEADLINE, MONEY = range(4)


@inject
async def create_requests_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data["request"] = Request()
    await update.message.reply_text(" # Создание заявки на решение задания началось.")
    await update.message.reply_text(" # Опишите тему задания...")
    return TOPIC


async def topic_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, ):
    context.user_data["request"].topic = update.message.text.lower()
    await update.message.reply_text(" # Опишите само задание.")
    return MAIN_TEXT


async def main_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["request"].main_text = update.message.text.lower()
    await update.message.reply_text(" # Опишите дедлайн задания.")
    return DEADLINE


async def deadline_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Сохраняем дедлайн
    context.user_data["request"].deadline = update.message.text.lower()
    await update.message.reply_text(" # Напишите цену, которую вы готовы заплатить за него.")
    return MONEY


@inject
async def money_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        create_request_service: CreateRequestService = Provide[ServiceContainer.create_request_service],
        is_integer_service: IsIntegerService = Provide[ServiceContainer.is_integer_service],
):
    try:
        context.user_data["request"].money = int(update.message.text.lower())
    except ValueError:
        await update.message.reply_text("Братец введи число... ну по братски😭")
        return MONEY

    if context.user_data["request"].money <= 0:
        await update.message.reply_text("Число должно быть больше нуля🤡")
        return MONEY

    if context.user_data["request"].money >= 1_000_000:
        await update.message.reply_text("Ты рофлишь?? больше миллиона.. давай ка скинь маленько")
        return MONEY


    request = context.user_data["request"]
    request.creator_id = update.effective_user.id
    request.is_open = True

    result = await create_request_service.execute(request)

    await update.message.reply_text(result.message)

    await update.message.reply_text(result.message)
    del context.user_data["request"]
    return ConversationHandler.END
