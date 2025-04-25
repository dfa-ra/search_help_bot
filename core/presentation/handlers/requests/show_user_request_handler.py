from io import BytesIO

from dependency_injector.wiring import inject, Provide
from telegram import Update, InputFile
from telegram.ext import ContextTypes

from app.service_container import ServiceContainer
from core.common.completable import CompletableRequestsResult, CompletableFileResult
from core.services import DrawRequestService, ShowMyRequestsService, GetRequestFileByIdService


@inject
async def show_user_requests_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        get_request_file_service: GetRequestFileByIdService = Provide[ServiceContainer.get_request_file_service],
        show_my_requests_service: ShowMyRequestsService = Provide[ServiceContainer.show_my_requests_service],
        draw_request_service: DrawRequestService = Provide[ServiceContainer.draw_request_service],
):
    requests: CompletableRequestsResult = await show_my_requests_service.execute(update.effective_user.id)
    if requests.is_success():
        print(requests)
        for request in requests.list:
            text = await draw_request_service.execute(request)
            file_result: CompletableFileResult = await get_request_file_service.execute(request.id)
            if file_result.is_success():
                print("FILE NAME:    " + file_result.file.file_name)
                await update.message.reply_document(
                    document=InputFile(
                        BytesIO(file_result.file.file_bytes),
                        filename=file_result.file.file_name
                    ),
                    filename=file_result.file.file_name,
                    caption=text,
                )
            else:
                print("ФАЙЛА НЕ БУДЕТ ПУПУПУ")
                await update.message.reply_text(text)
    else:
        await update.message.reply_text(requests.message)
