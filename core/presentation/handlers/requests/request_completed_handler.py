from dependency_injector.wiring import Provide, inject
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from app.service_container import ServiceContainer
from core.common.completable import SingleResult
from core.services import ShowMySelectedRequestsService

COMPLETE_REQUEST, BAD_END = range(2)


@inject
async def request_completed_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        show_my_selected_requests_service: ShowMySelectedRequestsService = Provide[
            ServiceContainer.show_my_selected_requests_service],
):
    requests: SingleResult = await show_my_selected_requests_service.execute(update.effective_user.id)
    print(requests.result)
    if requests.is_success():
        keyboard = [[
            "№" + str(request.id) + " " + request.topic] for request in requests.result
                    ] + [["Все перечисленные"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            " # Выбери ту заявку которую ты хочешь закрыть ",
            reply_markup=reply_markup
        )
        return COMPLETE_REQUEST
    else:
        await update.message.reply_text(requests.message)
        return BAD_END


async def complete_request_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    pass


async def request_bad_end_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    pass
