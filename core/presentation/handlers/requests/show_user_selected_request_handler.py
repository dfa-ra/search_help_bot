from io import BytesIO

from dependency_injector.wiring import inject, Provide
from telegram import Update, InputFile
from telegram.ext import ContextTypes

from app.service_container import ServiceContainer
from core.common.completable import SingleResult
from core.presentation.senders import request_with_file_sender, request_sender
from core.services import DrawRequestService, ShowMySelectedRequestsService, GetRequestFileByIdService


# хендлер команды /show_my_selected_requests
# позволяет просматривать все выбраные для работы заявки пользователя
@inject
async def show_user_selected_requests_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        get_request_file_service: GetRequestFileByIdService = Provide[ServiceContainer.get_request_file_service],
        show_my_selected_requests_service: ShowMySelectedRequestsService = Provide[ServiceContainer.show_my_selected_requests_service],
):
    requests: SingleResult = await show_my_selected_requests_service.execute(update.effective_user.id)
    if requests.is_success():
        print(requests)
        for request in requests.result:
            file_result: SingleResult = await get_request_file_service.execute(request.id)
            if file_result.is_success():
                await request_with_file_sender(update, request, file_result.result)
            else:
                await request_sender(update, request)
    else:
        await update.message.reply_text(requests.message)
