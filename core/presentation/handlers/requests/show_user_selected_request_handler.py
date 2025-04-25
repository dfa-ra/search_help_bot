from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes

from app.service_container import ServiceContainer
from core.common.completable import CompletableRequestsResult
from core.services import DrawRequestService, ShowMySelectedRequestsService


@inject
async def show_user_selected_requests_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        show_my_selected_requests_service: ShowMySelectedRequestsService = Provide[ServiceContainer.show_my_selected_requests_service],
        draw_request_service: DrawRequestService = Provide[ServiceContainer.draw_request_service],
):
    requests: CompletableRequestsResult = await show_my_selected_requests_service.execute(update.effective_user.id)
    if requests.is_success():
        print(requests)
        for request in requests.list:
            text = await draw_request_service.execute(request)
            await update.message.reply_text(text)
    else:
        await update.message.reply_text(requests.message)
