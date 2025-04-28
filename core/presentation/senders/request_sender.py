from io import BytesIO

from dependency_injector.wiring import Provide, inject

from app.service_container import ServiceContainer
from core.models import RequestModel, FileModel

from telegram import Update, ReplyKeyboardMarkup, InputFile

from core.services import DrawRequestService

@inject
async def request_with_file_sender(
        update: Update,
        request: RequestModel,
        file: FileModel,
        draw_request_service: DrawRequestService = Provide[ServiceContainer.draw_request_service],
):
    text: str = await draw_request_service.execute(request)
    print("FILE NAME:    " + file.file_name)
    await update.message.reply_document(
        document=InputFile(
            BytesIO(file.file_bytes),
            filename=file.file_name
        ),
        caption=text,
    )

@inject
async def request_sender(
        update: Update,
        request: RequestModel,
        draw_request_service: DrawRequestService = Provide[ServiceContainer.draw_request_service],
):
    text: str = await draw_request_service.execute(request)
    await update.message.reply_text(text)
