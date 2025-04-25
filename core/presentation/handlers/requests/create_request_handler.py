from bson import Binary

from dependency_injector.wiring import inject, Provide
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from app.service_container import ServiceContainer
from core.common.completable import CompletableRequestsResult
from core.models import Request, FileModel
from core.services import CreateRequestService, IsIntegerService, SaveRequestFileService, DeleteRequestService

TOPIC, MAIN_TEXT, FILE_DESCRIPTION, DEADLINE, MONEY = range(5)


@inject
async def create_requests_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data["request"] = Request()
    await update.message.reply_text(" # Создание заявки на решение задания началось.")
    await update.message.reply_text(" # Опишите тему задания...")
    return TOPIC


async def topic_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["request"].topic = update.message.text.lower()
    await update.message.reply_text(" # Опишите само задание.")
    return MAIN_TEXT


async def main_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["request"].main_text = update.message.text.lower()

    keyboard = [["Без файла"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        " # Пришли файл (pdf, docx) в котором будет подробное описание задачи. "
        "Можешь вставить туда дополнительные ссылки или скриншоты помогающие лучше понять "
        "задачу", reply_markup=reply_markup
    )
    return FILE_DESCRIPTION


async def description_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    text = update.message.text

    if isinstance(text, str) and text == "Без файла":
        context.user_data["request_file"] = None
        await update.message.reply_text(" # Напиши дедлайн задания.")
        return DEADLINE

    if document is None:
        await update.message.reply_text("Пожалуйста, пришли файл.")
        return FILE_DESCRIPTION

    file_id = document.file_id
    new_file = await context.bot.get_file(file_id)
    file_bytes = await new_file.download_as_bytearray()

    context.user_data["request_file"] = FileModel(
        file_name=document.file_name,
        file_bytes=Binary(file_bytes),
        mime_type=document.mime_type
    )
    await update.message.reply_text(" # Напиши дедлайн задания.")
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
        delete_request_service: DeleteRequestService = Provide[ServiceContainer.delete_request_service],
        save_request_file_service: SaveRequestFileService = Provide[ServiceContainer.save_request_file_service]
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

    result_create: CompletableRequestsResult = await create_request_service.execute(request)

    if result_create.is_success():

        document = context.user_data["request_file"]

        if document is None:
            await update.message.reply_text(result_create.message)
        else:
            result_add_file = await save_request_file_service.execute(
                result_create.request.id,
                result_create.request.creator_id,
                document,
            )
            if result_add_file.is_success():
                await update.message.reply_text(result_create.message)

            if result_add_file.is_failure():
                await delete_request_service.execute(result_create.request.id, result_create.request.creator_id)
                await update.message.reply_text(result_add_file.message)

    else:
        await update.message.reply_text(result_create.message)

    del context.user_data["request"]
    del context.user_data["request_file"]
    return ConversationHandler.END
